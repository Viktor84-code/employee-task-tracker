<template>
  <div class="employees-view">
    <div class="page-header">
      <h1>Сотрудники</h1>
      <p class="subtitle">Все сотрудники команды</p>
    </div>

    <EmployeeList />

    <p v-if="store.error" class="error">{{ store.error }}</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import EmployeeList from '../components/EmployeeList.vue'

const store = useDataStore()

onMounted(() => {
  store.fetchEmployees()
})
</script>

<style scoped>
.employees-view {
  max-width: 800px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.error {
  margin-top: 24px;
  padding: 12px;
  background: var(--danger-bg);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-sm);
  color: var(--danger);
  font-size: 14px;
  text-align: center;
}
</style>