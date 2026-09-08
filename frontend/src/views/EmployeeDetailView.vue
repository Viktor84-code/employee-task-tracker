<template>
  <div class="employee-detail">
    <div class="page-header">
      <button class="btn-back" @click="$router.back()">← Назад</button>
      <h1>Профиль сотрудника</h1>
    </div>

    <div v-if="employee.id" class="detail-card">
      <div class="detail-header">
        <div class="avatar">{{ initials(employee.full_name) }}</div>
        <div class="header-info">
          <h2>{{ employee.full_name }}</h2>
          <span class="position-badge">{{ employee.position }}</span>
        </div>
      </div>

      <div class="detail-grid">
        <div class="detail-field">
          <label>Email</label>
          <p class="field-value">{{ employee.email || 'Не указан' }}</p>
        </div>

        <div class="detail-field">
          <label>Дата приёма</label>
          <p class="field-value">{{ employee.hired_at || 'Не указана' }}</p>
        </div>
      </div>
    </div>

    <div class="tasks-section">
      <div class="section-header">
        <h3>Задачи сотрудника</h3>
        <span class="count">{{ assignedTasks.length }}</span>
      </div>

      <ul v-if="assignedTasks.length" class="task-list">
        <li
          v-for="task in assignedTasks"
          :key="task.id"
          class="task-item"
          @click="$router.push(`/tasks/${task.id}`)"
        >
          <div class="task-info">
            <span class="task-title">{{ task.title }}</span>
            <span class="task-due">Срок: {{ task.due_date }}</span>
          </div>
          <span :class="['status-dot', `dot-${task.status}`]">
            {{ statusLabel(task.status) }}
          </span>
        </li>
      </ul>

      <div v-else-if="employee.id" class="empty-state">
        <span class="empty-icon">🕐</span>
        <p>У сотрудника нет задач</p>
      </div>
    </div>

    <div v-if="!employee.id && !error" class="loading">
      <span class="spinner"></span>
      <p>Загрузка...</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch, TASK_API } from '../api'
import { useDataStore } from '../stores/data'

const route = useRoute()
const store = useDataStore()
const employee = ref({})
const error = ref('')

const assignedTasks = computed(() =>
  store.tasks.filter((t) => t.assignee === employee.value.id) || []
)

const initials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const statusLabel = (status) => {
  const labels = {
    new: 'Новая',
    in_progress: 'В работе',
    done: 'Завершена'
  }
  return labels[status] || status
}

const fetchEmployee = async () => {
  try {
    const [emp] = await Promise.all([
      apiFetch(TASK_API, `/api/employees/${route.params.id}/`),
      store.tasks.length ? Promise.resolve() : store.fetchTasks()
    ])
    employee.value = emp
  } catch (e) {
    error.value = e.message
  }
}

onMounted(fetchEmployee)
</script>

<style scoped>
.employee-detail {
  max-width: 800px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
}

.btn-back {
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  transition: all var(--transition);
}

.btn-back:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.detail-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 32px;
  margin-bottom: 24px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}

.avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 600;
  flex-shrink: 0;
}

.header-info h2 {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.position-badge {
  padding: 4px 12px;
  background: var(--accent-glow);
  color: var(--accent);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.detail-field label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.field-value {
  font-size: 15px;
  color: var(--text-primary);
  line-height: 1.5;
}

.tasks-section {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.section-header h3 {
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

.task-list {
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
  transition: background var(--transition);
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

.task-due {
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

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px;
  color: var(--text-secondary);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  margin-top: 16px;
  padding: 12px;
  background: var(--danger-bg);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-sm);
  color: var(--danger);
  font-size: 14px;
  text-align: center;
}
</style>