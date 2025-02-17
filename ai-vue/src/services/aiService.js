import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:9997/v1'
const API_KEY = 'sk-e77245df376b4c1a82a47141de27a560'

export const sendMessage = async (message, onChunk) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${API_KEY}`
      },
      body: JSON.stringify({
        model: 'deepseek-r1-distill-qwen',
        messages: [
          {role: 'system', content: 'You are a helpful assistant.'},
          {role: 'user', content: message}
        ],
        stream: true
      })
    })

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n').filter(line => line.trim() !== '')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const jsonStr = line.slice(6).trim()
          if (!jsonStr || jsonStr === '[DONE]') continue
          
          try {
            const parsed = JSON.parse(jsonStr)
            const content = parsed.choices?.[0]?.delta?.content
            if (content !== undefined) onChunk(content)
          } catch (e) {
            console.error('解析响应数据失败:', e, '原始数据:', jsonStr)
          }
        }
      }
    }
  } catch (error) {
    console.error('AI服务调用失败:', error)
    throw new Error('AI服务调用失败，请稍后重试')
  }
}

export const convertNL2SQL = async (query) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/nl2sql`, {
      query: query
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || '转换失败');
  }
};