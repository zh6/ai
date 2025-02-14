# coding:utf-8
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from volcengine.visual.VisualService import VisualService
from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv

# 加载环境变量
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

# 初始化火山引擎视觉服务
visual_service = VisualService()
visual_service.set_ak(os.getenv('VOLCENGINE_ACCESS_KEY_ID'))
visual_service.set_sk(os.getenv('VOLCENGINE_SECRET_ACCESS_KEY'))

class LogoInfo(BaseModel):
    add_logo: bool = False
    position: int = 0
    language: int = 0
    opacity: float = 0.3
    logo_text_content: str = ''

class ImageRequest(BaseModel):
    req_key: str = 'high_aes_general_v20_L'
    prompt: str
    model_version: str = 'general_v2.0_L'
    req_schedule_conf: str = 'general_v20_9B_rephraser'
    seed: int = -1
    scale: float = 3.5
    ddim_steps: int = 16
    width: int = 1920
    height: int = 1080
    use_sr: bool = True
    return_url: bool = True
    logo_info: LogoInfo = LogoInfo()

class AlgorithmBaseResp(BaseModel):
    status_code: int
    status_message: str

class ImageResponseData(BaseModel):
    algorithm_base_resp: AlgorithmBaseResp
    binary_data_base64: List[str] = []
    image_urls: List[str] = []
    llm_result: str = ''
    pe_result: str = ''
    predict_tags_result: str = ''
    rephraser_result: str = ''
    request_id: str
    vlm_result: str = ''

class ImageResponse(BaseModel):
    code: int
    message: str
    data: ImageResponseData
    request_id: str
    status: int
    time_elapsed: str

@app.post("/v1/image/create", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    try:
        form = request.dict()
        response = visual_service.cv_process(form)
        
        return {
            'code': response.get('code', 10000),
            'message': response.get('message', 'success'),
            'data': {
                'algorithm_base_resp': {
                    'status_code': response.get('data', {}).get('algorithm_base_resp', {}).get('status_code', 0),
                    'status_message': response.get('data', {}).get('algorithm_base_resp', {}).get('status_message', 'success')
                },
                'binary_data_base64': response.get('data', {}).get('binary_data_base64', []),
                'image_urls': response.get('data', {}).get('image_urls', []),
                'llm_result': response.get('data', {}).get('llm_result', ''),
                'pe_result': response.get('data', {}).get('pe_result', ''),
                'predict_tags_result': response.get('data', {}).get('predict_tags_result', ''),
                'rephraser_result': response.get('data', {}).get('rephraser_result', ''),
                'request_id': response.get('data', {}).get('request_id', ''),
                'vlm_result': response.get('data', {}).get('vlm_result', '')
            },
            'request_id': response.get('request_id', ''),
            'status': response.get('status', 10000),
            'time_elapsed': response.get('time_elapsed', '')
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'code': 50000,
                'message': str(e),
                'data': {
                    'algorithm_base_resp': {
                        'status_code': 1,
                        'status_message': str(e)
                    }
                }
            }
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8808)