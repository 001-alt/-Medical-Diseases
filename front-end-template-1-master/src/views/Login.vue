<template>
    <dv-border-box-8
        style="width: 100%; max-width: 600px; height: 350px; margin: auto; padding: 20px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); border-radius: 10px;">
        <div class="login-container">
            <h2 class="login-title">用户验证</h2>
            <form @submit.prevent="handleLogin">
                <div class="form-group">
                    <label for="username">用户名:</label>
                    <input type="text" id="username" v-model="username" required />
                </div>
                <div class="form-group">
                    <label for="password">密码:</label>
                    <input type="password" id="password" v-model="password" required />
                </div>
                <button type="submit">登录</button>
                <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
            </form>
        </div>
    </dv-border-box-8>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex'; // 引入 Vuex 的 mapActions

export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: ''
        };
    },
    computed: {
        isLoggedIn() {
            return !!localStorage.getItem('access_token'); // 计算属性来判断用户是否已登录
        }
    },
    methods: {
        ...mapActions(['login']), // 使用 Vuex 的登录方法

        async handleLogin() {
            this.errorMessage = ''; // 清空错误信息
            try {
                const response = await axios.post('http://localhost:5000/login', {
                    username: this.username,
                    password: this.password
                });

                if (response.data.status === 'success') {
                    // 存储 token
                    localStorage.setItem('access_token', response.data.access_token);

                    // 调用 Vuex 的登录方法
                    this.login(); // 更新 Vuex 状态

                    // 登录成功后可以进行页面跳转
                    this.$router.push('/'); // 假设您有一个 home 页面
                } else {
                    this.errorMessage = response.data.message;
                }
            } catch (error) {
                this.errorMessage = '登录失败，请检查您的用户名和密码';
                console.error(error);
            }
        }
    }
};
</script>

<style scoped>
html,
body {
    height: 100%;
    margin: 0;
    background-color: #282c34;
}

.login-container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    color: white;
    font-family: Arial, sans-serif;
}

.login-title {
    font-size: 2rem;
    text-align: center;
    font-weight: bold;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1rem;
    color: #212020;
}

button {
    width: 100%;
    margin: 10px 0;
    padding: 10px;
    background-color: #007bff;
    border: none;
    border-radius: 15px;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}

.error {
    color: red;
    text-align: center;
    margin-top: 10px;
}
</style>
