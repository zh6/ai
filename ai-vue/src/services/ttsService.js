import axios from 'axios'

// 根据环境使用不同的 API 地址
const API_URL = process.env.NODE_ENV === 'development' 
  ? 'http://localhost:5000'  // 开发环境使用本地服务器
  : window.location.hostname === 'localhost'
    ? 'http://localhost:5000'  // 本地生产环境
    : `http://${window.location.hostname}:5000`  // 远程生产环境

export const generateSpeech = async (text) => {
  try {
    const response = await axios.post(`${API_URL}/tts`, { text })
    return response.data
  } catch (error) {
    console.error('Error generating speech:', error)
    throw error
  }
}