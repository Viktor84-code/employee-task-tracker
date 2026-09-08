<template>
  <div class="task-list card">
    <div class="card-header">
      <h2>Список задач</h2>
      <span class="count">{{ filteredTasks.length }}</span>
    </div>

    <ul v-if="filteredTasks.length">
      <li
        v-for="task in filteredTasks"
        :key="task.id"
        class="task-item"
        @click="goToTask(task.id)"
      >
        <div class="task-info">
          <span class="task-title">{{ task.title }}</span>
          <span class="task-assignee" v-if="task.assignee_name">{{ task.assignee_name }}</span>
        </div>
        <span :class="['status-dot', `dot-${task.status}`]">
          {{ statusLabel(task.status) }}
        </span>
      </li>
    </ul>

    <div v-else class="empty-state">
      <span class="empty-icon">📝</span>
      <p>Нет задач</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'

const store = useDataStore()
const router = useRouter()

const filteredTasks = computed(() => store.filteredTasks)

const statusLabel = (status) => {
  const labels = { new: 'Новая', in_progress: 'В работе', done: 'Завершена' }
  return labels[status] || status
}

const goToTask = (id) => {
  router.push(`/tasks/${id}`)
}
</script>

<style scoped>
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.card-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.count {
  padding: 2px 10px;
  background: var(--bg-input);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
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
  padding: 14px 24px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: all var(--transition);
}

.task-item:last-child {
  border-bottom: none;
}

.task-item:hover {
  background: var(--bg-card-hover);
}

.task-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.task-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.task-assignee {
  font-size: 12px;
  color: var(--text-muted);
}

.status-dot {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
  margin-left: 12px;
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

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 32px;
  display: block;
  margin-bottom: 8px;
}

.empty-state p {
  font-size: 14px;
}
</style>
