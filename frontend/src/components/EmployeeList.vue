<template>
  <div class="employee-list">
    <h2>Список сотрудников</h2>
    <ul>
      <li v-for="employee in employees" :key="employee.id">
        <strong>{{ employee.full_name }}</strong>
        <span>{{ employee.position }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const employees = ref([])

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8003/api/employees/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`
      }
    })
    if (response.ok) {
      employees.value = await response.json()
    }
  } catch (e) {
    console.error('Ошибка при получении сотрудников:', e)
  }
})
</script>

<style scoped>
.employee-list {
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
</style>
