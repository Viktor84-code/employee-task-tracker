<template>
  <div class="task-list">
    <h2>Список задач</h2>
    <ul>
      <li
        v-for="task in store.filteredTasks"
        :key="task.id"
        :class="{ selected: store.selectedTaskId === task.id }"
        @click="store.selectTask(task.id)"
      >
        <div class="task-info">
          <strong>{{ task.title }}</strong>
          <span v-if="isImportant(task)" class="badge">Важная</span>
        </div>
        <span :class="['status', task.status]">{{ statusLabel(task.status) }}</span>
      </li>
    </ul>
    <p v-if="!store.loading && !store.filteredTasks.length">Задачи не найдены</p>

    <div v-if="store.selectedTask" class="details">
      <h3>Детали задачи</h3>
      <p><strong>Название:</strong> {{ store.selectedTask.title }}</p>
      <p><strong>Описание:</strong> {{ store.selectedTask.description || '—' }}</p>
      <p><strong>Исполнитель:</strong> {{ store.selectedTask.assignee_name || '—' }}</p>
      <p><strong>Срок:</strong> {{ store.selectedTask.due_date }}</p>
      <p><strong>Статус:</strong> {{ statusLabel(store.selectedTask.status) }}</p>
      <div class="status-actions">
        <button
          v-for="s in statuses"
          :key="s.value"
          :class="['status-btn', s.value, { active: store.selectedTask.status === s.value }]"
          :disabled="store.selectedTask.status === s.value"
          @click="changeStatus(s.value)"
        >
          {{ s.label }}
        </button>
      </div>
      <p v-if="store.error" class="error">{{ store.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDataStore } from '../stores/data'

const store = useDataStore()

const statuses = [
  { value: 'new', label: 'Новая' },
  { value: 'in_progress', label: 'В работе' },
  { value: 'done', label: 'Завершена' }
]

const importantTitles = computed(() => new Set(store.importantTasks.map((i) => i.task)))

const statusLabel = (value) => statuses.find((s) => s.value === value)?.label || value

const isImportant = (task) => importantTitles.value.has(task.title)

const changeStatus = async (status) => {
  await store.updateTaskStatus(store.selectedTask.id, status)
}

onMounted(() => {
  store.fetchTasks()
  store.fetchImportantTasks()
})
</script>

<style scoped>
.task-list {
  padding: 20px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s;
}
li:hover {
  background: #f5f5f5;
}
li.selected {
  background: #e7f7ef;
  border-color: #42b883;
}
.task-info {
  display: flex;
  align-items: center;
  gap: 8px;
}
.badge {
  background: #d9534f;
  color: white;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 8px;
}
.status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.new {
  background: #f0f0f0;
}
.in_progress {
  background: #fff3cd;
}
.done {
  background: #d4edda;
}
.details {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: left;
}
.status-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
.status-btn {
  padding: 6px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background: white;
  cursor: pointer;
}
.status-btn:hover:not(:disabled) {
  background: #f0f0f0;
}
.status-btn.active {
  border-color: #42b883;
  background: #42b883;
  color: white;
}
.status-btn:disabled {
  cursor: default;
}
.error {
  color: red;
}
</style>