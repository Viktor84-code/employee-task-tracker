<template>
  <div class="container">
    <h1>Employee Task Tracker</h1>

    <nav v-if="authStore.token" class="nav">
      <router-link to="/dashboard">Главная</router-link>
      <router-link to="/busy">Занятые сотрудники</router-link>
      <router-link to="/important">Важные задачи</router-link>
      <button class="logout" @click="handleLogout">Выход</button>
    </nav>

    <router-view />
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
.container {
  padding: 20px;
  text-align: center;
}
.nav {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin: 20px 0;
  align-items: center;
  flex-wrap: wrap;
}
.nav a {
  text-decoration: none;
  color: #42b883;
  font-weight: bold;
  padding: 6px 12px;
  border-radius: 4px;
}
.nav a.router-link-active {
  background: #42b883;
  color: white;
}
.logout {
  background: #d9534f;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  cursor: pointer;
}
</style>