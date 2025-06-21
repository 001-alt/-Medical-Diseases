<template>
    <div class="welcome-page">
        <div class="bg-animation"></div>

        <div class="content">
            <!-- 系统标题 -->
            <div class="system-title">
                <h1>医疗数据可视化分析系统</h1>
                <p class="subtitle">Medical Data Visualization Analysis System</p>
            </div>

            <!-- 系统简介 -->
            <div class="system-intro">
                <h2>系统简介</h2>
                <p>本系统致力于医疗数据的可视化分析与预测，通过直观的图表展示和先进的预测算法，帮助医疗工作者更好地理解和分析医疗数据。系统提供实时数据监控、疾病预测、用户管理等多项功能，为医疗决策提供有力支持。</p>
            </div>

            <!-- 功能模块 -->
            <div class="feature-grid">
                <router-link v-for="(item, index) in features" :key="index" :to="item.path" class="feature-card">
                    <div class="card-content">
                        <div class="icon">{{ item.icon }}</div>
                        <h3>{{ item.title }}</h3>
                        <p>{{ item.desc }}</p>
                    </div>
                    <div class="card-bg"></div>
                </router-link>
            </div>

            <!-- 系统特点 -->
            <div class="system-features">
                <h2>系统特点</h2>
                <div class="features-list">
                    <div v-for="(feature, index) in systemFeatures" :key="index" class="feature-item">
                        <span class="feature-icon">{{ feature.icon }}</span>
                        <span>{{ feature.text }}</span>
                    </div>
                </div>
            </div>

            <!-- 登录按钮 -->
            <div class="login-section" v-if="!isAuthenticated">
                <router-link to="/login" class="login-btn">
                    登录系统
                    <span class="btn-effect"></span>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'WelcomePage',
    data() {
        return {
            isAuthenticated: false,
            features: [
                { icon: '🏥', title: '首页', desc: '查看医疗健康数据统计', path: '/' },
                { icon: '📊', title: '可视化', desc: '多维度数据可视化展示', path: '/index' },
                { icon: '👁️', title: '在线预测', desc: '实时疾病预测分析', path: '/pred' },
                { icon: '📋', title: '数据表格', desc: '详细的数据记录查询', path: '/tableData' },
                { icon: '👥', title: '用户管理', desc: '系统用户权限管理', path: '/usermanagement' },
                { icon: '📈', title: '预测历史', desc: '查看历史预测记录', path: '/predictionhistory' }
            ],
            systemFeatures: [
                { icon: '✨', text: '实时数据分析' },
                { icon: '🔮', text: '智能预测' },
                { icon: '🔒', text: '安全性保障' },
                { icon: '⚡', text: '高效可靠' }
            ]
        }
    },
    created() {
        this.isAuthenticated = !!localStorage.getItem('access_token')
    }
}
</script>

<style scoped>
.welcome-page {
    min-height: 100vh;
    background: #0a1929;
    position: relative;
    overflow: hidden;
}

.bg-animation {
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, #0a192f 0%, #112240 100%);
    opacity: 0.8;
    z-index: 1;
}

.content {
    position: relative;
    z-index: 2;
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px;
    color: #fff;
}

.system-title {
    text-align: center;
    margin-bottom: 60px;
}

.system-title h1 {
    font-size: 3em;
    margin-bottom: 15px;
    background: linear-gradient(120deg, #64ffda 0%, #48bfe3 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 20px rgba(100, 255, 218, 0.2);
}

.subtitle {
    font-size: 1.4em;
    color: #8892b0;
}

.system-intro {
    background: rgba(17, 34, 64, 0.6);
    padding: 30px;
    border-radius: 15px;
    border: 1px solid rgba(100, 255, 218, 0.1);
    backdrop-filter: blur(10px);
    margin-bottom: 60px;
    line-height: 1.8;
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 25px;
    margin-bottom: 60px;
}

.feature-card {
    position: relative;
    padding: 25px;
    background: rgba(17, 34, 64, 0.6);
    border-radius: 15px;
    border: 1px solid rgba(100, 255, 218, 0.1);
    backdrop-filter: blur(10px);
    text-decoration: none;
    color: #fff;
    overflow: hidden;
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(100, 255, 218, 0.3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.card-content {
    position: relative;
    z-index: 2;
}

.card-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at top right, rgba(100, 255, 218, 0.1), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.feature-card:hover .card-bg {
    opacity: 1;
}

.icon {
    font-size: 2.5em;
    margin-bottom: 15px;
}

h3 {
    color: #64ffda;
    margin-bottom: 10px;
    font-size: 1.4em;
}

.system-features {
    background: rgba(17, 34, 64, 0.6);
    padding: 30px;
    border-radius: 15px;
    border: 1px solid rgba(100, 255, 218, 0.1);
}

.features-list {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 25px;
}

.feature-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 15px;
    background: rgba(100, 255, 218, 0.05);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.feature-item:hover {
    background: rgba(100, 255, 218, 0.1);
}

.login-btn {
    position: relative;
    display: inline-block;
    padding: 15px 40px;
    background: linear-gradient(45deg, #64ffda, #48bfe3);
    color: #0a192f;
    border-radius: 30px;
    text-decoration: none;
    font-weight: bold;
    overflow: hidden;
}

.btn-effect {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
}

.login-btn:hover .btn-effect {
    transform: translateX(100%);
}

@media (max-width: 768px) {
    .feature-grid {
        grid-template-columns: 1fr;
    }

    .features-list {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>
