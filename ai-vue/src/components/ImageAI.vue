<template>
  <div class="image-container">
    <h2 class="title">AI绘图</h2>
    <div class="image-content">
      <div class="prompt-input">
        <div class="input-wrapper">
          <el-input
            v-model="prompt"
            type="textarea"
            :rows="3"
            placeholder="请描述您想要生成的图片..."
            @keyup.enter.ctrl="generateImage"
            class="custom-input"
          />
          <div class="prompt-length" :class="{ 'warning': prompt.length > 200 }">
            {{ prompt.length }}/300
          </div>
        </div>
        <el-button 
          type="primary" 
          :icon="Picture" 
          @click="generateImage" 
          :loading="loading"
          class="generate-btn"
          :disabled="!prompt.trim() || prompt.length > 300"
        >
          生成图片
        </el-button>
      </div>

      <transition name="fade">
        <div class="image-result" v-if="imageUrl || loading || aiDescription">
          <transition name="bounce">
            <div v-if="loading" class="loading-container">
              <div class="loading-animation">
                <span v-for="(dot, index) in 3" :key="index" class="dot"></span>
              </div>
              <p>正在为您创作精美图片...</p>
              <div class="progress-bar">
                <div class="progress-inner"></div>
              </div>
            </div>
          </transition>

          <div v-if="!loading" class="result-wrapper">
            <transition name="scale">
              <el-image 
                v-if="imageUrl" 
                :src="imageUrl" 
                fit="contain"
                class="result-image"
                @load="handleImageLoad"
                @error="handleImageError"
              >
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                    <p>图片生成失败，请重试</p>
                  </div>
                </template>
              </el-image>
            </transition>
            
            <transition name="slide-up">
              <div v-if="aiDescription" class="image-description">
                <el-icon><ChatLineRound /></el-icon>
                <p>{{ aiDescription }}</p>
              </div>
            </transition>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Picture, Loading, ChatLineRound } from '@element-plus/icons-vue'
import { generateImage as generateAIImage } from '../services/imageService'
import { ElMessage } from 'element-plus'

const prompt = ref('')
const loading = ref(false)
const imageUrl = ref('')
const aiDescription = ref('')

const handleImageLoad = () => {
  ElMessage.success('图片生成成功！')
}

const handleImageError = () => {
  ElMessage.error('图片加载失败，请重试')
  imageUrl.value = ''
}

const generateImage = async () => {
  if (!prompt.value.trim()) return
  if (prompt.value.length > 300) {
    ElMessage.warning('提示文字不能超过300字')
    return
  }

  loading.value = true
  imageUrl.value = ''
  aiDescription.value = ''
  
  try {
    const response = await generateAIImage(prompt.value)
    console.log('Service Response:', response)
    
    if (response && response.imageUrl) {
      imageUrl.value = response.imageUrl
      aiDescription.value = response.data?.llm_result || response.data?.rephraser_result || ''
    } else {
      throw new Error('Invalid response format')
    }
  } catch (error) {
    console.error('Error generating image:', error)
    ElMessage.error(error.message || '图片生成失败，请稍后重试')
    imageUrl.value = ''
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.image-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 24px;
  background: linear-gradient(135deg, var(--el-bg-color) 0%, var(--el-bg-color-page) 100%);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.title {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 32px;
  text-align: center;
  background: linear-gradient(45deg, var(--el-color-primary) 0%, var(--el-color-success) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.image-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.prompt-input {
  display: flex;
  gap: 16px;
}

.input-wrapper {
  flex: 1;
  position: relative;
}

.custom-input {
  flex: 1;
  transition: all 0.3s ease;
}

.custom-input :deep(.el-textarea__inner) {
  border-radius: 12px;
  padding: 16px;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.custom-input :deep(.el-textarea__inner:focus) {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.prompt-length {
  position: absolute;
  right: 10px;
  bottom: 5px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  transition: all 0.3s ease;
}

.prompt-length.warning {
  color: var(--el-color-danger);
}

.generate-btn {
  padding: 0 32px;
  height: auto;
  border-radius: 12px;
  font-size: 16px;
  transition: all 0.3s ease;
}

.generate-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(var(--el-color-primary-rgb), 0.3);
}

.image-result {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--el-bg-color-page);
  border-radius: 16px;
  padding: 32px;
  min-height: 512px;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
}

.loading-container {
  text-align: center;
  color: var(--el-text-color-secondary);
}

.loading-animation {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-bottom: 16px;
}

.dot {
  width: 12px;
  height: 12px;
  background: var(--el-color-primary);
  border-radius: 50%;
  animation: bounce 0.5s infinite alternate;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  to { transform: translateY(-10px); }
}

.progress-bar {
  width: 200px;
  height: 4px;
  background: var(--el-border-color-lighter);
  border-radius: 2px;
  overflow: hidden;
  margin: 16px auto;
}

.progress-inner {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, var(--el-color-primary), var(--el-color-success));
  animation: progress 2s ease infinite;
  transform-origin: left;
}

@keyframes progress {
  0% { transform: scaleX(0); }
  50% { transform: scaleX(0.7); }
  100% { transform: scaleX(0.9); }
}

.result-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.result-image {
  max-width: 100%;
  max-height: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.image-error {
  text-align: center;
  color: var(--el-text-color-secondary);
}

.image-error .el-icon {
  font-size: 64px;
  margin-bottom: 16px;
  color: var(--el-color-danger);
}

.image-description {
  background: var(--el-bg-color);
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: flex-start;
  gap: 12px;
  max-width: 80%;
}

.image-description .el-icon {
  color: var(--el-color-primary);
  font-size: 20px;
  margin-top: 3px;
}

/* 动画效果 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.bounce-leave-active {
  animation: bounce-in 0.5s reverse;
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.5;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.5s ease;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.5s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>