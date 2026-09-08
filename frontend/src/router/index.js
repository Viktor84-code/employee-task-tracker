import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import Dashboard from '../components/Dashboard.vue'
import TaskDetailView from '../views/TaskDetailView.vue'
import BusyView from '../views/BusyView.vue'
import ImportantView from '../views/ImportantView.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: LoginForm },
    { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
    { path: '/tasks/:id', component: TaskDetailView, meta: { requiresAuth: true } },
    { path: '/busy', component: BusyView, meta: { requiresAuth: true } },
    { path: '/important', component: ImportantView, meta: { requiresAuth: true } }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    next('/')
  } else if (to.path === '/' && authStore.token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
