<!-- <template>
    <div id="header">
        <div id="header-left">
            <h1>医疗可视化</h1>
        </div>
        <div id="header-nav">
            <div v-for="item in routerLink" :key="item.path" v-if="!(item.name === 'Login' && isAuthenticated)"
                :class="['header-nav-item', activePath === item.path ? 'active' : '', 'cool-border']"
                @click="routerChange(item.path)">
                <router-link class="nav content" :to="item.path">
                    {{ item.meta.name }}
                </router-link>
                <div :class="[activePath === item.path ? 'top-left' : '', 'corner']"></div>
                <div :class="[activePath === item.path ? 'top-right' : '', 'corner']"></div>
                <div :class="[activePath === item.path ? 'bottom-left' : '', 'corner']"></div>
                <div :class="[activePath === item.path ? 'bottom-right' : '', 'corner']"></div>
            </div>
        </div>
        <div id="header-right">
            <div id="header-time">
                {{ currentDateTime }}
            </div>
            <div id="login-status">
                
                <el-avatar v-if="!isAuthenticated" icon="el-icon-user" @click.native="goToLogin" class="avatar-icon" />

                
                <el-dropdown v-else @command="handleCommand">
                    <span class="el-dropdown-link">
                        <el-avatar :src="avatarUrl" class="avatar-icon" />
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                        <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            activePath: "/",
            routerLink: [],
            currentDateTime: this.getCurrentDateTime(),
            avatarUrl: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        };
    },
    computed: {
        ...mapGetters(['isAuthenticated'])
    },
    created() {
        this.routerLink = this.$router.options.routes;
        this.activePath = this.$route.path;
        this.interval = setInterval(() => {
            this.currentDateTime = this.getCurrentDateTime();
        }, 1000);
    },
    beforeDestroy() {
        // 清除定时器
        if (this.interval) {
            clearInterval(this.interval);
        }
    },
    methods: {
        getCurrentDateTime() {
            const now = new Date();
            const year = now.getFullYear();
            const month = (now.getMonth() + 1).toString().padStart(2, '0');
            const day = now.getDate().toString().padStart(2, '0');
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },
        routerChange(path) {
            this.activePath = path;
        },
        goToLogin() {
            this.$router.push('/login');
        },
        handleCommand(command) {
            if (command === 'logout') {
                this.$store.dispatch('logout');
                this.$router.push('/login');
            } else if (command === 'profile') {
                this.$router.push('/profile');
            }
        }
    }
}
</script>

<style lang="less" scoped>
#header-time {
    color: #52a2e4;
    font-size: 17px;
}

#header-right {
    display: flex;
    align-items: center;
}

#login-status {
    margin-left: 20px;

    .avatar-icon {
        cursor: pointer;
        background-color: #007bff;
        color: white;
        transition: all 0.3s;

        &:hover {
            transform: scale(1.05);
            background-color: #0056b3;
        }
    }
}

.el-dropdown-link {
    cursor: pointer;
}

/* 其他原有样式保持不变 */
#header {
    display: flex;
    padding: 10px 150px 0 150px;
    align-items: center;
    justify-content: space-between;

    #header-left {
        h1 {
            color: #fff;
            font-size: 23px;
        }
    }

    #header-nav {
        display: flex;

        .header-nav-item {
            margin-right: 15px;
            padding: 10px 40px;
            border: 1px solid transparent;
            border-radius: 80px;
        }

        .header-nav-item.active {
            background: #1b2d4a;
        }

        .nav {
            text-decoration: none;
            color: #52a2e4;
            font-size: 15px;
        }
    }
}

.cool-border {
    position: relative;
}

.corner {
    position: absolute;
    width: 0;
    height: 0;
    border: 5px solid transparent;
}

.top-left {
    top: 0;
    left: 0;
    border-top-color: #fff;
    border-left-color: #fff;
}

.top-right {
    top: 0;
    right: 0;
    border-top-color: #fff;
    border-right-color: #fff;
}

.bottom-left {
    bottom: 0;
    left: 0;
    border-bottom-color: #fff;
    border-left-color: #fff;
}

.bottom-right {
    bottom: 0;
    right: 0;
    border-bottom-color: #fff;
    border-right-color: #fff;
}

.content {
    display: flex;
    justify-content: center;
    align-items: center;
}

.avatar-icon {
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
        transform: scale(1.05);
    }
}
</style> -->

