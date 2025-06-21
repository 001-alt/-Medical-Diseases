import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import Index from '../views/Index.vue';
import Pred from '../views/Pred.vue';
import TableData from '../views/TableData.vue';
import UserManagement from '../views/UserManagement.vue';
import Login from '../views/Login.vue';
import LogManagement from '../views/LogManagement.vue'; // 新增日志管理视图
import PredictionHistory from '../views/PredictionHistory.vue';
import NotFound from '../views/NotFound.vue'; // 404 页面组件
Vue.use(VueRouter);
const routes = [
    {
        path: '/', 
        name: 'Home',
        component: Home,
        meta: { name: '首页' },
    },
    {
        path: '/index',
        name: 'Index',
        component: Index,
        meta: { name: '可视化' },
    },
    {
        path: '/pred',
        name: 'Pred',
        component: Pred,
        meta: { name: '在线预测', requiresAuth: true  },
    },
    {
        path: '/tableData',
        name: 'TableData',
        component: TableData,
        meta: { name: '数据表格', requiresAuth: true  },
    },
    {
        path: '/usermanagement', 
        name: 'UserManagement',
        component: UserManagement,
        meta: { name: '用户管理', requiresAuth: true  },
    },
    {
        path: '/login', // 登录页路由
        name: 'Login',
        component: Login,
        meta: { name: '登录' },
    },
    {
        path: '/predictionhistory',
        name: 'PredictionHistory',
        component: PredictionHistory,
        meta: { name: '预测历史', requiresAuth: true },
      },
      {
        path: '/logmanagement',  // 新增日志管理路由
        name: 'LogManagement',
        component: LogManagement,
        meta: { name: '日志管理', requiresAuth: true  },
    }, 
    
];
const router = new VueRouter({
    mode: 'history', // 使用 HTML5 History 模式
    base: process.env.BASE_URL,
    routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('access_token'); // 检查用户是否登录
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    if (requiresAuth && !isAuthenticated) {
        next({ name: 'Login' }); // 如果需要身份验证但用户未登录，重定向到登录页面
    } else {
        next(); // 继续路由
    }
});


export default router;
