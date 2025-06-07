<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';

const excursionList = ref([]);
const filteredExcursionList = ref([]);
const searchRequest = ref('');
const HistoryList = ref([]);
const isLoading = ref(false);
const router = useRouter();

async function Search() {
  isLoading.value = true;
  try {
    const response = await axios.get('/detailed_tours_20 (2).json');
    excursionList.value = response.data;

    if (searchRequest.value.toLowerCase() === 'test') {
      filteredExcursionList.value = [...excursionList.value];
    } else if (searchRequest.value) {
      filteredExcursionList.value = excursionList.value.filter(excursion =>
        excursion.title.toLowerCase().includes(searchRequest.value.toLowerCase())
      );
    } else {
      filteredExcursionList.value = [...excursionList.value]
        .sort(() => 0.5 - Math.random())
        .slice(0, 6);
    }
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  } finally {
    isLoading.value = false;
  }
}

function GetHistory() {
  HistoryList.value = JSON.parse(localStorage.getItem('tourHistory')) || [];
}

function GoToTour(id) {
  router.push({ name: 'excursion', params: { id } });
}

function deleteHistory(id) {
  const tourHistory = JSON.parse(localStorage.getItem('tourHistory')) || [];
  const updatedHistory = tourHistory.filter(tour => tour.id !== id);
  localStorage.setItem('tourHistory', JSON.stringify(updatedHistory));
  GetHistory();
}

function clearAllHistory() {
  if (confirm('Вы уверены, что хотите очистить всю историю?')) {
    localStorage.removeItem('tourHistory');
    GetHistory();
  }
}

onMounted(() => {
  Search();
  GetHistory();
});
</script>

<template>
  <div class="home-page">
    <div class="search-bar-container">
      <input 
        v-model="searchRequest" 
        @input="Search"
        @keyup.enter="Search"
        type="text" 
        placeholder="Поиск городов, экскурсий..."
        class="search-input"
      >
      <button @click="Search" class="search-button">
        <span class="button-text">Поиск</span>
        <span class="button-icon">🔍</span>
      </button>
    </div>

    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
    </div>

    <div v-else class="excursion-results-section">
      <div 
        v-for="excursion in filteredExcursionList" 
        :key="excursion.id"
        class="excursion-card"
        @click="GoToTour(excursion.id)"
      >
        <div class="card-image-placeholder">
          <span class="image-text">{{ excursion.city.charAt(0) }}</span>
        </div>
        <div class="card-content">
          <h3>{{ excursion.title }}</h3>
          <p class="description">{{ excursion.description }}</p>
          <div class="card-details">
            <span class="detail-item">🗓 {{ excursion.date }}</span>
            <span class="detail-item">💰 {{ excursion.price }}₽</span>
            <span class="detail-item">📍 {{ excursion.departure }}</span>
          </div>
          <div class="card-badge" v-if="excursion.price < 1000">Выгодно!</div>
        </div>
      </div>

      <div v-if="!filteredExcursionList.length" class="no-results">
        <p>По запросу "{{ searchRequest }}" ничего не найдено</p>
        <button @click="searchRequest = ''; Search()" class="reset-button">
          Сбросить поиск
        </button>
      </div>
    </div>

    <div class="history-section">
      <div class="history-header">
        <h4>История посещений</h4>
        <button 
          v-if="HistoryList.length" 
          @click="clearAllHistory"
          class="clear-history-button"
        >
          Очистить всё
        </button>
      </div>
      
      <div v-if="HistoryList.length" class="history-list">
        <div 
          v-for="History in HistoryList" 
          :key="History.id"
          class="history-item"
        >
          <div class="history-info" @click="GoToTour(History.id)">
            <div class="history-name">
              <span class="history-icon">📅</span>
              {{ History.name }}
            </div>
            <div class="history-meta">
              <span class="history-date">{{ History.date }}</span>
              <span class="history-id">ID: {{ History.id }}</span>
            </div>
          </div>
          <button 
            @click.stop="deleteHistory(History.id)"
            class="delete-button"
            title="Удалить из истории"
          >
            🗑️
          </button>
        </div>
      </div>
      
      <div v-else class="empty-history">
        <p>Вы пока не посещали экскурсий</p>
      </div>
    </div>
  </div>
</template>

<style scoped>

.MainForm {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    font-size: 18px;
    color: #e0e0e0;
    padding: 15px;
}

.TextForm {
    color: #a5d8ff;
    margin-bottom: 1.5rem;
}

.Image {
    background-color: rgba(40, 42, 54, 0.8);
    max-width: 600px;
    padding: 25px;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    text-align: center;
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    width: 100%;
    box-sizing: border-box;
}

.Image img {
    height: 300px;
    width: 300px;
    border-radius: 25px;
    border: 2px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transition: transform 0.3s ease;
    object-fit: cover;
}

.Image img:hover {
    transform: scale(1.02);
}

.ReloadBtn {
    background-color: #4dabf7;
    color: white;
    border: none;
    margin-top: 25px;
    border-radius: 8px;
    padding: 12px 25px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(77, 171, 247, 0.2);
}

.ReloadBtn:hover {
    background-color: #339af0;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(77, 171, 247, 0.3);
}

select {
    background-color: rgba(40, 42, 54, 0.8);
    color: #e0e0e0;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 8px 15px;
    margin-top: 1rem;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 200px;
    max-width: 100%;
    box-sizing: border-box;
}

select:hover {
    border-color: rgba(77, 171, 247, 0.5);
}

select:focus {
    outline: none;
    border-color: #4dabf7;
    box-shadow: 0 0 0 2px rgba(77, 171, 247, 0.2);
}

label {
    margin-right: 10px;
    color: #a5d8ff;
    font-size: 1rem;
}

/* Адаптив для телефонов */
@media (max-width: 480px) {
    .TextForm {
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }

    .Image img {
        width: 100%;
        height: auto;
        max-height: 300px;
        border-radius: 15px;
    }

    .ReloadBtn {
        width: 100%;
        padding: 14px 0;
        font-size: 1.1rem;
        margin-top: 15px;
        border-radius: 12px;
    }

    select {
        width: 100%;
        font-size: 1.1rem;
        padding: 10px 12px;
        margin-top: 1rem;
    }

    label {
        display: block;
        margin-bottom: 6px;
        font-size: 1.1rem;
    }
}

</style>