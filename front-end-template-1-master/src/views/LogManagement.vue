<!-- <template>
    <div class="log-management">
       
        <div class="header-actions">
            <div class="search-box">
                <input type="text" v-model="searchQuery" placeholder="搜索日志..." @input="handleSearch" />
                <button @click="handleSearchClear">清除</button>
            </div>
        </div>

     
        <div class="main-content">
            <div v-if="loading" class="loader">加载中...</div>
            <table v-if="filteredLogs.length" class="log-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户ID</th>
                        <th>操作</th>
                        <th>详细信息</th>
                        <th>时间</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="log in paginatedLogs" :key="log.id">
                        <td>{{ log.id }}</td>
                        <td>{{ log.user_id }}</td>
                        <td>{{ log.action }}</td>
                        <td>{{ log.details }}</td>
                        <td>{{ new Date(log.timestamp).toLocaleString() }}</td>
                    </tr>
                </tbody>
            </table>

          
            <div v-else class="empty-state">暂无日志记录</div>

            
            <div class="pagination-container" v-if="filteredLogs.length">
                <button @click="previousPage" :disabled="currentPage === 1">上一页</button>
                <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
                <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'LogManagement',
    data() {
        return {
            logs: [],
            loading: false,
            searchQuery: '',
            currentPage: 1,
            itemsPerPage: 10,
        };
    },
    computed: {
        filteredLogs() {
            if (!this.searchQuery) return this.logs;
            const query = this.searchQuery.toLowerCase();
            return this.logs.filter(log =>
                log.action.toLowerCase().includes(query) ||
                log.details.toLowerCase().includes(query)
            );
        },
        paginatedLogs() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredLogs.slice(start, start + this.itemsPerPage);
        },
        totalPages() {
            return Math.ceil(this.filteredLogs.length / this.itemsPerPage);
        }
    },
    methods: {
        async fetchLogs() {
            this.loading = true;
            try {
                const response = await axios.get('http://127.0.0.1:5000/getOperationLogs');
                if (response.data.status === 'success') {
                    // 添加额外的数据验证
                    const validLogs = response.data.logs.map(log => ({
                        ...log,
                        timestamp: log.timestamp || new Date().toISOString() // 提供默认值
                    }));
                    this.logs = validLogs;
                } else {
                    console.error('获取日志失败:', response.data.message);
                    this.logs = []; // 确保 logs 不会为 undefined
                }
            } catch (error) {
                console.error('获取日志失败:', error);
                this.logs = []; // 确保 logs 不会为 undefined
                if (error.response) {
                    // 服务器返回了错误响应
                    alert(`服务器错误: ${error.response.data.message}`);
                } else {
                    // 网络或其他错误
                    alert('无法连接到服务器');
                }
            } finally {
                this.loading = false;
            }
        },


        handleSearch() {
            // 这里可以添加任何额外的逻辑，比如记录搜索日志
            console.log('Searching logs for: ', this.searchQuery);
        },

        handleSearchClear() {
            this.searchQuery = '';
        },

        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },

        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        }
    },
    mounted() {
        this.fetchLogs();
    }
};
</script>

<style scoped>
.log-management {
    padding: 20px;
    background-color: #f0f2f5;
    min-height: 100vh;
}

.header-actions {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    background: #fff;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.search-box {
    display: flex;
    align-items: center;
}

.search-box input {
    padding: 10px 15px;
    margin-right: 10px;
    border: 1px solid #e8e8e8;
    border-radius: 4px;
    width: 200px;
}

