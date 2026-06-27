import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        isAuthenticated: !!localStorage.getItem('access_token'), // 初始状态
    },
    mutations: {
        login(state) {
            state.isAuthenticated = true; // 更新登录状态
        },
        logout(state) {
            state.isAuthenticated = false; // 更新登出状态
        },
    },
    actions: {
        login({ commit }) {
            commit('login'); // 提交登录变更
        },
        logout({ commit }) {
            commit('logout'); // 提交登出变更
        },
    },
    getters: {
        isAuthenticated: state => state.isAuthenticated, // 获取登录状态
    },
});
