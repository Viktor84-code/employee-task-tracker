<template>
  <div class="employee-list card">
    <div class="card-header">
      <h2>Сотрудники</h2>
      <span class="count">{{ store.employees.length }}</span>
    </div>

    <ul v-if="store.employees.length">
      <li
        v-for="employee in store.employees"
        :key="employee.id"
        :class="['employee-item', { selected: store.selectedEmployeeId === employee.id }]"
        @click="store.selectEmployee(employee.id)"
      >
        <div class="avatar">{{ initials(employee.full_name) }}</div>
        <div class="employee-info">
          <span class="employee-name">{{ employee.full_name }}</span>
          <span class="employee-position">{{ employee.position }}</span>
        </div>
      </li>
    </ul>

    <div v-else class="empty-state">
      <span class="empty-icon">👥</span>
      <p>Нет сотрудников</p>
    </div>
  </div>
</template>

<script setup>
import { useDataStore } from '../stores/data'

const store = useDataStore()

const initials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
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

.employee-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: all var(--transition);
}

.employee-item:last-child {
  border-bottom: none;
}

.employee-item:hover {
  background: var(--bg-card-hover);
}

.employee-item.selected {
  background: rgba(99, 102, 241, 0.1);
  border-left: 3px solid var(--accent);
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.employee-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.employee-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.employee-position {
  font-size: 12px;
  color: var(--text-muted);
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
