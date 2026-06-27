import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import dataV from '@jiaminghi/data-view';
import VueParticles from 'vue-particles';
import axios from '@/api/axios';
import "swiper/swiper.min.css";
import * as echarts from 'echarts';
import Toast from 'vue-toastification';
import "vue-toastification/dist/index.css"; // 引入样式文件
import "@/utils/echarts-wordcloud.min.js";
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import '@fortawesome/fontawesome-free/css/all.min.css'

Vue.use(ElementUI);
Vue.use(VueParticles);
Vue.use(dataV);
Vue.use(Toast); // 注册 Toast 插件
Vue.config.productionTip = false;
Vue.config.devtools = true; // 启用 Devtools
Vue.prototype.$http = axios;
Vue.prototype.$echarts = echarts;

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');