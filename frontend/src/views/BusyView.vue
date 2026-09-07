<template>
  <div class="busy-view">
    <h2>Занятые сотрудники</h2>
    <ul>
      <li v-for="employee in store.busyEmployees" :key="employee.id">
        <strong>{{ employee.full_name }}</strong>
        <span>{{ employee.position }}</span>
      </li>
    </ul>
    <p v-if="!store.loading && !store.busyEmployees.length">Нет занятых сотрудников</p>
    <p v-if="store.error" class="error">{{ store.error }}</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

onMounted(() => {
  store.fetchBusyEmployees()
})
</script>

<style scoped>
.busy-view {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
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
.error {
  color: red;
}
</style>