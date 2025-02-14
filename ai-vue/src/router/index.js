import { createRouter, createWebHistory } from 'vue-router'
import ChatAI from '../components/ChatAI.vue'
import ImageAI from '../components/ImageAI.vue'
import TTSAI from '../components/TTSAI.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/chat'
    },
    {
      path: '/chat',
      component: ChatAI
    },
    {
      path: '/image',
      component: ImageAI
    },
    {
      path: '/tts',
      component: TTSAI
    }
  ]
})

export default router