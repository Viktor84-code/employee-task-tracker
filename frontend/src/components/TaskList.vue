<template>
  <div class="task-list">
    <h2>Список задач</h2>
    <ul>
      <li v-for="task in tasks" :key="task.id">
        <strong>{{ task.title }}</strong>
        <span :class="task.status">{{ task.status }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const tasks = ref([])

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8003/api/tasks/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (response.ok) {
      tasks.value = await response.json()
    }
  } catch (e) {
    console.error('Ошибка при получении задач:', e)
  }
})
</script>

<style scoped>
.task-list {
  padding: 20px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.new {
  background: #f0f0f0;
}
.in_progress {
  background: #fff3cd;
}
.done {
  background: #d4edda;
}
</style>
