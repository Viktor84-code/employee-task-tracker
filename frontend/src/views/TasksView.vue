<template>
  <div class="tasks-view">
    <div class="page-header">
      <h1>Задачи</h1>
      <p class="subtitle">Все задачи проекта</p>
    </div>

    <div class="tasks-grid">
      <div class="grid-section" v-if="store.tasks.length"><TaskList /></div>
      <div v-else class="empty-block">
        <span class="empty-icon">📝</span>
        <p>Нет задач</p>
      </div>
      <div class="grid-section"><TaskForm /></div>
    </div>

    <p v-if="store.error" class="error">{{ store.error }}</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import TaskList from '../components/TaskList.vue'
import TaskForm from '../components/TaskForm.vue'

const store = useDataStore()

onMounted(() => {
  store.fetchTasks()
})
</script>

<style scoped>
.tasks-view {
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

.tasks-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  align-items: start;
}

.grid-section {
  min-width: 0;
}

.empty-block {
  padding: 60px 20px;
  background: var(--bg-card);
  border: 1px dashed var(--border);
  border-radius: var(--radius);
  text-align: center;
  color: var(--text-muted);
}

.empty-icon {
  font-size: 40px;
  display: block;
  margin-bottom: 12px;
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

@media (max-width: 1000px) {
  .tasks-grid {
    grid-template-columns: 1fr;
  }
}
</style>