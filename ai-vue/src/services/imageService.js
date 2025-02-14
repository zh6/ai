import axios from 'axios'

// 根据环境使用不同的 API 地址
const API_URL = process.env.NODE_ENV === 'development' 
  ? 'http://localhost:8808'  // 开发环境使用本地服务器
  : window.location.hostname === 'localhost'
    ? 'http://localhost:8808'  // 本地生产环境
    : `http://${window.location.hostname}:8808`  // 远程生产环境

export const generateImage = async (prompt) => {
  try {
    const response = await axios.post(`${API_URL}/v1/image/create`, {
      prompt,
      width: 1024,
      height: 1024
    })
    return response.data
  } catch (error) {
    console.error('Error generating image:', error)
    throw error
  }
}