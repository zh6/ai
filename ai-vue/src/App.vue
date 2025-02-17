<script setup>
import { ChatDotRound, Picture, Microphone, DataAnalysis, Document } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'

const isLoaded = ref(false)

onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true
  }, 100)
})
</script>

<template>
  <div class="app-wrapper" :class="{ 'loaded': isLoaded }">
    <el-container class="layout">
      <el-header class="header">
        <div class="header-content">
          <div class="logo">
            <span class="logo-icon">🤖</span>
            <span class="logo-text">AI工具集</span>
          </div>
          <el-menu
            mode="horizontal"
            router
            :default-active="$route.path"
            class="menu"
          >
            <el-menu-item index="/chat">
              <el-icon><ChatDotRound /></el-icon>
              <span class="menu-text">智能问答</span>
            </el-menu-item>
            <el-menu-item index="/image">
              <el-icon><Picture /></el-icon>
              <span class="menu-text">AI绘图</span>
            </el-menu-item>
            <el-menu-item index="/tts">
              <el-icon><Microphone /></el-icon>
              <span>语音合成</span>
            </el-menu-item>
            <el-menu-item index="/sql">
              <el-icon><DataAnalysis /></el-icon>
              <span class="menu-text">SQL转换</span>
            </el-menu-item>
            <el-menu-item index="/knowledge">
              <el-icon><Document /></el-icon>
              <span>知识库问答</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade-transform" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>

      <el-footer class="footer">
        <div class="footer-content">
          <div class="footer-links">
            <a href="#" class="footer-link">关于我们</a>
            <span class="divider">|</span>
            <a href="#" class="footer-link">使用指南</a>
            <span class="divider">|</span>
            <a href="#" class="footer-link">联系支持</a>
          </div>
          <div class="copyright">
            AI Tools ©{{ new Date().getFullYear() }} Created with Element Plus
          </div>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<style scoped>
.app-wrapper {
  opacity: 0;
  transform: translateY(20px);
}

.app-wrapper.loaded {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7eb 100%);
}

.header {
  padding: 0;
  background: linear-gradient(90deg, var(--el-color-primary) 0%, var(--el-color-primary-light-3) 100%);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 100%;
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-right: 48px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 28px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.logo-text {
  font-size: 22px;
  font-weight: 600;
  background: linear-gradient(120deg, #fff 0%, rgba(255, 255, 255, 0.8) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.menu {
  flex: 1;
  background: transparent;
  border: none;
  display: flex;
  justify-content: center;
}

:deep(.el-menu--horizontal .el-menu-item) {
  height: 60px;
  line-height: 60px;
  margin: 0 8px;
  padding: 0 24px;
  font-size: 16px;
  color: rgba(255, 255, 255, 0.85);
  border-bottom: none;
  transition: all 0.3s ease;
}

:deep(.el-menu--horizontal .el-menu-item .el-icon) {
  font-size: 18px;
  margin-right: 8px;
  transition: transform 0.3s ease;
}

:deep(.el-menu--horizontal .el-menu-item:hover) {
  color: white;
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

:deep(.el-menu--horizontal .el-menu-item:hover .el-icon) {
  transform: scale(1.1);
}

:deep(.el-menu--horizontal .el-menu-item.is-active) {
  color: white;
  background: rgba(255, 255, 255, 0.15);
  font-weight: 500;
  position: relative;
}

:deep(.el-menu--horizontal .el-menu-item.is-active::after) {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background: white;
  border-radius: 3px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    width: 0;
    opacity: 0;
  }
  to {
    width: 30px;
    opacity: 1;
  }
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.footer {
  background: white;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.05);
  padding: 24px 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  text-align: center;
}

.footer-links {
  margin-bottom: 12px;
}

.footer-link {
  color: var(--el-text-color-regular);
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 14px;
}

.footer-link:hover {
  color: var(--el-color-primary);
}

.divider {
  margin: 0 12px;
  color: var(--el-border-color);
}

.copyright {
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

/* 路由切换动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.5s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
