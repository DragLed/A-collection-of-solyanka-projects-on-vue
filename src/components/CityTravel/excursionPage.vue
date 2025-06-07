<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const excursionId = parseInt(route.params.id);
const excursion = ref(null);
const HistoryList = ref([]);
const isLoading = ref(true);
const showAllSights = ref(false);
const weather = ref(null);
const error = ref('');

const API_KEY = '14cc090ee66620b128659eaa01ba47e4';

async function loadExcursionData() {
  isLoading.value = true;
  try {
    const response = await axios.get('/detailed_tours_20 (2).json');
    if (response.data && Array.isArray(response.data)) {
      excursion.value = response.data.find(item => item.id === excursionId) || null;
    }
  } catch (err) {
    console.error('Ошибка при загрузке экскурсии:', err);
  } finally {
    isLoading.value = false;
  }
  if (excursion.value && excursion.value.city) {
    try {
      const weatherResponse = await axios.get(
        `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
          excursion.value.city
        )}&units=metric&lang=ru&appid=${API_KEY}`
      );
      weather.value = weatherResponse.data;
      error.value = '';
    } catch (err) {
      weather.value = null;
      error.value = 'Город не найден. Проверьте правильность написания.';
    }
  }
}


function GoToTour(name, id, date) {
  const tourHistory = JSON.parse(localStorage.getItem('tourHistory')) || [];
  const existingTour = tourHistory.find(tour => tour.id === id);

  if (!existingTour) {
    tourHistory.push({ name, id, date });
    localStorage.setItem('tourHistory', JSON.stringify(tourHistory));
    showNotification(`Вы записались на "${name}"`, 'success');
  } else {
    showNotification(`Вы уже записаны на "${name}"`, 'info');
  }
  GetHistory();
}

function GetHistory() {
  HistoryList.value = JSON.parse(localStorage.getItem('tourHistory')) || [];
}

function showNotification(message, type = 'success') {
  const notification = document.createElement('div');
  notification.className = `notification ${type}`;
  notification.textContent = message;
  document.body.appendChild(notification);

  setTimeout(() => {
    notification.classList.add('fade-out');
    setTimeout(() => notification.remove(), 500);
  }, 3000);
}

function toggleSights() {
  showAllSights.value = !showAllSights.value;
}

onMounted(() => {
  loadExcursionData();
  GetHistory();
});
</script>


