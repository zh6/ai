<template>
  <div class="knowledge-container">
    <div class="knowledge-content">
      <div class="header">
        <h2>知识库问答</h2>
        <p class="subtitle">上传文档，让 AI 回答相关问题</p>
      </div>

      <!-- 文件上传区域 -->
      <div class="upload-section">
        <el-upload
          class="upload-area"
          :action="`${baseUrl}/upload`"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
          accept=".pdf,.txt,.docx"
          :limit="1"
        >
          <template #trigger>
            <el-button type="primary" :icon="Upload">上传文档</el-button>
          </template>
          <template #tip>
            <div class="el-upload__tip">
              支持 PDF、TXT、DOCX 格式文件
            </div>
          </template>
        </el-upload>
      </div>

      <!-- 聊天区域 -->
      <div class="chat-section">
        <div class="messages" ref="messagesContainer">
          <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
            <el-avatar 
              :size="40" 
              :icon="message.type === 'user' ? 'User' : 'Assistant'" 
              class="message-avatar" 
            />
            <div class="message-content">
              <template v-if="message.type === 'user'">
                {{ message.content }}
              </template>
              <template v-else>
                <div class="ai-response">
                  <div class="answer" v-html="formatMessage(message.content)"></div>
                  <div v-if="message.sources && message.sources.length" class="sources">
                    <div class="sources-title">参考来源：</div>
                    <div v-for="(source, idx) in message.sources" :key="idx" class="source-item">
                      {{ source }}
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="请输入您的问题..."
            @keyup.enter.ctrl="sendMessage"
            :disabled="loading"
          />
          <el-button 
            type="primary" 
            :icon="Position" 
            @click="sendMessage"
            :loading="loading"
            :disabled="!inputMessage.trim()"
          >
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Upload, Position } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const baseUrl = 'http://localhost:8002'
const inputMessage = ref('')
const loading = ref(false)
const messages = ref([
  { type: 'assistant', content: '您好！我是知识库助手，请上传文档后向我提问。' }
])
const messagesContainer = ref(null)
const chatHistory = ref([])

// 监听消息变化，自动滚动到底部
watch(messages, () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}, { deep: true })

// 格式化消息内容
const formatMessage = (content) => {
  if (!content) return ''
  return content
    .replace(/\n/g, '<br>')
    .replace(/\s/g, '&nbsp;')
}

// 上传前验证
const beforeUpload = (file) => {
  const validTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
  if (!validTypes.includes(file.type)) {
    ElMessage.error('只支持 PDF、TXT、DOCX 格式文件！')
    return false
  }
  return true
}

// 上传成功处理
const handleUploadSuccess = (response) => {
  ElMessage.success('文档上传成功！')
  messages.value.push({
    type: 'assistant',
    content: '文档已上传并处理完成，您可以开始提问了。'
  })
}

// 上传失败处理
const handleUploadError = (error) => {
  ElMessage.error('文档上传失败，请重试！')
  console.error('Upload error:', error)
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const question = inputMessage.value.trim()
  messages.value.push({ type: 'user', content: question })
  inputMessage.value = ''
  loading.value = true

  try {
    const response = await fetch(`${baseUrl}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: question,
        chat_history: chatHistory.value
      })
    })

    if (!response.ok) {
      throw new Error('请求失败')
    }

    const data = await response.json()
    messages.value.push({
      type: 'assistant',
      content: data.answer,
      sources: data.sources
    })

    // 更新聊天历史
    chatHistory.value.push([question, data.answer])
  } catch (error) {
    console.error('Query error:', error)
    ElMessage.error('请求失败，请重试！')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.knowledge-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px;
  background: var(--el-bg-color);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.knowledge-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header {
  text-align: center;
}

.header h2 {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
  background: linear-gradient(45deg, var(--el-color-primary) 0%, var(--el-color-success) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: var(--el-text-color-secondary);
  font-size: 16px;
}

.upload-section {
  padding: 20px;
  border-radius: 8px;
  background: var(--el-bg-color-page);
}

.chat-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 0;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: var(--el-bg-color-page);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-content {
  flex: 1;
  padding: 12px 16px;
  border-radius: 8px;
  max-width: 80%;
}

.user .message-content {
  background: var(--el-color-primary-light-9);
}

.assistant .message-content {
  background: var(--el-bg-color);
}

.ai-response {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sources {
  margin-top: 8px;
  font-size: 0.9em;
  color: var(--el-text-color-secondary);
}

.sources-title {
  font-weight: 500;
  margin-bottom: 4px;
}

.source-item {
  padding: 4px 8px;
  background: var(--el-bg-color-page);
  border-radius: 4px;
  margin-bottom: 4px;
}

.input-area {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.input-area .el-input {
  flex: 1;
}

.el-button {
  height: 40px;
}
</style> 