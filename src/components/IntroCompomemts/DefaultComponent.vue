<script setup>
const siteName = 'dragled.ru'
</script>

<template>
  <section class="welcome-container">
    <h1 class="title">Добро пожаловать на {{ siteName }}!</h1>
    <p class="subtitle">Здесь ты найдёшь крутые проекты, статьи и разработки от DragLed 💻</p>
      <nav class="nav-wrapper">
    <router-link class="nav-link" to="/aboutMe">
      Коротко обо мне и проектах <b>*клик*</b>
    </router-link>
  </nav>
    <p class="subtitle">Надеюсь, тебе понравится!</p>
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
.nav-wrapper {
  padding: 1rem 2rem;
  text-align: center;
  background: linear-gradient(135deg, #1e3c72, #2a5298);
  border-radius: 1rem;
  margin: 2rem auto;
  max-width: 600px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25);
}

.nav-link {
  font-size: 1.2rem;
  font-weight: 600;
  color: beige;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.2s ease;
  cursor: pointer;
  user-select: none;
}

.nav-link b {
  font-weight: 700;
  color: #ffd966;
  margin-left: 0.3rem;
}

.nav-link:hover {
  color: #fffacd;
  transform: scale(1.05);
}

.nav-link:active {
  color: #f0e68c;
  transform: scale(0.98);
}


</style>
