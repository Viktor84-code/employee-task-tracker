<template>
  <div class="dashboard">
    <h2>Главная</h2>

    <div class="dashboard-grid">
      <EmployeeList />
      <TaskList />
      <TaskForm />
    </div>
  </div>
</template>

<script setup>
import EmployeeList from './EmployeeList.vue'
import TaskList from './TaskList.vue'
import TaskForm from './TaskForm.vue'
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 20px;
}
</style>
