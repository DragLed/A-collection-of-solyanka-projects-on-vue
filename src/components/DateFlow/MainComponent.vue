<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { differenceInDays, differenceInMonths, format, parseISO, addMonths, addDays} from 'date-fns'
import { ru } from 'date-fns/locale'




const DateListInDays = ref([]);

const startDate = ref(''); 

watch(startDate, (val) => {
  if (val) {
    DateListInDay();
  }
});

const DateList = [
  { label: "10 дней", type: "days", value: 10 },
  { label: "1 месяц", type: "months", value: 1 },
  { label: "50 дней", type: "days", value: 50 },
  { label: "100 дней", type: "days", value: 100 },
  { label: "200 дней", type: "days", value: 200 },
  { label: "300 дней", type: "days", value: 300 },
  { label: "1 год", type: "months", value: 12 },
  { label: "400 дней", type: "days", value: 400 },
  { label: "500 дней", type: "days", value: 500 },
  { label: "600 дней", type: "days", value: 600 },
    { label: "650 дней", type: "days", value: 650 },
    { label: "700 дней", type: "days", value: 700 },
    { label: "750 дней", type: "days", value: 750 },
    { label: "800 дней", type: "days", value: 800 },
    { label: "850 дней", type: "days", value: 850 },
    { label: "900 дней", type: "days", value: 900 },
    { label: "950 дней", type: "days", value: 950 },
  { label: "700 дней", type: "days", value: 700 },
  { label: "2 года", type: "months", value: 24 },
  { label: "800 дней", type: "days", value: 800 },
  { label: "900 дней", type: "days", value: 900 },
  { label: "1000 дней", type: "days", value: 1000 },
    { label: "3 года", type: "months", value: 36 },
    { label: "4 года", type: "months", value: 48 },
    { label: "5 лет", type: "months", value: 60 },
    { label: "6 лет", type: "months", value: 72 },
    { label: "7 лет", type: "months", value: 84 },
    { label: "8 лет", type: "months", value: 96 },
    { label: "9 лет", type: "months", value: 108 },
    { label: "10 лет", type: "months", value: 120 },
    { label: "11 лет", type: "months", value: 132 },
    { label: "12 лет", type: "months", value: 144 },
    { label: "13 лет", type: "months", value: 156 },
    { label: "14 лет", type: "months", value: 168 },
    { label: "15 лет", type: "months", value: 180 },
    { label: "16 лет", type: "months", value: 192 },
    { label: "17 лет", type: "months", value: 204 },
    { label: "18 лет", type: "months", value: 216 },
    { label: "19 лет", type: "months", value: 228 },
    { label: "20 лет", type: "months", value: 240 },
    { label: "21 год", type: "months", value: 252 },
    { label: "22 года", type: "months", value: 264 },
    { label: "23 года", type: "months", value: 276 },
    { label: "24 года", type: "months", value: 288 },
    { label: "25 лет", type: "months", value: 300 },
    { label: "30 лет", type: "months", value: 360 },
    { label: "35 лет", type: "months", value: 420 },
    { label: "40 лет", type: "months", value: 480 },
    { label: "50 лет", type: "months", value: 600 },
    { label: "75 лет", type: "months", value: 900 },
    { label: "100 лет", type: "months", value: 1200 },
    { label: "1000 лет", type: "months", value: 12000 },
    { label: "10000 лет", type: "months", value: 120000 },







  

];


function DateListInDay() {
  const start = parseISO(startDate.value);
  const results = [];
  const result = [];
  const today = new Date();

  for (const item of DateList) {
    let end;

    if (item.type === "days") {
      end = addDays(start, item.value);
    } else if (item.type === "months") {
      end = addMonths(start, item.value);
    }

    const formattedDate = format(end, 'dd MMMM yyyy', { locale: ru });

    results.push({
      label: item.label,
      dateFormatted: formattedDate,
      date: end.toISOString(),
    });
  }

  


    for (const item of results) {
    const differenceDay = differenceInDays(new Date(item.date), today);
    console.log(`Разница в днях для ${item.label}: ${differenceDay} дн.`);
    

    result.push({
        label: item.label,
        differenceDay: differenceDay,
        dateFormatted: item.dateFormatted,

    })};

    DateListInDays.value = result;
    console.log('DateListInDays:', DateListInDays.value);
}





