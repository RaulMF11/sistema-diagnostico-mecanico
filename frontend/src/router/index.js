import { createRouter, createWebHistory } from 'vue-router'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [],
// })

import DiagnosticoForm from '../components/DiagnosticoForm.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: DiagnosticoForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
