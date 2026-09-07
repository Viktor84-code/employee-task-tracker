<template>
  <div class="container">
    <h1>Employee Task Tracker</h1>

    <!-- Компонент входа -->
    <LoginForm />
  </div>
</template>

<script setup>
import LoginForm from './components/LoginForm.vue'
</script>

<style scoped>
.container {
  padding: 20px;
  text-align: center;
}
</style>