function LoadDate() {
  const savedDate = localStorage.getItem('startDate');
  if (savedDate) {
    startDate.value = savedDate; // строка ISO
  } else {
    const defaultDate = new Date('2024-07-25T00:00:00');
    startDate.value = defaultDate.toISOString();
  }
  console.log('Start Date:', startDate.value);
}

const differenceDateInMonthsAndDays = computed(() => {
    const start = parseISO(startDate.value);
    const end = new Date();
    const months = differenceInMonths(end, start);
    const intermediateDate = addMonths(start, months);
    const days = differenceInDays(end, intermediateDate);

    return(`${months} мес. ${days} дн.`);
});

const differenceDateInDays = computed(() => {
    const start = parseISO(startDate.value);
    const end = new Date();
    const days = differenceInDays(end, start);

    return(`${days} дн.`);
});



onMounted(() => {
  LoadDate();
  DateListInDay();
});
</script>

<template>
  <section class="date-container">
    <p class="current-diff">
  Мы вместе уже❤️: <strong>{{ differenceDateInMonthsAndDays }}</strong>  
  (<em>{{ differenceDateInDays }}</em>)
</p>


    <ul class="date-list">
      <li v-for="dateItem in DateListInDays" :key="dateItem.label" :class="{'past': dateItem.differenceDay < 0, 'today': dateItem.differenceDay === 0, 'future': dateItem.differenceDay > 0}">
        <div class="label">{{ dateItem.label }}</div>
        <div class="date">{{ dateItem.dateFormatted }}</div>
        <div class="difference">
          <template v-if="dateItem.differenceDay > 0">
            Через <strong>{{ dateItem.differenceDay }} дн.</strong>
          </template>
          <template v-else-if="dateItem.differenceDay < 0">
            Было <strong>{{ Math.abs(dateItem.differenceDay) }} дн. назад</strong>
          </template>
          <template v-else>
            <strong>Сегодня!</strong>
          </template>
        </div>
      </li>
    </ul>
  </section>
</template>


<style scoped>
.date-container {
  max-width: 480px;
  margin: 2rem auto;
  padding: 1.5rem 2rem;
  background: rgba(18, 18, 24, 0.85);
  border-radius: 12px;
  box-shadow: 0 0 15px rgba(77, 171, 247, 0.3);
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.current-diff {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
  color: #4dabf7;
}

.date-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.date-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  margin-bottom: 0.7rem;
  border-radius: 8px;
  background: rgba(30, 30, 36, 0.8);
  box-shadow: 0 0 8px rgba(77, 171, 247, 0.1);
  transition: background-color 0.3s ease;
}

.date-list li.future {
  border-left: 4px solid #4dabf7;
}

.date-list li.past {
  border-left: 4px solid #e57373;
  opacity: 0.8;
}

.date-list li.today {
  border-left: 4px solid #20c997;
  background: rgba(32, 201, 151, 0.2);
  font-weight: 600;
}

.label {
  flex: 1;
  font-weight: 600;
  font-size: 1rem;
  color: #b0c7ff;
}

.date {
  flex: 1;
  text-align: center;
  font-size: 0.95rem;
  color: #a0a0a0;
  font-style: italic;
}

.difference {
  flex: 1;
  text-align: right;
  font-size: 1rem;
  font-weight: 700;
  color: #4dabf7;
}

.date-list li.past .difference {
  color: #e57373;
}

.date-list li.today .difference {
  color: #20c997;
}

</style>
