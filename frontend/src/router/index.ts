import { createRouter, createWebHistory } from 'vue-router'
import ReaderView from '../views/ReaderView.vue'
import Dashboard  from '../components/Dashboard.vue'

const routes = [
  // …your other routes…
  { path: '/', name: 'Dashboard', component: Dashboard },
  {
    path: '/reader',
    name: 'Reader',
    component: ReaderView,
    props: route => ({
      fileId: route.query.fileId as string,
      page: parseInt(route.query.page as string) || 1
    })
  }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
