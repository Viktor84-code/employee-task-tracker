<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>Главная</h1>
      <p class="subtitle">Управление сотрудниками и задачами</p>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon employees-icon">👥</div>
        <div class="stat-info">
          <span class="stat-value">{{ store.employees.length }}</span>
          <span class="stat-label">Сотрудников</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon tasks-icon">📝</div>
        <div class="stat-info">
          <span class="stat-value">{{ store.tasks.length }}</span>
          <span class="stat-label">Всего задач</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon progress-icon">🔄</div>
        <div class="stat-info">
          <span class="stat-value">{{ inProgressCount }}</span>
          <span class="stat-label">В работе</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon done-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ doneCount }}</span>
          <span class="stat-label">Завершено</span>
        </div>
      </div>
    </div>

    <div class="dashboard-grid">
      <div class="grid-section">
        <EmployeeList />
      </div>
      <div class="grid-section">
        <TaskList />
      </div>
      <div class="grid-section">
        <TaskForm />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDataStore } from '../stores/data'
import EmployeeList from './EmployeeList.vue'
import TaskList from './TaskList.vue'
import TaskForm from './TaskForm.vue'

const store = useDataStore()

const inProgressCount = computed(() => store.tasks.filter(t => t.status === 'in_progress').length)
const doneCount = computed(() => store.tasks.filter(t => t.status === 'done').length)

onMounted(() => {
  store.refresh()
})
</script>

<style scoped>
.dashboard {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  transition: all var(--transition);
}

.stat-card:hover {
  border-color: var(--border-focus);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.employees-icon { background: var(--info-bg); }
.tasks-icon { background: var(--accent-glow); }
.progress-icon { background: var(--warning-bg); }
.done-icon { background: var(--success-bg); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 24px;
}

.grid-section {
  min-width: 0;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
