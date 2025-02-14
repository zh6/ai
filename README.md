# AI Web 应用

这是一个集成了多个 AI 功能的 Web 应用，包括：
- 文字转语音
- AI 图片生成
- AI 聊天

## 项目结构

```
.
├── ai-vue/          # 前端 Vue 项目
├── server.py        # 图片生成服务
├── tts_server.py    # 语音合成服务
└── requirements.txt # Python 依赖
```

## 环境要求

- Node.js 16+
- Python 3.8+
- 火山引擎 API 密钥

## 安装和运行

1. 安装前端依赖
```bash
cd ai-vue
npm install
```

2. 安装后端依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
创建 `.env` 文件并添加以下内容：
```
VOLCENGINE_ACCESS_KEY_ID=your_access_key_id
VOLCENGINE_SECRET_ACCESS_KEY=your_secret_access_key
```

4. 运行服务
```bash
# 运行前端开发服务器
cd ai-vue
npm run dev

# 运行后端服务器（需要新开终端）
python server.py    # 图片生成服务
python tts_server.py # 语音服务
```

## 部署说明

- 前端已部署到 Vercel
- 后端需要在本地运行，确保模型文件在 `asset` 目录下 