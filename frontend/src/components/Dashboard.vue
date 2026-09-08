<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>Главная</h1>
      <p class="subtitle">Управление сотрудниками и задачами</p>
    </div>

    <div class="stats-grid">
      <router-link to="/employees" class="stat-card">
        <div class="stat-icon employees-icon">👥</div>
        <div class="stat-info">
          <span class="stat-value">{{ store.employees.length }}</span>
          <span class="stat-label">Сотрудников</span>
        </div>
        <span class="stat-arrow">→</span>
      </router-link>
      <router-link to="/tasks" class="stat-card">
        <div class="stat-icon tasks-icon">📝</div>
        <div class="stat-info">
          <span class="stat-value">{{ store.tasks.length }}</span>
          <span class="stat-label">Всего задач</span>
        </div>
        <span class="stat-arrow">→</span>
      </router-link>
      <router-link to="/tasks" class="stat-card">
        <div class="stat-icon progress-icon">🔄</div>
        <div class="stat-info">
          <span class="stat-value">{{ inProgressCount }}</span>
          <span class="stat-label">В работе</span>
        </div>
      </router-link>
      <router-link to="/tasks" class="stat-card">
        <div class="stat-icon done-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ doneCount }}</span>
          <span class="stat-label">Завершено</span>
        </div>
      </router-link>
    </div>

    <div class="quick-actions">
      <router-link to="/tasks" class="action-card">
        <span class="action-icon">📝</span>
        <span class="action-title">Задачи</span>
        <span class="action-desc">Просмотр и создание задач</span>
      </router-link>
      <router-link to="/employees" class="action-card">
        <span class="action-icon">👥</span>
        <span class="action-title">Сотрудники</span>
        <span class="action-desc">Список сотрудников команды</span>
      </router-link>
    </div>

    <p v-if="store.error" class="error">{{ store.error }}</p>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDataStore } from '../stores/data'

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
  text-decoration: none;
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
  flex-shrink: 0;
}

.employees-icon { background: var(--info-bg); }
.tasks-icon { background: var(--accent-glow); }
.progress-icon { background: var(--warning-bg); }
.done-icon { background: var(--success-bg); }

.stat-info {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
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

.stat-arrow {
  color: var(--text-muted);
  font-size: 18px;
  transition: transform var(--transition);
}

.stat-card:hover .stat-arrow {
  transform: translateX(4px);
  color: var(--accent);
}

.quick-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  max-width: 640px;
}

.action-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  text-decoration: none;
  transition: all var(--transition);
}

.action-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-icon {
  font-size: 28px;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.action-desc {
  font-size: 13px;
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

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .quick-actions {
    grid-template-columns: 1fr;
  }
}
</style>