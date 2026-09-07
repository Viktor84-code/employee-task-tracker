<template>
  <div class="login-form">
    <h2>Вход</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" type="text" placeholder="Логин" required />
      <input v-model="password" type="password" placeholder="Пароль" required />
      <button type="submit">Войти</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    const response = await fetch('http://localhost:8002/api/auth/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    const data = await response.json()
    if (response.ok) {
      authStore.setToken(data.access)
      router.push('/dashboard')
    } else {
      error.value = data.detail || 'Ошибка входа'
    }
  } catch (e) {
    error.value = 'Не удалось соединиться с сервером'
  }
}
</script>

<style scoped>
.login-form {
  max-width: 300px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}
button {
  width: 100%;
  padding: 10px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
}
.error {
  color: red;
}
</style>