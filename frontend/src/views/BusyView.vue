<template>
  <div class="busy-view">
    <div class="page-header">
      <h1>Занятые сотрудники</h1>
      <p class="subtitle">Сотрудники, у которых есть активные задачи</p>
    </div>

    <div class="content-card">
      <ul v-if="store.busyEmployees.length">
        <li v-for="employee in store.busyEmployees" :key="employee.id" class="employee-item">
          <div class="avatar">{{ initials(employee.full_name) }}</div>
          <div class="employee-info">
            <span class="employee-name">{{ employee.full_name }}</span>
            <span class="employee-position">{{ employee.position }}</span>
          </div>
          <span class="busy-badge">Занят</span>
        </li>
      </ul>

      <div v-else class="empty-state">
        <span class="empty-icon">✅</span>
        <p>Нет занятых сотрудников</p>
      </div>

      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

const initials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

onMounted(() => {
  store.fetchBusyEmployees()
})
</script>

<style scoped>
.busy-view {
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

.content-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.employee-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
}

.employee-item:last-child {
  border-bottom: none;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--warning);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.employee-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.employee-name {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.employee-position {
  font-size: 13px;
  color: var(--text-muted);
}

.busy-badge {
  padding: 4px 12px;
  background: var(--warning-bg);
  color: var(--warning);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 40px;
  display: block;
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 15px;
}

.error {
  padding: 12px 24px;
  color: var(--danger);
  font-size: 14px;
}
</style>
