<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';

const InputSearch = ref('');
const Memes = ref([]);
const IsSearch = ref(false);
const NoResults = ref(false);
const FavoriteMemes = ref(JSON.parse(localStorage.getItem('favoriteMemes') || '[]'));
const AllMemes = ref([]);

const SortFilter = ref('none'); // none | asc | desc
const LengthFilter = ref('all'); // all | short | medium | long
const PopularityFilter = ref('all'); // all | low | medium | high

const Search = async () => {
  try {
    const response = await axios.get('https://api.imgflip.com/get_memes');
    AllMemes.value = response.data.data.memes;
    filterMemes();
    IsSearch.value = true;
  } catch (error) {
    console.error('Ошибка при загрузке мемов:', error);
  }
};

const filterMemes = () => {
  let filtered = [];

  // Поиск по имени
  if (InputSearch.value) {
    filtered = AllMemes.value.filter(meme =>
      meme.name.toLowerCase().includes(InputSearch.value.toLowerCase())
    );
  } else {
    filtered = [...AllMemes.value];
  }

  // Фильтр по длине названия
  if (LengthFilter.value !== 'all') {
    filtered = filtered.filter(meme => {
      const len = meme.name.length;
      if (LengthFilter.value === 'short') return len < 10;
      if (LengthFilter.value === 'medium') return len >= 10 && len <= 15;
      if (LengthFilter.value === 'long') return len > 15;
      return true;
    });
  }

  // Фильтр по популярности (box_count)
  if (PopularityFilter.value !== 'all') {
    filtered = filtered.filter(meme => {
      const count = meme.box_count;
      if (PopularityFilter.value === 'low') return count <= 2;
      if (PopularityFilter.value === 'medium') return count > 2 && count <= 4;
      if (PopularityFilter.value === 'high') return count > 4;
      return true;
    });
  }

  // Сортировка
  if (SortFilter.value === 'asc') {
    filtered.sort((a, b) => a.name.localeCompare(b.name));
  } else if (SortFilter.value === 'desc') {
    filtered.sort((a, b) => b.name.localeCompare(a.name));
  }

  Memes.value = filtered;
  NoResults.value = Memes.value.length === 0;
};

watch([InputSearch, SortFilter, LengthFilter, PopularityFilter], filterMemes);

function toggleFavorite(id) {
  const index = FavoriteMemes.value.indexOf(id);
  if (index === -1) {
    FavoriteMemes.value.push(id);
  } else {
    FavoriteMemes.value.splice(index, 1);
  }
  localStorage.setItem('favoriteMemes', JSON.stringify(FavoriteMemes.value));
}

onMounted(() => {
  Search();
});
</script>

<template>
 <nav class="main-nav">
  <router-link to="Memmarket/favorites" class="nav-link">Избраное⭐️</router-link>
  </nav>
  <div class="maincomponent">
    <header class="main-header">
      <h1>МемМаркет</h1>
    </header>
    <div class="search">
      <input v-model="InputSearch" type="text" placeholder="Поиск мемов..." />
      
      <select v-model="SortFilter">
        <option value="none">Без сортировки</option>
        <option value="asc">По имени (А→Я)</option>
        <option value="desc">По имени (Я→А)</option>
      </select>

      <select v-model="LengthFilter">
        <option value="all">Длина названия: все</option>
        <option value="short">Короткие (&lt;10)</option>
        <option value="medium">Средние (10-15)</option>
        <option value="long">Длинные (&gt;15)</option>
      </select>

      <select v-model="PopularityFilter">
        <option value="all">Популярность: все</option>
        <option value="low">Низкая (≤2 текста)</option>
        <option value="medium">Средняя (3-4 текста)</option>
        <option value="high">Высокая (&gt;4 текста)</option>
      </select>

      <button @click="Search">Поиск мемов</button>
    </div>
    <div class="content">
      <div v-if="!IsSearch">
        <p>Загрузка...</p>
      </div>
      <div v-else>
        <p v-if="NoResults">По запросу "{{ InputSearch }}" ничего не найдено.</p>
        <div class="meme-list" v-else>
          <div class="meme-item" v-for="mem in Memes" :key="mem.id">
            <img class="meme-image" :src="mem.url" :alt="mem.name" />
            <h3>{{ mem.name }}</h3>
            <button
              :class="{ active: FavoriteMemes.includes(mem.id) }"
              @click="toggleFavorite(mem.id)"
            >
              {{ FavoriteMemes.includes(mem.id) ? '🗑 Удалить из избранного' : '💖 В избранное' }}
            </button>
          </div>
        </div>
      </div>
    </div>
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
.maincomponent {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #0e0e12;
  color: #ffffff;
  min-height: 100vh;
}

.main-header {
  margin-top: 2rem;
  font-size: 2rem;
  font-weight: bold;
  color: #3399ff;
  transition: color 0.3s ease;
}

.main-header:hover {
  color: #5fb0ff;
}

.search {
  display: flex;
  gap: 1rem;
  margin: 2rem 0;
  align-items: center;
}

input[type="text"] {
  background-color: #1e1e28;
  color: #e0e0e0;
  border: 1px solid #444;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  width: 250px;
  transition: all 0.2s ease;
}

input:focus {
  outline: none;
  border-color: #3399ff;
  box-shadow: 0 0 0 2px rgba(51, 153, 255, 0.3);
}

select {
  background-color: #1e1e28;
  color: #e0e0e0;
  border: 1px solid #444;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  width: 180px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
  font-weight: 500;
}

select:focus {
  outline: none;
  border-color: #3399ff;
  box-shadow: 0 0 0 2px rgba(51, 153, 255, 0.3);
}

select:hover {
  border-color: #5fb0ff;
  box-shadow: 0 0 5px rgba(95, 176, 255, 0.6);
}

button {
  background-color: #3399ff;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #2a85e0;
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 4px 12px rgba(51, 153, 255, 0.4);
}

button.active {
  background-color: #ff5c57;
  transition: all 0.3s ease;
}

button.active:hover {
  background-color: #e64b4b;
  transform: translateY(-2px) scale(1.02);
}

.meme-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
}

.meme-item {
  border: 1px solid #333;
  border-radius: 16px;
  background-color: #1a1a22;
  padding: 1rem;
  text-align: center;
  max-width: 220px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.meme-item:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.6);
}

.meme-image {
  width: 170px;
  height: auto;
  margin-bottom: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
  transition: transform 0.3s ease;
}

.meme-image:hover {
  transform: scale(1.1);
}

.content {
  margin-top: 1rem;
  padding-bottom: 2rem;
  width: 100%;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