<template>
    <div id="header">
        <div id="header-left">
            <h1>医疗可视化</h1>
        </div>
        <div id="header-nav">
            <div v-for="item in filteredRouterLinks" :key="item.path"
                :class="['header-nav-item', activePath === item.path ? 'active' : '', 'cool-border']"
                @click="routerChange(item.path)">
                <router-link class="nav content" :to="item.path">
                    {{ item.meta.name }}
                </router-link>
                <div :class="[activePath === item.path ? 'top-left' : '', 'corner']"></div>
                <div :class="[activePath === item.path ? 'top-right' : '', 'corner']"></div>
                <div :class="[activePath === item.path ? 'bottom-left' : '', 'corner']"></div>
                <div :class="[activePath === item.path ? 'bottom-right' : '', 'corner']"></div>
            </div>
        </div>
        <div id="header-right">
            <div id="header-time">
                {{ currentDateTime }}
            </div>
            <div id="login-status">
                <!-- 未登录显示默认头像 -->
                <el-avatar v-if="!isAuthenticated" icon="el-icon-user" @click.native="goToLogin" class="avatar-icon" />

                <!-- 登录后显示用户头像和下拉菜单 -->
                <el-dropdown v-else @command="handleCommand">
                    <span class="el-dropdown-link">
                        <el-avatar :src="avatarUrl" class="avatar-icon" />
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item command="logManagement">日志管理</el-dropdown-item>
                        <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            activePath: "/",
            routerLink: [],
            currentDateTime: this.getCurrentDateTime(),
            avatarUrl: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'
        };
    },
    computed: {
        ...mapGetters(['isAuthenticated']),
        filteredRouterLinks() {
            return this.routerLink.filter(route => {
                // 如果用户未登录，只显示Home和Index
                if (!this.isAuthenticated) {
                    return route.name === 'Home' || route.name === 'Index';
                }
                // 如果用户已登录，显示除Login和LogManagement以外的所有路由
                return route.name !== 'Login' && route.name !== 'LogManagement';
            });
        },
    },
    created() {
        this.routerLink = this.$router.options.routes;
        this.activePath = this.$route.path;
        this.interval = setInterval(() => {
            this.currentDateTime = this.getCurrentDateTime();
        }, 1000);
        // 如果用户未登录且当前路径需要认证，重定向到首页
        if (!this.isAuthenticated && this.$route.meta.requiresAuth) {
            this.$router.push('/');
        }
    },
    watch: {
        // 监听认证状态变化
        isAuthenticated(newValue) {
            if (!newValue && this.$route.meta.requiresAuth) {
                this.$router.push('/');
            }
        }
    },
    beforeDestroy() {
        // 清除定时器
        if (this.interval) {
            clearInterval(this.interval);
        }
    },
    methods: {
        getCurrentDateTime() {
            const now = new Date();
            const year = now.getFullYear();
            const month = (now.getMonth() + 1).toString().padStart(2, '0');
            const day = now.getDate().toString().padStart(2, '0');
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const seconds = now.getSeconds().toString().padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },
        routerChange(path) {
            this.activePath = path;
        },
        goToLogin() {
            this.$router.push('/login');
        },
        handleCommand(command) {
            if (command === 'logout') {
                this.$store.dispatch('logout');
                this.$router.push('/login');
            } else if (command === 'logManagement') {
                this.$router.push('/logmanagement');
            }
        }
    }
}
</script>


<style lang="less" scoped>
#header-time {
    color: #52a2e4;
    font-size: 17px;
}

#header-right {
    display: flex;
    align-items: center;
}

#login-status {
    margin-left: 20px;

    .avatar-icon {
        cursor: pointer;
        background-color: #007bff;
        color: white;
        transition: all 0.3s;

        &:hover {
            transform: scale(1.05);
            background-color: #0056b3;
        }
    }
}

.el-dropdown-link {
    cursor: pointer;
}

/* 其他原有样式保持不变 */
#header {
    display: flex;
    padding: 10px 150px 0 150px;
    align-items: center;
    justify-content: space-between;

    #header-left {
        h1 {
            color: #fff;
            font-size: 23px;
        }
    }

    #header-nav {
        display: flex;

        .header-nav-item {
            margin-right: 15px;
            padding: 10px 40px;
            border: 1px solid transparent;
            border-radius: 80px;
        }

        .header-nav-item.active {
            background: #1b2d4a;
        }

        .nav {
            text-decoration: none;
            color: #52a2e4;
            font-size: 15px;
        }
    }
}

.cool-border {
    position: relative;
}

.corner {
    position: absolute;
    width: 0;
    height: 0;
    border: 5px solid transparent;
}

.top-left {
    top: 0;
    left: 0;
    border-top-color: #fff;
    border-left-color: #fff;
}

.top-right {
    top: 0;
    right: 0;
    border-top-color: #fff;
    border-right-color: #fff;
}

.bottom-left {
    bottom: 0;
    left: 0;
    border-bottom-color: #fff;
    border-left-color: #fff;
}

.bottom-right {
    bottom: 0;
    right: 0;
    border-bottom-color: #fff;
    border-right-color: #fff;
}

.content {
    display: flex;
    justify-content: center;
    align-items: center;
}

.avatar-icon {
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
        transform: scale(1.05);
    }
}
</style>
