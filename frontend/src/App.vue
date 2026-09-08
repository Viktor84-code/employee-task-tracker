<template>
  <div id="app">
    <nav v-if="authStore.token" class="navbar">
      <div class="nav-brand">
        <span class="brand-icon">📋</span>
        <span class="brand-text">TaskTracker</span>
      </div>
      <div class="nav-links">
        <router-link to="/dashboard" class="nav-link">
          <span class="nav-icon">🏠</span> Главная
        </router-link>
        <router-link to="/busy" class="nav-link">
          <span class="nav-icon">👥</span> Занятые
        </router-link>
        <router-link to="/important" class="nav-link">
          <span class="nav-icon">⭐</span> Важные
        </router-link>
      </div>
      <button class="btn-logout" @click="handleLogout">
        <span>Выйти</span>
      </button>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 64px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.brand-icon {
  font-size: 24px;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  transition: all var(--transition);
  text-decoration: none;
}

.nav-link:hover {
  background: var(--bg-card);
  color: var(--text-primary);
}

.nav-link.router-link-active {
  background: var(--accent);
  color: white;
  box-shadow: 0 0 16px var(--accent-glow);
}

.nav-icon {
  font-size: 16px;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border: 1px solid var(--danger);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--danger);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
}

.btn-logout:hover {
  background: var(--danger);
  color: white;
  box-shadow: 0 0 16px rgba(239, 68, 68, 0.3);
}

.main-content {
  flex: 1;
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}
</style>
