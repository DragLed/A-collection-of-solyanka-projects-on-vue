<script setup>
const aboutText = `Привет! Я — DragLed, Никита — фуллстек разработчик, увлечённый созданием удобных веб-приложений и интересных проектов. Мой опыт охватывает фронтенд и бэкенд, а мои проекты направлены на решение реальных задач и создание полезных инструментов. Ниже — мои ключевые работы.`

const projects = [
  {
    name: 'CityTravel',
    link: 'https://github.com/DragLed/CityTravel',
    description: `
      Веб-платформа для поиска и бронирования экскурсий с функциями создания маршрутов, поиска попутчиков и встроенного чата. 
      Реализован полный фронтенд на Vue.js с использованием Vue Router и интеграцией API для динамического получения данных. 
      Особенность — удобный UX, история посещений и поддержка карт для отображения локаций экскурсий. Идеально подходит для путешественников, желающих организовать свой досуг.
    `
  },
  {
    name: 'CatsFactImage',
    link: 'https://github.com/DragLed/CatsFactImage',
    description: `
      Минималистичное приложение, показывающее случайный факт про кошек вместе с картинкой. 
      Использует внешний API для получения фактов и изображений, реализовано на Vue.js. 
      Цель — создать лёгкий и приятный способ узнать что-то новое о кошках в один клик.
    `
  },
  {
    name: 'My-To-Do-List',
    link: 'https://github.com/DragLed/My-To-Do-List',
    description: `
      Классический таск-менеджер для организации дел и задач. 
      Позволяет добавлять, редактировать и удалять задачи с сохранением состояния в localStorage. 
      Простое и интуитивное приложение, сделанное на Vue.js, помогает эффективно управлять временем.
    `
  }
]
</script>

<template>
  <section class="about-section">
    <h2 class="section-title">Обо мне</h2>
    <p class="about-text">{{ aboutText }}</p>

    <h3 class="projects-title">Мои проекты</h3>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.name" class="project-item">
        <a :href="project.link" target="_blank" rel="noopener noreferrer" class="project-name">{{ project.name }}</a>
        <p class="project-description" v-html="project.description.trim().replace(/\n/g, '<br>')"></p>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.about-section {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #222;
  background-color: #f5f7fa;
  border-radius: 1rem;
  box-shadow: 0 6px 12px rgba(0,0,0,0.1);
}

.section-title {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
  color: #1e3c72;
}

.about-text {
  font-size: 1.125rem;
  line-height: 1.6;
  margin-bottom: 2rem;
  text-align: center;
}

.projects-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #345678;
}

.projects-list {
  list-style: none;
  padding: 0;
}

.project-item {
  margin-bottom: 1.75rem;
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 0.8rem;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.project-name {
  font-weight: 700;
  font-size: 1.25rem;
  color: #2a5298;
  text-decoration: none;
  transition: color 0.3s ease;
}

.project-name:hover {
  color: #1e3c72;
  text-decoration: underline;
}

.project-description {
  margin-top: 0.5rem;
  font-size: 1rem;
  color: #444;
  white-space: pre-line;
}
</style>
