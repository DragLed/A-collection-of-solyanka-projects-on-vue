// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import MainComponent from '../components/CityTravel/homeComponent.vue'
import ExcursionPage from '../components/CityTravel/excursionPage.vue'
// import TestComponent from '../components/TestComponent.vue';
import HomeView from '../components/CatsFact&Image/HomeView.vue';
import ImageView from '../components/CatsFact&Image/ImageView.vue';
import FactView from '../components/CatsFact&Image/FactView.vue';
import MainComponent2 from '../components/My-To-do-List/mainComponent.vue'
import DefaultComponent from '../components/DefaultComponent.vue';



const routes = [
  { path: '/', component: DefaultComponent },
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