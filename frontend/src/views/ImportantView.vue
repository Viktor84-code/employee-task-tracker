<template>
  <div class="important-view">
    <h2>Важные задачи</h2>
    <ul>
      <li v-for="task in store.importantTasks" :key="task.id">
        <strong>{{ task.title }}</strong>
        <span :class="task.status">{{ task.status }}</span>
      </li>
    </ul>
    <p v-if="!store.loading && !store.importantTasks.length">Нет важных задач</p>
    <p v-if="store.error" class="error">{{ store.error }}</p>
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
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
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
.error {
  color: red;
}
</style>