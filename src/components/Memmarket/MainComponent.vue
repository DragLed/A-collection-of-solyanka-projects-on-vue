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
   <div class="Router">
      
  </div>
  <div class="maincomponent">
    <header class="main-header">
      <h1>МемМаркет</h1>
    </header>
    <router-link to="/Memmarket/favorites" class="nav-link">Избранное</router-link>
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

@media (max-width: 768px) {
  .search {
    flex-direction: column;
    gap: 0.8rem;
    align-items: stretch;
    width: 90%;
    margin: 1rem auto 2rem;
  }

  input[type="text"],
  select,
  button {
    width: 100%;
    font-size: 1.1rem;
  }

  .meme-list {
    flex-direction: column;
    gap: 1.5rem;
  }

  .meme-item {
    max-width: 100%;
    padding: 0.8rem;
  }

  .meme-image {
    width: 100%;
    height: auto;
  }

  .nav-link {
    margin: 1rem auto;
    width: 90%;
    text-align: center;
  }
}

@media (max-width: 400px) {
  .main-header {
    font-size: 1.5rem;
  }

  button {
    padding: 0.6rem 1rem;
  }
}


</style>


