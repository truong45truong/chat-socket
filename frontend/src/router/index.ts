import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/views/home/index.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login/index.vue')
    },
    {
      path: '/',
      name: 'home',
      component: HomePage ,
    },
  ]
})

export default router
