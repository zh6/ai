from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import XinferenceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
import shutil
from dotenv import load_dotenv
import chromadb

load_dotenv()

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置向量库存储路径
PERSIST_DIRECTORY = "knowledge_base"
if not os.path.exists(PERSIST_DIRECTORY):
    os.makedirs(PERSIST_DIRECTORY)

# 配置文档上传路径
UPLOAD_DIRECTORY = "uploads"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# 从环境变量获取API地址
EMBEDDING_API_BASE = os.getenv("EMBEDDING_API_BASE", "http://127.0.0.1:9997")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "None")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

# 初始化 embeddings
try:
    xinference = XinferenceEmbeddings(
        server_url="http://127.0.0.1:9997",
        model_uid="m3e-large"
    )
    # 测试 embedding 是否正常工作
    test_embedding = xinference.embed_query("This is a test query")
    print(f"Embedding service test successful. Vector dimension: {len(test_embedding)}")
except Exception as e:
    print(f"Error initializing embeddings: {str(e)}")
    raise

# 初始化 Chroma 客户端
client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)

# 初始化向量数据库
vectordb = Chroma(
    client=client,
    collection_name="knowledge_base",
    embedding_function=xinference,
)

# 初始化对话模型
llm = ChatOpenAI(
    model="deepseek-r1-distill-qwen",
    temperature=0.5,
    base_url="http://127.0.0.1:9997/v1",
    api_key="None"
)

class QueryRequest(BaseModel):
    query: str
    chat_history: Optional[List[tuple]] = []

@app.get("/knowledge_base/status")
async def get_knowledge_base_status():
    try:
        # 获取向量库中的所有文档数量
        collection = vectordb.get()
        doc_count = len(collection['ids']) if collection else 0
        
        # 获取已上传的文件列表
        uploaded_files = []
        if os.path.exists(UPLOAD_DIRECTORY):
            uploaded_files = os.listdir(UPLOAD_DIRECTORY)
        
        return {
            "document_count": doc_count,
            "uploaded_files": uploaded_files,
            "persist_directory": PERSIST_DIRECTORY
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/knowledge_base/clear")
async def clear_knowledge_base():
    try:
        global vectordb, client
        
        # 关闭现有连接
        client = None
        vectordb = None
        
        # 删除向量库
        if os.path.exists(PERSIST_DIRECTORY):
            shutil.rmtree(PERSIST_DIRECTORY)
            os.makedirs(PERSIST_DIRECTORY)
        
        # 删除上传的文件
        if os.path.exists(UPLOAD_DIRECTORY):
            shutil.rmtree(UPLOAD_DIRECTORY)
            os.makedirs(UPLOAD_DIRECTORY)
            
        # 重新初始化
        client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
        vectordb = Chroma(
            client=client,
            collection_name="knowledge_base",
            embedding_function=xinference,
        )
        
        return {"message": "Knowledge base cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def process_document(file_path: str):
    # 根据文件类型选择合适的加载器
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path, encoding='utf-8')
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    # 加载文档
    try:
        documents = loader.load()
    except UnicodeDecodeError:
        if file_path.endswith('.txt'):
            loader = TextLoader(file_path, encoding='gbk')
            documents = loader.load()
        else:
            raise
    
    # 优化分割策略：使用更小的块大小和重叠，以及按句子分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,  # 减小块大小以提高精确度
        chunk_overlap=100,  # 增加重叠以保持上下文
        length_function=len,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""]  # 优先按自然段落和句子分割
    )
    splits = text_splitter.split_documents(documents)

    # 将文档添加到向量库
    vectordb.add_documents(splits)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 检查文件类型
        if not file.filename.endswith(('.pdf', '.txt', '.docx')):
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # 保存文件
        file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 处理文档
        process_document(file_path)

        return {"message": "File uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
async def query_knowledge_base(request: QueryRequest):
    try:
        # 创建检索器，使用 MMR 搜索策略
        retriever = vectordb.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 5,
                "fetch_k": 10,
                "lambda_mult": 0.7
            }
        )

        # 构建更好的提示模板
        prompt_template = """请基于以下已知信息，简洁和准确地回答用户的问题。如果无法从中得到答案，请说 "抱歉，我在知识库中没有找到相关信息。"

已知信息：
{context}

用户问题：{question}

请注意：
1. 只使用已知信息中的内容来回答
2. 如果已知信息中没有相关内容，请直接说明
3. 不要编造或推测任何信息
4. 如果信息不完整，可以说明信息仅供参考

回答："""

        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # 创建检索链
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            chain_type="stuff",
            verbose=False,  # 关闭详细日志
            combine_docs_chain_kwargs={
                "prompt": PROMPT
            }
        )

        # 执行查询
        result = qa_chain.invoke({
            "question": request.query,
            "chat_history": request.chat_history
        })

        # 获取相关文档并计算相似度分数
        search_results = vectordb.similarity_search_with_score(
            request.query,
            k=5
        )
        
        # 过滤和处理结果
        filtered_results = []
        for doc, score in search_results:
            # 将分数归一化到 0-1 范围
            normalized_score = 1 / (1 + score)  # 使用距离的倒数作为相似度分数
            if normalized_score >= 0.5:  # 相似度阈值过滤
                filtered_results.append({
                    "content": doc.page_content,
                    "score": round(normalized_score, 3)  # 保留三位小数
                })

        return {
            "answer": result["answer"],
            "sources": filtered_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 