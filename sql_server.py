from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Optional

# 加载环境变量
load_dotenv()

# 设置 DeepSeek API 客户端
# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com"
# )
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.siliconflow.cn"
)

app = FastAPI()

class NL2SQLRequest(BaseModel):
    query: str

class NL2SQLResponse(BaseModel):
    natural_language: str
    sql_query: str
    database_schema: str

def get_database_schema():
    """
    获取数据库结构信息
    这里需要根据实际情况实现，可以是静态定义或从数据库动态获取
    """
    return """
    表结构信息如下：
    1. users 表:
       - id (int): 用户ID
       - username (varchar): 用户名
       - email (varchar): 邮箱
       - created_at (datetime): 创建时间
    
    2. orders 表:
       - id (int): 订单ID
       - user_id (int): 用户ID，关联users表
       - total_amount (decimal): 订单总金额
       - status (varchar): 订单状态
       - created_at (datetime): 创建时间
    
    # 根据实际数据库添加更多表结构...
    """

@app.post("/api/nl2sql", response_model=NL2SQLResponse)
async def nl2sql(request: NL2SQLRequest):
    try:
        natural_language = request.query
        
        if not natural_language:
            raise HTTPException(status_code=400, detail="No query provided")
            
        # 获取数据库结构信息
        db_schema = get_database_schema()
        
        # 构建提示词
        prompt = f"""
        基于以下数据库结构信息，将自然语言转换为MySQL查询语句。
        
        {db_schema}
        
        请将以下自然语言转换为准确的MySQL查询语句，只使用上述定义的表和字段：
        {natural_language}
        
        注意：
        1. 只返回有效的SQL语句，不要包含任何其他解释
        2. 只使用上述数据库结构中定义的表和字段
        3. 确保生成的SQL语法正确且可执行
        """
        
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[
                {"role": "system", "content": "你是一个专业的SQL转换助手。你的任务是基于给定的数据库结构，将自然语言准确地转换为MySQL查询语句。只能使用提供的表和字段。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        # 获取生成的SQL
        sql_query = response.choices[0].message.content.strip()
        
        return NL2SQLResponse(
            natural_language=natural_language,
            sql_query=sql_query,
            database_schema=db_schema
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5003) 