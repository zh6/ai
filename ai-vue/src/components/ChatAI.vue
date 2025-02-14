<template>
  <div class="chat-container">
    <h2 class="chat-title">智能问答</h2>
    <div class="chat-content">
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
          <el-avatar :size="40" :icon="message.type === 'user' ? 'User' : 'Assistant'" class="message-avatar" />
          <div class="message-content">
            <div v-if="message.type === 'user'">{{ message.content }}</div>
            <div v-else class="assistant-message" v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>
      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="请输入您的问题..."
          @keyup.enter.ctrl="sendMessage"
          class="custom-input"
        />
        <el-button type="primary" :icon="Promotion" @click="sendMessage" :loading="loading" class="send-button">
          发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Promotion } from '@element-plus/icons-vue'
import { sendMessage as sendAIMessage } from '../services/aiService'

const inputMessage = ref('')
const loading = ref(false)
const messages = ref([
  { type: 'assistant', content: '你好！我是AI助手，有什么可以帮助你的吗？' }
])
const messagesContainer = ref(null)

// 监听消息列表变化，自动滚动到底部
watch(messages, () => {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
})

// 格式化消息内容，处理换行和特殊字符
const formatMessage = (content) => {
  if (!content) return ''
  return content
    .replace(/\n/g, '<br>')
    .replace(/\s/g, '&nbsp;')
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({ type: 'user', content: userMessage })
  inputMessage.value = ''
  loading.value = true

  try {
    // 创建一个新的响应式消息对象
    const assistantMessage = { type: 'assistant', content: '' }
    const messageIndex = messages.value.length
    messages.value.push(assistantMessage)

    await sendAIMessage(userMessage, (content) => {
      // 直接更新消息内容
      assistantMessage.content += content
      // 强制更新消息数组以触发视图更新
      messages.value[messageIndex] = { ...assistantMessage }
    })
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value.push({ type: 'assistant', content: '抱歉，我遇到了一些问题，请稍后再试。' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.chat-title {
  font-size: 24px;
  color: var(--el-color-primary);
  margin-bottom: 24px;
  text-align: center;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: calc(100vh - 250px);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.05);
}

.message {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.message-avatar:hover {
  transform: scale(1.05);
}

.message-content {
  max-width: 70%;
  padding: 16px 20px;
  border-radius: 12px;
  position: relative;
  transition: transform 0.2s ease;
}

.message.user .message-content {
  background: var(--el-color-primary-light-8);
  color: var(--el-color-primary-dark-2);
  box-shadow: 0 4px 12px rgba(var(--el-color-primary-rgb), 0.1);
}

.message.assistant .message-content {
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.assistant-message {
  line-height: 1.6;
  white-space: pre-wrap;
}

.message-content:hover {
  transform: translateY(-2px);
}

.chat-input {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.custom-input {
  flex: 1;
}

.custom-input :deep(.el-textarea__inner) {
  border-radius: 8px;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.custom-input :deep(.el-textarea__inner:focus) {
  border-color: var(--el-color-primary);
  box-shadow: 0 2px 8px rgba(var(--el-color-primary-rgb), 0.2);
}

.send-button {
  padding: 12px 24px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(var(--el-color-primary-rgb), 0.2);
}

.send-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--el-color-primary-rgb), 0.3);
}

.send-button:active {
  transform: translateY(0);
}
</style>