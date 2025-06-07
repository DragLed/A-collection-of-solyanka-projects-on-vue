<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const FavoriteMemes = ref(JSON.parse(localStorage.getItem('favoriteMemes') || '[]'));
const AllMemes = ref([]);

const Search = async () => {
  try {
    const response = await axios.get('https://api.imgflip.com/get_memes');
    AllMemes.value = response.data.data.memes;
  } catch (error) {
    console.error('Ошибка при загрузке мемов:', error);
  }
};

const toggleFavorite = (id) => {
  FavoriteMemes.value = FavoriteMemes.value.filter(memeId => memeId !== id);
  localStorage.setItem('favoriteMemes', JSON.stringify(FavoriteMemes.value));
};

const favoriteMemesList = computed(() => {
  return AllMemes.value.filter(meme => FavoriteMemes.value.includes(meme.id));
});

const goBack = () => {
  window.history.back();
};

onMounted(() => {
  Search();
});
</script>

<template>
   <div class="Router">
      <router-link to="/Memmarket" class="nav-link">Вернуться</router-link>
  </div>
  <div class="meme-list">
    <template v-if="favoriteMemesList.length > 0">
      <div class="meme-items" v-for="mem in favoriteMemesList" :key="mem.id">
        <div class="meme-item">
          <img class="meme-image" :src="mem.url" :alt="mem.name" />
          <h3>{{ mem.name }}</h3>
          <button @click="toggleFavorite(mem.id)"> 🗑 Удалить из избранного </button>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="empty-favorites">
        <p>Пока ничего нет в избранном.</p>
        <button @click="goBack">⬅ Вернуться назад</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.meme-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  padding: 20px;
  background-color: #121212;
  min-height: 300px;
}

.meme-items {
  flex: 1 1 200px;
  max-width: 220px;
}

.meme-item {
  background-color: #1e1e1e;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.6);
  padding: 12px;
  text-align: center;
  transition: transform 0.2s ease;
}

.meme-item:hover {
  transform: scale(1.05);
}

.meme-image {
  max-width: 100%;
  border-radius: 8px;
  margin-bottom: 8px;
  user-select: none;
}

h3 {
  color: #ffffff;
  font-size: 1rem;
  margin-bottom: 12px;
  overflow-wrap: break-word;
}

button {
  background-color: #ff3b3f;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 14px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
  user-select: none;
}

button:hover {
  background-color: #e03135;
}

button:active {
  transform: scale(0.95);
}

.empty-favorites {
  width: 100%;
  text-align: center;
  color: #ccc;
  font-size: 1.2rem;
}

.empty-favorites p {
  margin-bottom: 20px;
}

.nav-link {
  position: relative;
  text-decoration: none;
  color: #e0e0e0;
  font-weight: 500;
  font-size: 1.1rem;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
  z-index: 1;
  border-radius: 8px;
}

.nav-link:hover {
  color: #ffffff;
  background: rgba(60, 60, 70, 0.6);
}

.nav-link.router-link-exact-active {
  color: #4dabf7;
  font-weight: 600;
}

.Router {
  display: flex;
  text-align: center;
  justify-content: center;
  align-items: center;
}
.nav-link {
  display: inline-block;
  margin-bottom: 1.5rem;
  margin: 25px;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background: linear-gradient(145deg, #4dabf7, #1e90ff);
  box-shadow: 0 0 10px rgba(77, 171, 247, 0.6), 0 0 5px rgba(77, 171, 247, 0.3);
  text-decoration: none;
  transition: all 0.3s ease;
}
.nav-link:hover {
  background: linear-gradient(145deg, #63b3ff, #3598ff);
  box-shadow: 0 0 15px rgba(77, 171, 247, 0.8), 0 0 10px rgba(77, 171, 247, 0.4);
  transform: translateY(-2px);
}

</style>
