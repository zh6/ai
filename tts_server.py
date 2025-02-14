# coding:utf-8
import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ChatTTS
import torch
import torchaudio
import io

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化ChatTTS
chat = ChatTTS.Chat()
chat.load(compile=True)

class TTSRequest(BaseModel):
    text: str

class TTSResponse(BaseModel):
    code: int
    message: str
    data: str  # base64编码的音频数据

@app.post("/v1/tts/generate", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    try:
        # 生成语音
        wavs = chat.infer([request.text])
        wav = wavs[0]
        
        # 将音频数据转换为base64
        buffer = io.BytesIO()
        torchaudio.save(buffer, torch.from_numpy(wav).unsqueeze(0), 24000, format="wav")
        audio_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            'code': 10000,
            'message': 'success',
            'data': audio_base64
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'code': 50000,
                'message': str(e)
            }
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8809)