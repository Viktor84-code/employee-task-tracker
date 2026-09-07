<template>
  <div class="task-form">
    <h2>Создать задачу</h2>
    <form @submit.prevent="handleCreate">
      <input v-model="title" type="text" placeholder="Название" required />
      <textarea v-model="description" placeholder="Описание"></textarea>
      <input v-model="due_date" type="date" required />
      <button type="submit">Создать</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
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

const handleCreate = async () => {
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
  } catch (e) {
    error.value = e.message
  }
}
</script>

<style scoped>
.task-form {
  padding: 20px;
}
input,
textarea {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}
button {
  width: 100%;
  padding: 10px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>