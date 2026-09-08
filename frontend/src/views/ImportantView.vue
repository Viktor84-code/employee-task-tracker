<template>
  <div class="important-view">
    <div class="page-header">
      <h1>Важные задачи</h1>
      <p class="subtitle">Задачи, требующие особого внимания</p>
    </div>

    <div class="content-card">
      <ul v-if="store.importantTasks.length">
        <li v-for="task in store.importantTasks" :key="task.id" class="task-item">
          <div class="task-info">
            <span class="task-title">{{ task.title }}</span>
          </div>
          <span :class="['status-badge', `status-${task.status}`]">
            {{ statusLabel(task.status) }}
          </span>
        </li>
      </ul>

      <div v-else class="empty-state">
        <span class="empty-icon">⭐</span>
        <p>Нет важных задач</p>
      </div>

      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

const statusLabel = (status) => {
  const labels = { new: 'Новая', in_progress: 'В работе', done: 'Завершена' }
  return labels[status] || status
}

onMounted(() => {
  store.fetchImportantTasks()
})
</script>

<style scoped>
.important-view {
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

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
}

.task-item:last-child {
  border-bottom: none;
}

.task-info {
  min-width: 0;
}

.task-title {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  margin-left: 16px;
  flex-shrink: 0;
}

.status-new {
  background: var(--info-bg);
  color: var(--info);
}

.status-in_progress {
  background: var(--warning-bg);
  color: var(--warning);
}

.status-done {
  background: var(--success-bg);
  color: var(--success);
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