.main-content {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.log-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.log-table th {
    background: #fafafa;
    padding: 16px;
    text-align: left;
}

.log-table td {
    padding: 16px;
    border-bottom: 1px solid #f0f0f0;
}

.empty-state {
    text-align: center;
    padding: 40px 0;
}

.pagination-container {
    padding: 15px;
    text-align: right;
    background: #fff;
}

.pagination-container button {
    margin: 0 4px;
}
</style>  -->

<template>
    <div class="log-management">
        <div class="header-actions">
            <div class="search-box">
                <input type="text" v-model="searchQuery" placeholder="搜索日志..." @input="handleSearch" />
                <button @click="handleSearchClear">清除</button>
            </div>
        </div>

        <div class="main-content">
            <div v-if="loading" class="loader">加载中...</div>
            <table v-if="filteredLogs.length" class="log-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>用户ID</th>
                        <th>操作</th>
                        <th>详细信息</th>
                        <th>时间</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="log in paginatedLogs" :key="log.id">
                        <td>{{ log.id }}</td>
                        <td>{{ log.user_id }}</td>
                        <td>{{ log.action }}</td>
                        <td>{{ log.details }}</td>
                        <td>{{ new Date(log.timestamp).toLocaleString() }}</td>
                    </tr>
                </tbody>
            </table>

            <div v-else class="empty-state">暂无日志记录</div>

            <div class="pagination-container" v-if="filteredLogs.length">
                <button @click="previousPage" :disabled="currentPage === 1">上一页</button>
                <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
                <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'LogManagement',
    data() {
        return {
            logs: [],
            loading: false,
            searchQuery: '',
            currentPage: 1,
            itemsPerPage: 10,
        };
    },
    computed: {
        filteredLogs() {
            if (!this.searchQuery) return this.logs;
            const query = this.searchQuery.toLowerCase();
            return this.logs.filter(log =>
                log.action.toLowerCase().includes(query) ||
                log.details.toLowerCase().includes(query)
            );
        },
        paginatedLogs() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredLogs.slice(start, start + this.itemsPerPage);
        },
        totalPages() {
            return Math.ceil(this.filteredLogs.length / this.itemsPerPage);
        }
    },
    methods: {
        async fetchLogs() {
            this.loading = true;
            try {
                const response = await axios.get('http://127.0.0.1:5000/getOperationLogs');
                if (response.data.status === 'success') {
                    const validLogs = response.data.logs.map(log => ({
                        ...log,
                        timestamp: log.timestamp || new Date().toISOString()
                    }));
                    this.logs = validLogs;
                } else {
                    console.error('获取日志失败:', response.data.message);
                    this.logs = [];
                }
            } catch (error) {
                console.error('获取日志失败:', error);
                this.logs = [];
                if (error.response) {
                    alert(`服务器错误: ${error.response.data.message}`);
                } else {
                    alert('无法连接到服务器');
                }
            } finally {
                this.loading = false;
            }
        },
        handleSearch() {
            console.log('Searching logs for: ', this.searchQuery);
        },
        handleSearchClear() {
            this.searchQuery = '';
        },
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        }
    },
    mounted() {
        this.fetchLogs();
    }
};
</script>

<style scoped>
.log-management {
    padding: 20px;
    background-color: #0a192f;
    /* 深蓝背景 */
    min-height: 100vh;
    color: #e6f1ff;
    /* 浅蓝色字体 */
}

.header-actions {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    background: #172a45;
    /* 中等深蓝 */
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(16, 43, 122, 0.2);
    /* 蓝色投影 */
}

.search-box {
    display: flex;
    align-items: center;
    gap: 10px;
}

.search-box input {
    padding: 12px 20px;
    border: 1px solid #2d4059;
    /* 中间蓝色 */
    border-radius: 6px;
    width: 280px;
    background: #2d4059;
    /* 输入框背景 */
    color: #a8dadc;
    transition: all 0.3s ease;
}

.search-box input:focus {
    border-color: #00b4d8;
    /* 高亮蓝色 */
    box-shadow: 0 0 8px rgba(0, 180, 216, 0.3);
}

.search-box button {
    padding: 12px 24px;
    border-radius: 6px;
    background: #00b4d8;
    /* 亮蓝色按钮 */
    color: #f8f9fa;
    font-weight: 600;
    transition: transform 0.2s, background 0.3s;
}

.search-box button:hover {
    background: #0096c7;
    /* 深一点的蓝色 */
    transform: translateY(-1px);
}

.main-content {
    background: rgba(23, 42, 69, 0.9);
    /* 半透明深蓝 */
    border-radius: 12px;
    padding: 24px;
    backdrop-filter: blur(8px);
    box-shadow: 0 6px 24px rgba(0, 31, 63, 0.2);
}

.log-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 20px 0;
}

.log-table th {
    background: #27496d;
    /* 表头深蓝 */
    padding: 18px;
    font-weight: 600;
    color: #88dfff;
    border-bottom: 2px solid #00b4d8;
}

.log-table td {
    padding: 16px;
    border-bottom: 1px solid rgba(0, 180, 216, 0.15);
    /* 浅蓝色分隔线 */
    transition: background 0.2s;
}

.log-table tr:hover td {
    background: rgba(0, 180, 216, 0.05);
    /* 行悬停效果 */
}

.empty-state {
    text-align: center;
    padding: 50px 0;
    color: #88dfff;
    opacity: 0.7;
}

.pagination-container {
    padding: 20px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
}

.pagination-container button {
    padding: 10px 20px;
    border-radius: 6px;
    background: rgba(0, 180, 216, 0.8);
    /* 半透明蓝色 */
    color: #fff;
    border: none;
    transition: all 0.3s;
}

.pagination-container button:disabled {
    background: #27496d;
    /* 深蓝色禁用状态 */
    opacity: 0.6;
}

.pagination-container button:hover:not(:disabled) {
    background: #0096c7;
    box-shadow: 0 4px 12px rgba(0, 150, 199, 0.3);
}

.loader {
    text-align: center;
    padding: 30px;
    color: #88dfff;
    font-size: 1.1em;
}
</style>
