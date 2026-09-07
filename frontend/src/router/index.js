import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginForm from '../components/LoginForm.vue'
import Dashboard from '../components/Dashboard.vue'
import BusyView from '../views/BusyView.vue'
import ImportantView from '../views/ImportantView.vue'

const routes = [
  { path: '/', name: 'login', component: LoginForm },
  { path: '/dashboard', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/busy', name: 'busy', component: BusyView, meta: { requiresAuth: true } },
  { path: '/important', name: 'important', component: ImportantView, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.token) {
    return { name: 'login' }
  }
})

export default router