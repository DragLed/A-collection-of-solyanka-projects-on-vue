// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import ExcursionPage from '../components/CityTravel/excursionPage.vue'
// import TestComponent from '../components/TestComponent.vue';
import HomeView from '../components/CatsFact&Image/HomeView.vue';
import ImageView from '../components/CatsFact&Image/ImageView.vue';
import FactView from '../components/CatsFact&Image/FactView.vue';
import MainComponent2 from '../components/My-To-do-List/mainComponent.vue'
import DefaultComponent from '../components/IntroCompomemts/DefaultComponent.vue';
import AboutComponent from '@/components/IntroCompomemts/AboutComponent.vue';
import MainComponent3 from '@/components/DateFlow/MainComponent.vue';
import DateInputComponent from '@/components/DateFlow/DateInputComponent.vue';
import NotesComponent from '@/components/DateFlow/NotesComponent.vue';
import MainComponent4 from '@/components/Memmarket/MainComponent.vue';
import FavoritesView from '@/components/Memmarket/FavoritesView.vue';
import MainComponent from '@/components/CityTravel/mainComponent.vue';



const routes = [
  { path: '/', component: DefaultComponent },
  { path: '/aboutMe', component: AboutComponent },

  { path: '/Memmarket', component: MainComponent4},
  { path: '/Memmarket/favorites', component: FavoritesView},

  {path: '/DateFlower', component: MainComponent3},
  { path: '/DateFlower/DateInput', component: DateInputComponent },
  { path: '/DateFlower/Notes', component: NotesComponent },


  { path: '/excursion', component: MainComponent },
  { path: '/excursion/excursions/:id', component: ExcursionPage, name: 'excursion' },


  { path: '/Cats', component: HomeView},
  { path: '/Cats/Fact', component: FactView},
  { path: '/Cats/Image', component: ImageView},

  { path: '/My-To-Do-List', component: MainComponent2},



]

const router = createRouter({
    history: createWebHistory(),
    routes
  });

export default router