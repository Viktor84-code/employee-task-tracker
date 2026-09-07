<template>
  <div class="task-form">
    <h2>Создать задачу</h2>
    <form @submit.prevent="handleCreate">
      <input v-model="title" type="text" placeholder="Название" required />
      <textarea v-model="description" placeholder="Описание"></textarea>
      <input v-model="due_date" type="date" required />
      <button type="submit">Создать</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const title = ref('')
const description = ref('')
const due_date = ref('')
const error = ref('')

const handleCreate = async () => {
  try {
    const response = await fetch('http://localhost:8003/api/tasks/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify({
        title: title.value,
        description: description.value,
        due_date: due_date.value
      })
    })
    if (response.ok) {
      alert('Задача создана!')
      title.value = ''
      description.value = ''
      due_date.value = ''
    } else {
      error.value = 'Ошибка при создании задачи'
    }
  } catch (e) {
    error.value = 'Не удалось соединиться с сервером'
  }
}
</script>

<style scoped>
.task-form {
  padding: 20px;
}
input,
textarea {
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
  margin-top: 10px;
}
</style>
