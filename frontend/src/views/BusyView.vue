<template>
  <div class="busy-view">
    <div class="page-header">
      <h1>Занятые сотрудники</h1>
      <p class="subtitle">Сотрудники, у которых есть активные задачи</p>
    </div>

    <div class="content-card">
      <ul v-if="busyEmployees.length">
        <li v-for="employee in busyEmployees" :key="employee.id" class="employee-item">
          <div class="avatar">{{ initials(employee.full_name) }}</div>
          <div class="employee-info">
            <span class="employee-name">{{ employee.full_name }}</span>
            <span class="employee-position">{{ employee.position }}</span>
            <ul v-if="employee.active_tasks && employee.active_tasks.length" class="task-list">
              <li v-for="task in employee.active_tasks" :key="task.id" class="task-item">
                <span class="task-title">{{ task.title }}</span>
                <span :class="['status-dot', `dot-${task.status}`]">
                  {{ statusLabel(task.status) }}
                </span>
              </li>
            </ul>
          </div>
          <span class="busy-badge">Занят ({{ employee.active_tasks_count }})</span>
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
import { computed, onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

// только те, у кого реально есть активные задачи
const busyEmployees = computed(() =>
  (store.busyEmployees || []).filter(e => (e.active_tasks_count || 0) > 0)
)

const initials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const statusLabel = (status) => {
  const labels = { new: 'Новая', in_progress: 'В работе', done: 'Завершена' }
  return labels[status] || status
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

.task-list {
  list-style: none;
  padding: 6px 0 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  font-size: 12px;
  color: var(--text-secondary);
}

.task-title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 320px;
}

.status-dot {
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 10px;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.dot-new {
  background: var(--info-bg);
  color: var(--info);
}

.dot-in_progress {
  background: var(--warning-bg);
  color: var(--warning);
}

.dot-done {
  background: var(--success-bg);
  color: var(--success);
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
