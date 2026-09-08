<template>
  <div class="important-view">
    <div class="page-header">
      <h1>Важные задачи</h1>
      <p class="subtitle">Задачи, требующие особого внимания</p>
    </div>

    <div class="content-card">
      <ul v-if="store.importantTasks.length">
        <li v-for="item in store.importantTasks" :key="item.task" class="task-item">
          <div class="task-info">
            <span class="task-title">{{ item.task }}</span>
            <span class="task-due" v-if="item.due_date">Срок: {{ item.due_date }}</span>
          </div>
          <div class="employee-badges" v-if="item.employees && item.employees.length">
            <span
              v-for="name in item.employees"
              :key="name"
              class="employee-badge"
            >
              👤 {{ name }}
            </span>
          </div>
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
  gap: 16px;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border);
}

.task-item:last-child {
  border-bottom: none;
}

.task-info {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.task-title {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
}

.task-due {
  font-size: 12px;
  color: var(--text-muted);
}

.employee-badges {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 6px;
}

.employee-badge {
  padding: 4px 10px;
  background: var(--warning-bg);
  color: var(--warning);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
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
