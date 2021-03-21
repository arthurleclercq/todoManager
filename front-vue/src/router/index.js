import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import List from '../views/List.vue'
import Login from '../views/Login.vue'
import Account from '../views/Account.vue'
import store from '@/store'

Vue.use(VueRouter)

function loginIfNot(to,from,next){
  if (!store.getters.isAuthenticated){
    next("/login")
  }else{
    next()
  }
}



const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    beforeEnter: loginIfNot
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/account',
    name: 'Account',
    component: Account
  },
  {
    path: '/list/:todo_list_name',
    name: 'List',
    component: List,
    beforeEnter: loginIfNot
  },
  {
    path: '*',
    beforeEnter: (from, to, next) => next('/login')
}]; 


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
