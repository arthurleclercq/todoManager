import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
import store from "./store"

Vue.use(BootstrapVue);
Vue.config.productionTip = false

axios.interceptors.request.use(request => { 
  let token=localStorage.getItem("jwt")                                                                                          
  request.headers['token'] = token;
  return request;                                                                                                                   
}, err => {                                                                                                                           
  return Promise.reject(err);                                                                                                       
}); 


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
