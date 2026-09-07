<template>
  <div class="employee-list">
    <h2>Список сотрудников</h2>
    <ul>
      <li
        v-for="employee in store.employees"
        :key="employee.id"
        :class="{ selected: store.selectedEmployeeId === employee.id }"
        @click="store.selectEmployee(employee.id)"
      >
        <strong>{{ employee.full_name }}</strong>
        <span>{{ employee.position }}</span>
      </li>
    </ul>
    <p v-if="!store.loading && !store.employees.length">Сотрудники не найдены</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

onMounted(() => {
  store.fetchEmployees()
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
  cursor: pointer;
  transition: background 0.2s;
}
li:hover {
  background: #f5f5f5;
}
li.selected {
  background: #42b883;
  color: white;
  border-color: #42b883;
}
</style>