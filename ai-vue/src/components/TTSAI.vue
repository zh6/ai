<template>
  <div class="tts-container">
    <div class="tts-content">
      <div class="header">
        <h2>AI 语音助手</h2>
        <p class="subtitle">输入文字，让 AI 为你朗读</p>
      </div>
      
      <div class="text-input-container">
        <el-input
          v-model="text"
          type="textarea"
          :rows="4"
          placeholder="在这里输入你想要转换的文字..."
          :maxlength="500"
          show-word-limit
          resize="none"
          @keyup.enter.ctrl="generateAudio"
        />
        
        <div class="action-area">
          <span class="hint">提示：按下 Ctrl + Enter 快速生成</span>
          <el-button 
            type="primary" 
            :icon="Microphone" 
            @click="generateAudio" 
            :loading="loading"
            class="generate-btn"
            :disabled="!text.trim()"
          >
            {{ loading ? '生成中...' : '生成语音' }}
          </el-button>
        </div>
      </div>

      <transition name="fade">
        <div class="audio-player" v-if="audioSrc">
          <div class="player-container">
            <audio controls :src="audioSrc" class="audio-element"></audio>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Microphone } from '@element-plus/icons-vue'
import { generateSpeech } from '../services/ttsService'
import { ElMessage } from 'element-plus'

const text = ref('')
const loading = ref(false)
const audioSrc = ref('')

const generateAudio = async () => {
  if (!text.value.trim()) return

  loading.value = true
  try {
    const base64Audio = await generateSpeech(text.value.trim())
    audioSrc.value = `data:audio/wav;base64,${base64Audio}`
  } catch (error) {
    ElMessage.error('语音生成失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.tts-container {
  min-height: 100%;
  display: flex;
  justify-content: center;
  padding: 2rem;
  background-color: #f9fafb;
}

.tts-content {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.header {
  text-align: center;
  margin-bottom: 1rem;
}

.header h2 {
  font-size: 2rem;
  color: #1a1a1a;
  margin: 0;
  font-weight: 600;
}

.subtitle {
  color: #666;
  margin-top: 0.5rem;
  font-size: 1rem;
}

.text-input-container {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.text-input-container :deep(.el-textarea__inner) {
  border-radius: 8px;
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.text-input-container :deep(.el-textarea__inner:focus) {
  border-color: var(--el-color-primary);
  box-shadow: 0 0 0 2px rgba(var(--el-color-primary-rgb), 0.2);
}

.action-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.hint {
  color: #666;
  font-size: 0.875rem;
}

.generate-btn {
  padding: 12px 24px;
  font-size: 1rem;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.generate-btn:not(:disabled):hover {
  transform: translateY(-1px);
}

.audio-player {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.player-container {
  width: 100%;
}

.audio-element {
  width: 100%;
  height: 40px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .tts-container {
    padding: 1rem;
  }
  
  .action-area {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .hint {
    text-align: center;
  }
}
</style>