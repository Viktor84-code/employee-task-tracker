<template>
  <div class="container">
    <h1>Employee Task Tracker</h1>

    <button @click="showDashboard = !showDashboard">
      {{ showDashboard ? 'Выйти' : 'Войти' }}
    </button>

    <LoginForm v-if="!showDashboard" />
    <Dashboard v-else />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from './components/LoginForm.vue'
import Dashboard from './components/Dashboard.vue'
</script>

<style scoped>
.container {
  padding: 20px;
  text-align: center;
}
</style>