<template>
  <div class="excursion-page">
    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
      <p>Загрузка данных экскурсии...</p>
    </div>

    <div v-else-if="!excursion" class="error-message">
      <h2>Экскурсия не найдена</h2>
      <p>К сожалению, запрашиваемая экскурсия не существует или была удалена.</p>
      <router-link to="/" class="back-link">← Вернуться на главную</router-link>
    </div>

    <div v-else class="excursion-container">
      
      <div class="excursion-header">
        <h1>{{ excursion.title }}</h1>
        <div class="excursion-meta">
          <span class="meta-item">📍 {{ excursion.city }}</span>
          <span class="meta-item">📅 {{ excursion.date }}</span>
          <span class="meta-item">⏱️ {{ excursion.time_start }} - {{ excursion.time_end }}</span>
        </div>
      </div>

      <!-- <div class="excursion-gallery">
        <div class="main-image"></div>
        <div class="thumbnails">
          <div class="thumbnail" v-for="i in 3" :key="i"></div>
        </div>
      </div> -->

      <div class="excursion-content">
        <div class="content-section">
          <h2>Описание экскурсии</h2>
          <p class="short-description">{{ excursion.description }}</p>
          <p class="full-description">{{ excursion.full_description }}</p>
        </div>

        <div class="content-grid">
          <div class="info-card">
            <h3>Основная информация</h3>
            <ul class="info-list">
              <li><strong>Дистанция:</strong> {{ excursion.distance_km }} км</li>
              <li><strong>Цена:</strong> {{ excursion.price }} руб.</li>
              <li><strong>Транспорт:</strong> {{ excursion.transport }}</li>
            </ul>
          </div>

          <div class="info-card">
            <h3>Места</h3>
            <ul class="info-list">
              <li><strong>Место сбора:</strong> {{ excursion.arrival }}</li>
              <li><strong>Место отправления:</strong> {{ excursion.departure }}</li>
            </ul>
          </div>

          <div class="info-card">
            <h3>Погода</h3>
            <ul class="info-list" v-if="weather">
              <li>
                <h2 class="text-xl font-semibold">{{ weather.name }}</h2>
              </li>
              <li>
                <div class="flex items-center gap-4 mt-2">
                  <img :src="`https://openweathermap.org/img/wn/${weather.weather[0].icon}@2x.png`"
                    :alt="weather.weather[0].description" />
                  <div>
                    <span class="text-lg capitalize">{{ weather.weather[0].description }}  </span>
                    <span class="text-xl font-bold">+{{ Math.round(weather.main.temp) }}°C</span>
                  </div>
                </div>
              </li>
            </ul>
            <div v-else-if="error" class="text-red-500 mt-4">{{ error }}</div>
            <div v-else class="text-gray-500 mt-4">Загрузка погоды...</div>
          </div>

          <div class="info-card full-width" v-if="excursion.sights && excursion.sights.length">
            <h3>Достопримечательности <button @click="toggleSights" class="toggle-sights">
                {{ showAllSights ? 'Скрыть' : 'Показать все' }}
              </button></h3>
            <ul class="sights-list" :class="{ 'show-all': showAllSights }">
              <li v-for="(sight, index) in excursion.sights" :key="index">
                <span class="sight-number">{{ index + 1 }}.</span> {{ sight }}
              </li>
            </ul>
            <p class="sights-count">Всего объектов: {{ excursion.sights.length }}</p>
          </div>
        </div>

        <div class="action-section">
          <div class="price-tag">
            <span class="price">{{ excursion.price }} руб.</span>
            <span class="per-person">за человека</span>
          </div>
          <button @click="GoToTour(excursion.title, excursion.id, excursion.date)" class="book-button">
            Записаться на экскурсию
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.excursion-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
  color: #e0e0e0;
  font-family: 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background: #121212;
}

.excursion-header {
  margin-bottom: 20px;
}

.excursion-header h1 {
  font-size: 36px;
  margin: 0;
  font-weight: 700;
}

.excursion-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
  flex-wrap: wrap;
  color: #bbb;
  font-size: 14px;
}

.excursion-meta span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.excursion-description {
  font-size: 16px;
  line-height: 1.6;
  color: #ddd;
}

.sights-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  max-height: 350px;
  overflow-y: auto;
  background: #1e1e1e;
  padding: 10px;
  border-radius: 8px;
  color: #ccc;
}

.sights-list div {
  padding: 8px;
  border-bottom: 1px solid #333;
}

.price-tag {
  font-size: 28px;
  font-weight: 700;
  color: #4caf50;
  margin-bottom: 15px;
}

.action-section {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
  margin-top: 25px;
}

.book-button {
  background-color: #4caf50;
  color: #121212;
  border: none;
  padding: 12px 25px;
  font-size: 20px;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  user-select: none;
}

.book-button:hover {
  background-color: #43a047;
}

/* Адаптивность для телефонов */
@media (max-width: 600px) {
  .excursion-header h1 {
    font-size: 24px;
  }

  .excursion-meta {
    flex-direction: column;
    gap: 10px;
    font-size: 13px;
  }

  .content-grid {
    grid-template-columns: 1fr !important;
    gap: 20px;
  }

  .sights-list {
    grid-template-columns: 1fr !important;
    max-height: none !important;
    padding: 8px;
  }

  .price-tag {
    font-size: 20px;
  }

  .action-section {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .book-button {
    width: 100%;
    padding: 14px 20px;
    font-size: 18px;
    border-radius: 10px;
  }
}

</style>