<template>
  <div class="task-form card">
    <div class="card-header">
      <h2>Создать задачу</h2>
    </div>

    <form @submit.prevent="handleCreate" class="form-body">
      <div class="form-group">
        <label for="title">Название</label>
        <input
          id="title"
          v-model="title"
          type="text"
          placeholder="Введите название задачи"
          required
        />
      </div>

      <div class="form-group">
        <label for="description">Описание</label>
        <textarea
          id="description"
          v-model="description"
          placeholder="Описание задачи (необязательно)"
          rows="3"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="due_date">Срок</label>
        <input
          id="due_date"
          v-model="due_date"
          type="date"
          required
        />
      </div>

      <button type="submit" class="btn-create" :disabled="loading">
        {{ loading ? 'Создание...' : 'Создать задачу' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">Задача создана!</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()
const title = ref('')
const description = ref('')
const due_date = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

const handleCreate = async () => {
  loading.value = true
  error.value = ''
  success.value = false
  try {
    await store.createTask({
      title: title.value,
      description: description.value,
      due_date: due_date.value,
      assignee: store.selectedEmployeeId || null
    })
    title.value = ''
    description.value = ''
    due_date.value = ''
    success.value = true
    setTimeout(() => { success.value = false }, 2000)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
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
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.card-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.form-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 14px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 14px;
  transition: all var(--transition);
  outline: none;
  font-family: inherit;
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px var(--accent-glow);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--text-muted);
}

.btn-create {
  width: 100%;
  padding: 12px;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition);
}

.btn-create:hover:not(:disabled) {
  background: var(--accent-hover);
  box-shadow: 0 0 16px var(--accent-glow);
}

.btn-create:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  margin-top: 12px;
  padding: 10px;
  background: var(--danger-bg);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--radius-sm);
  color: var(--danger);
  font-size: 13px;
  text-align: center;
}

.success {
  margin-top: 12px;
  padding: 10px;
  background: var(--success-bg);
  border: 1px solid rgba(34, 197, 94, 0.3);
  border-radius: var(--radius-sm);
  color: var(--success);
  font-size: 13px;
  text-align: center;
}
</style>