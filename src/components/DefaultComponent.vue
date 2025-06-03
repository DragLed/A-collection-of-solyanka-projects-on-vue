<script setup>
const siteName = 'dragled.ru'
</script>

<template>
  <section class="welcome-container">
    <h1 class="title">Добро пожаловать на {{ siteName }}!</h1>
    <p class="subtitle">Здесь ты найдёшь крутые проекты, статьи и разработки от DragLed 💻</p>
  </section>
</template>

<style scoped>
.welcome-container {
  padding: 2rem;
  text-align: center;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  color: white;
  border-radius: 1rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.25rem;
  color: #dce3f0;
}
</style>
