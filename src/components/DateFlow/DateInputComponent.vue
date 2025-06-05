<script setup>
import { ref, onMounted, watch } from 'vue'
import { parse, format } from 'date-fns'
import { ru } from 'date-fns/locale'

const InputDate = ref("2024-07-25");
const startDate = ref('');
const formattedStartDate = ref(''); 

function parseCustomDate(dateString) {
  try {
    const parsed = parse(dateString, 'yyyy-MM-dd', new Date());
    startDate.value = parsed;
    formattedStartDate.value = format(parsed, 'dd MMMM yyyy', { locale: ru });
    localStorage.setItem('startDate', dateString);
  } catch (error) {
    throw new Error(`Неверный формат даты. Ожидается yyyy-MM-dd, получено: ${dateString}`);
  }
}

watch(InputDate, (val) => {
  if (val) parseCustomDate(val)
})

function LoadDate() {
  const saved = localStorage.getItem('startDate');
  if (saved) {
    InputDate.value = saved;
    parseCustomDate(saved);
  }
}

onMounted(() => {
  LoadDate();
});
</script>

<template>
  <div class="container">
    <label for="date">Выбери дату:</label>
    <input type="date" id="date" v-model="InputDate" />

    <p class="result">Дата начала отношений: <span v-if="formattedStartDate">{{ formattedStartDate }}</span></p>
    <router-link to="/DateFlower" class="nav-link">Подтвердить</router-link>
  </div>
</template>

<style scoped>
.container {
  background-color: #1e1e2f;
  padding: 1.5rem;
  border-radius: 1rem;
  max-width: 400px;
  margin: 0 auto;
  color: #fff;
  font-family: 'Segoe UI', sans-serif;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

input[type="date"] {
  background-color: #2a2a3f;
  color: #fff;
  border: none;
  padding: 0.5rem;
  border-radius: 0.5rem;
  width: 100%;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.result {
  font-size: 1rem;
  margin-top: 0.5rem;
}

.nav-link {
  display: inline-block;
  margin-left: auto;
  margin-bottom: 1.5rem;
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
  background: linear-gradient(145deg, #63b3ff, ф#3598ff);
  box-shadow: 0 0 15px rgba(77, 171, 247, 0.8), 0 0 10px rgba(77, 171, 247, 0.4);
  transform: translateY(-2px);
}

</style>
