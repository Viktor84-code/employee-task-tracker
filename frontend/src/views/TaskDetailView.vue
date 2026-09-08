<template>
  <div class="task-detail">
    <div class="page-header">
      <button class="btn-back" @click="$router.back()">← Назад</button>
      <h1>Детали задачи</h1>
    </div>

    <div v-if="task.id" class="detail-card">
      <div class="detail-header">
        <h2>{{ task.title }}</h2>
        <span :class="['status-badge', `status-${task.status}`]">
          {{ statusLabel(task.status) }}
        </span>
      </div>

      <div class="detail-grid">
        <div class="detail-field">
          <label>Описание</label>
          <p class="field-value">{{ task.description || 'Нет описания' }}</p>
        </div>

        <div class="detail-field">
          <label>Исполнитель</label>
          <p class="field-value">{{ task.assignee_name || 'Не назначен' }}</p>
        </div>

        <div class="detail-field">
          <label>Срок</label>
          <p class="field-value">{{ task.due_date || 'Не указан' }}</p>
        </div>

        <div class="detail-field">
          <label>Статус</label>
          <p class="field-value">{{ statusLabel(task.status) }}</p>
        </div>
      </div>

      <div class="status-actions">
        <label>Изменить статус</label>
        <div class="status-buttons">
          <button
            :class="['btn-status', { active: task.status === 'new' }]"
            @click="changeStatus('new')"
          >
            🆕 Новая
          </button>
          <button
            :class="['btn-status', 'btn-progress', { active: task.status === 'in_progress' }]"
            @click="changeStatus('in_progress')"
          >
            🔄 В работе
          </button>
          <button
            :class="['btn-status', 'btn-done', { active: task.status === 'done' }]"
            @click="changeStatus('done')"
          >
            ✅ Завершена
          </button>
        </div>
      </div>
    </div>

    <div v-else class="loading">
      <span class="spinner"></span>
      <p>Загрузка...</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiFetch, TASK_API } from '../api'

const route = useRoute()
const task = ref({})
const error = ref('')

const statusLabel = (status) => {
  const labels = {
    new: 'Новая',
    in_progress: 'В работе',
    done: 'Завершена'
  }
  return labels[status] || status
}

const fetchTask = async () => {
  try {
    task.value = await apiFetch(TASK_API, `/api/tasks/${route.params.id}/`)
  } catch (e) {
    error.value = e.message
  }
}

const changeStatus = async (status) => {
  try {
    task.value = await apiFetch(TASK_API, `/api/tasks/${route.params.id}/`, {
      method: 'PATCH',
      body: { status }
    })
  } catch (e) {
    error.value = e.message
  }
}

onMounted(fetchTask)
</script>

<style scoped>
.task-detail {
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
}

.detail-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}

.detail-header h2 {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
}

.status-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.status-new {
  background: var(--info-bg);
  color: var(--info);
  border: 1px solid rgba(59, 130, 246, 0.3);
}

.status-in_progress {
  background: var(--warning-bg);
  color: var(--warning);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.status-done {
  background: var(--success-bg);
  color: var(--success);
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 32px;
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

.status-actions {
  padding-top: 24px;
  border-top: 1px solid var(--border);
}

.status-actions label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.status-buttons {
  display: flex;
  gap: 12px;
}

.btn-status {
  flex: 1;
  padding: 14px 20px;
  background: var(--bg-input);
  border: 2px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition);
}

.btn-status:hover {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-glow);
}

.btn-status.active {
  border-color: var(--accent);
  background: var(--accent);
  color: white;
}

.btn-progress.active {
  border-color: var(--warning);
  background: var(--warning);
}

.btn-done.active {
  border-color: var(--success);
  background: var(--success);
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
