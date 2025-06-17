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
  // Просто перезагрузим страницу или сделаем переход
  // Например, если используешь Vue Router, можно вызвать router.back()
  window.history.back();
};

onMounted(() => {
  Search();
});
</script>

<template> <nav class="main-nav">
  <router-link to="/Memmarket" class="nav-link">Вернуть к выбору</router-link>
  </nav>
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

.main-nav {
  position: relative;
  display: flex;
  gap: 1.5rem;
  padding: 1rem 2rem;
  background: rgba(30, 30, 36, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.05);
  max-width: max-content;
  margin: 0 auto;
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

.nav-decoration {
  position: absolute;
  bottom: -5px;
  left: 0;
  height: 2px;
  background: linear-gradient(90deg, #4dabf7, #20c997);
  border-radius: 2px;
  transition: all 0.3s ease;
  z-index: 0;
}

.nav-link:hover::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 2px;
  background: #4dabf7;
  border-radius: 2px;
}

.nav-link.router-link-exact-active::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: calc(100% + 12px);
  height: calc(100% + 8px);
  border: 2px solid rgba(77, 171, 247, 0.3);
  border-radius: 10px;
  z-index: -1;
}

.main-nav {
  --glow-color: rgba(77, 171, 247, 0.1);
  box-shadow: 0 0 15px var(--glow-color), 
              0 4px 20px rgba(0, 0, 0, 0.3);
}
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
</style>
