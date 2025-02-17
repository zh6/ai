import { createRouter, createWebHistory } from 'vue-router'
import ChatAI from '../components/ChatAI.vue'
import ImageAI from '../components/ImageAI.vue'
import TTSAI from '../components/TTSAI.vue'
import SQLAI from '../components/SQLAI.vue'
import KnowledgeAI from '../components/KnowledgeAI.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/chat'
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatAI
    },
    {
      path: '/image',
      name: 'image',
      component: ImageAI
    },
    {
      path: '/tts',
      name: 'tts',
      component: TTSAI
    },
    {
      path: '/sql',
      name: 'SQL',
      component: SQLAI
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: KnowledgeAI
    }
  ]
})

export default router