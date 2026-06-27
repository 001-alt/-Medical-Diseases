<!-- <template>
    <div class="user-management">
        <div class="header-actions">
            <div class="search-box">
                <input type="text" v-model="searchQuery" placeholder="搜索用户..." @input="handleSearch" />
                <button @click="handleSearchClear">清除</button>
            </div>
            <button @click="openModal">添加用户</button>
        </div>

        <div class="main-content">
            <div v-if="loading" class="loader">加载中...</div>
            <table v-if="filteredUsers.length" class="user-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>姓名</th>
                        <th>邮箱</th>
                        <th>性别</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in paginatedUsers" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.gender }}</td>
                        <td>
                            <button @click="editUser(user)">编辑</button>
                            <button @click="confirmDelete(user)">删除</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div v-else class="empty-state">暂无用户数据</div>

            <div class="pagination-container" v-if="filteredUsers.length">
                <button @click="previousPage" :disabled="currentPage === 1">上一页</button>
                <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
                <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
            </div>
        </div>

        <div v-if="showModal" class="modal">
            <div class="modal-content">
                <h3>{{ isEditing ? '编辑用户' : '新增用户' }}</h3>
                <form @submit.prevent="submitForm">
                    <div>
                        <label>姓名:</label>
                        <input type="text" v-model="formData.name" required />
                    </div>
                    <div>
                        <label>密码:</label>
                        <input type="password" v-model="formData.password" required />
                    </div>
                    <div>
                        <label>邮箱:</label>
                        <input type="email" v-model="formData.email" required />
                    </div>
                    <div>
                        <label>性别:</label>
                        <select v-model="formData.gender">
                            <option value="male">男</option>
                            <option value="female">女</option>
                        </select>
                    </div>
                    <button type="submit">{{ isEditing ? '更新' : '添加' }}</button>
                    <button @click="closeModal">取消</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'UserManagement',
    data() {
        return {
            users: [],
            loading: false,
            searchQuery: '',
            currentPage: 1,
            itemsPerPage: 10,
            showModal: false,
            isEditing: false,
            formData: this.getInitialFormData()
        };
    },
    computed: {
        filteredUsers() {
            if (!this.searchQuery) return this.users;
            const query = this.searchQuery.toLowerCase();
            return this.users.filter(user =>
                user.name.toLowerCase().includes(query) ||
                user.email.toLowerCase().includes(query)
            );
        },
        paginatedUsers() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredUsers.slice(start, start + this.itemsPerPage);
        },
        totalPages() {
            return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
        }
    },
    methods: {
        async fetchUsers() {
            this.loading = true;
            try {
                const response = await axios.get('http://127.0.0.1:5000/getAllUsers');
                if (response.data.status === 'success') {
                    this.users = response.data.users.map(user => ({
                        id: user[0],
                        name: user[1],
                        email: user[3],
                        gender: user[4] === 'male' ? '男' : '女'
                    }));
                } else {
                    alert(response.data.message || '获取用户数据失败');
                }
            } catch (error) {
                alert('无法连接到服务器');
                console.error('Error fetching users:', error);
            } finally {
                this.loading = false;
            }
        },

        async deleteUser(userId) {
            try {
                const response = await axios.delete(`http://127.0.0.1:5000/deleteUser/${userId}`);
                if (response.data.status === 'success') {
                    alert('删除成功');
                    await this.fetchUsers();
                } else {
                    alert(response.data.message || '删除用户失败');
                }
            } catch (error) {
                alert('无法连接到服务器');
                console.error('Error deleting user:', error);
            }
        },

        async submitForm() {
            const url = this.isEditing
                ? `http://127.0.0.1:5000/updateUser/${this.formData.id}`
                : 'http://127.0.0.1:5000/addUser';
            const method = this.isEditing ? 'put' : 'post';

            try {
                const response = await axios({ method, url, data: this.formData });
                if (response.data.status === 'success') {
                    alert(this.isEditing ? '更新成功' : '添加成功');
                    this.showModal = false;
                    await this.fetchUsers();
                } else {
                    alert(response.data.message || (this.isEditing ? '更新失败' : '添加失败'));
                }
            } catch (error) {
                alert('无法连接到服务器');
                console.error('Error submitting form:', error);
            }
        },

        editUser(user) {
            this.formData = {
                id: user.id,
                name: user.name,
                password: '',
                email: user.email,
                gender: user.gender === '男' ? 'male' : 'female'
            };
            this.isEditing = true;
            this.showModal = true;
        },

        openModal() {
            this.formData = this.getInitialFormData();
            this.isEditing = false;
            this.showModal = true;
        },

        getInitialFormData() {
            return {
                id: null,
                name: '',
                password: '',
                email: '',
                gender: 'male'
            };
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
        },

        confirmDelete(user) {
            if (confirm(`确认删除用户 "${user.name}" 吗？`)) {
                this.deleteUser(user.id);
            }
        },

        closeModal() {
            this.showModal = false;
            this.formData = this.getInitialFormData();
        }
    },
    mounted() {
        this.fetchUsers();
    }
};
</script>
<style scoped>
.user-management {
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
    transition: all 0.3s;
    width: 200px;
}

.search-box input:focus {
    border-color: #1890ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    outline: none;
}

button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background: #1890ff;
    color: white;
    cursor: pointer;
    transition: all 0.3s;
}

button:hover {
    background: #40a9ff;
    box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.main-content {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.user-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.user-table th {
    background: #fafafa;
    padding: 16px;
    text-align: left;
    font-weight: 500;
    color: rgba(0, 0, 0, 0.85);
    border-bottom: 1px solid #f0f0f0;
}

.user-table td {
    padding: 16px;
    border-bottom: 1px solid #f0f0f0;
}

.user-table tr:hover {
    background: #fafafa;
}

/* 编辑和删除按钮 */
.user-table .edit-btn {
    background: #52c41a;
    padding: 4px 12px;
    margin-right: 8px;
}

.user-table .delete-btn {
    background: #ff4d4f;
    padding: 4px 12px;
}

.empty-state {
    text-align: center;
    padding: 40px 0;
    color: rgba(0, 0, 0, 0.45);
}

.pagination-container {
    padding: 15px;
    text-align: right;
    background: #fff;
    border-top: 1px solid #f0f0f0;
}

.pagination-container button {
    margin: 0 4px;
    background: #fff;
    color: rgba(0, 0, 0, 0.65);
    border: 1px solid #d9d9d9;
}

.pagination-container button:disabled {
    background: #f5f5f5;
    color: rgba(0, 0, 0, 0.25);
    cursor: not-allowed;
}

.pagination-container span {
    margin: 0 15px;
    color: rgba(0, 0, 0, 0.65);
}

/* 模态框样式 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.45);
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.3s;
}

.modal-content {
    background: #fff;
    padding: 24px;
    border-radius: 8px;
    width: 420px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    animation: slideIn 0.3s;
}

.modal-content h3 {
    margin: 0 0 24px;
    color: rgba(0, 0, 0, 0.85);
    font-size: 16px;
    font-weight: 500;
}

.modal-content form>div {
    margin-bottom: 24px;
}

.modal-content label {
    display: block;
    margin-bottom: 8px;
    color: rgba(0, 0, 0, 0.85);
}

.modal-content input,
.modal-content select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    transition: all 0.3s;
}

.modal-content input:focus,
.modal-content select:focus {
    border-color: #40a9ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    outline: none;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

/* Loader样式 */
.loader {
    text-align: center;
    padding: 40px;
    color: #1890ff;
}

/* 表格内的操作按钮 */
.user-table button {
    margin: 0 5px;
    padding: 5px 10px;
    font-size: 12px;
}

.user-table button:first-child {
    background: #52c41a;
}

.user-table button:last-child {
    background: #f5222d;
}
</style> -->


<template>
    <div class="user-management">
        <!-- 头部搜索和操作区 -->
        <div class="header-actions">
            <div class="search-box">
                <input type="text" v-model="searchQuery" placeholder="搜索用户..." @input="handleSearch" />
                <button @click="handleSearchClear">清除</button>
            </div>
            <button @click="openModal">添加用户</button>
        </div>

        <!-- 主要内容区 -->
        <div class="main-content">
            <div v-if="loading" class="loader">加载中...</div>
            <table v-if="filteredUsers.length" class="user-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>姓名</th>
                        <th>邮箱</th>
                        <th>性别</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in paginatedUsers" :key="user.id">
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.gender }}</td>
                        <td>
                            <button @click="editUser(user)">编辑</button>
                            <button @click="confirmDelete(user)">删除</button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <!-- 空状态 -->
            <div v-else class="empty-state">暂无用户数据</div>

            <!-- 分页器 -->
            <div class="pagination-container" v-if="filteredUsers.length">
                <button @click="previousPage" :disabled="currentPage === 1">上一页</button>
                <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
                <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
            </div>
        </div>

        <!-- 用户表单对话框 -->
        <div v-if="showModal" class="modal">
            <div class="modal-content">
                <h3>{{ isEditing ? '编辑用户' : '新增用户' }}</h3>
                <form @submit.prevent="submitForm">
                    <div>
                        <label>姓名:</label>
                        <input type="text" v-model="formData.name" required />
                    </div>
                    <div>
                        <label>密码:</label>
                        <input type="password" v-model="formData.password" required />
                    </div>
                    <div>
                        <label>邮箱:</label>
                        <input type="email" v-model="formData.email" required />
                    </div>
                    <div>
                        <label>性别:</label>
                        <select v-model="formData.gender">
                            <option value="male">男</option>
                            <option value="female">女</option>
                        </select>
                    </div>
                    <button type="submit">{{ isEditing ? '更新' : '添加' }}</button>
                    <button @click="closeModal">取消</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'UserManagement',
    data() {
        return {
            users: [],
            loading: false,
            searchQuery: '',
            currentPage: 1,
            itemsPerPage: 10,
            showModal: false,
            isEditing: false,
            formData: this.getInitialFormData()
        };
    },
    computed: {
        filteredUsers() {
            if (!this.searchQuery) return this.users;
            const query = this.searchQuery.toLowerCase();
            return this.users.filter(user =>
                user.name.toLowerCase().includes(query) ||
                user.email.toLowerCase().includes(query)
            );
        },
        paginatedUsers() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredUsers.slice(start, start + this.itemsPerPage);
        },
        totalPages() {
            return Math.ceil(this.filteredUsers.length / this.itemsPerPage);
        }
    },
    methods: {
        async fetchUsers() {
            this.loading = true;
            try {
                const response = await axios.get('http://127.0.0.1:5000/getAllUsers');
                if (response.data.status === 'success') {
                    this.users = response.data.users.map(user => ({
                        id: user[0],
                        name: user[1],
                        email: user[3],
                        gender: user[4] === 'male' ? '男' : '女'
                    }));
                } else {
                    alert(response.data.message || '获取用户数据失败');
                }
            } catch (error) {
                alert('无法连接到服务器');
                console.error('Error fetching users:', error);
            } finally {
                this.loading = false;
            }
        },

        async deleteUser(userId) {
            try {
                const response = await axios.delete(`http://127.0.0.1:5000/deleteUser/${userId}`);
                if (response.data.status === 'success') {
                    alert('删除成功');
                    await this.fetchUsers();
                } else {
                    alert(response.data.message || '删除用户失败');
                }
            } catch (error) {
                alert('无法连接到服务器');
                console.error('Error deleting user:', error);
            }
        },

        async submitForm() {
            const url = this.isEditing
                ? `http://127.0.0.1:5000/updateUser/${this.formData.id}`
                : 'http://127.0.0.1:5000/addUser';
            const method = this.isEditing ? 'put' : 'post';

            try {
                const response = await axios({ method, url, data: this.formData });
                if (response.data.status === 'success') {
                    alert(this.isEditing ? '更新成功' : '添加成功');
                    this.showModal = false;
                    await this.fetchUsers();
                } else {
                    alert(response.data.message || (this.isEditing ? '更新失败' : '添加失败'));
                }
            } catch (error) {
                alert('无法连接到服务器');
                console.error('Error submitting form:', error);
            }
        },

        editUser(user) {
            this.formData = {
                id: user.id,
                name: user.name,
                password: '',
                email: user.email,
                gender: user.gender === '男' ? 'male' : 'female'
            };
            this.isEditing = true;
            this.showModal = true;
        },

        openModal() {
            this.formData = this.getInitialFormData();
            this.isEditing = false;
            this.showModal = true;
        },

        getInitialFormData() {
            return {
                id: null,
                name: '',
                password: '',
                email: '',
                gender: 'male'
            };
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
        },

        confirmDelete(user) {
            if (confirm(`确认删除用户 "${user.name}" 吗？`)) {
                this.deleteUser(user.id);
            }
        },

        closeModal() {
            this.showModal = false;
            this.formData = this.getInitialFormData();
        }
    },
    mounted() {
        this.fetchUsers();
    }
};
</script>
<style scoped>
.user-management {
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
    transition: all 0.3s;
    width: 200px;
}

.search-box input:focus {
    border-color: #1890ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    outline: none;
}

button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    background: #1890ff;
    color: white;
    cursor: pointer;
    transition: all 0.3s;
}

button:hover {
    background: #40a9ff;
    box-shadow: 0 2px 8px rgba(24, 144, 255, 0.2);
}

.main-content {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.user-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.user-table th {
    background: #fafafa;
    padding: 16px;
    text-align: left;
    font-weight: 500;
    color: rgba(0, 0, 0, 0.85);
    border-bottom: 1px solid #f0f0f0;
}

.user-table td {
    padding: 16px;
    border-bottom: 1px solid #f0f0f0;
}

.user-table tr:hover {
    background: #fafafa;
}

/* 编辑和删除按钮 */
.user-table .edit-btn {
    background: #52c41a;
    padding: 4px 12px;
    margin-right: 8px;
}

.user-table .delete-btn {
    background: #ff4d4f;
    padding: 4px 12px;
}

.empty-state {
    text-align: center;
    padding: 40px 0;
    color: rgba(0, 0, 0, 0.45);
}

.pagination-container {
    padding: 15px;
    text-align: right;
    background: #fff;
    border-top: 1px solid #f0f0f0;
}

.pagination-container button {
    margin: 0 4px;
    background: #fff;
    color: rgba(0, 0, 0, 0.65);
    border: 1px solid #d9d9d9;
}

.pagination-container button:disabled {
    background: #f5f5f5;
    color: rgba(0, 0, 0, 0.25);
    cursor: not-allowed;
}

.pagination-container span {
    margin: 0 15px;
    color: rgba(0, 0, 0, 0.65);
}

/* 模态框样式 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.45);
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeIn 0.3s;
}

.modal-content {
    background: #fff;
    padding: 24px;
    border-radius: 8px;
    width: 420px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    animation: slideIn 0.3s;
}

.modal-content h3 {
    margin: 0 0 24px;
    color: rgba(0, 0, 0, 0.85);
    font-size: 16px;
    font-weight: 500;
}

.modal-content form>div {
    margin-bottom: 24px;
}

.modal-content label {
    display: block;
    margin-bottom: 8px;
    color: rgba(0, 0, 0, 0.85);
}

.modal-content input,
.modal-content select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #d9d9d9;
    border-radius: 4px;
    transition: all 0.3s;
}

.modal-content input:focus,
.modal-content select:focus {
    border-color: #40a9ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    outline: none;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

/* Loader样式 */
.loader {
    text-align: center;
    padding: 40px;
    color: #1890ff;
}

/* 表格内的操作按钮 */
.user-table button {
    margin: 0 5px;
    padding: 5px 10px;
    font-size: 12px;
}

.user-table button:first-child {
    background: #52c41a;
}

.user-table button:last-child {
    background: #f5222d;
}

/* 添加或修改以下样式 */
.user-management {
    padding: 20px;
    background-color: #0d1b30;
    /* 深色背景 */
    min-height: 100vh;
    color: #fff;
}

.header-actions {
    background: #1b2d4a;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
}

.search-box input {
    background: #263b5b;
    color: #fff;
    border: 1px solid #52a2e4;
    padding: 10px 15px;
}

.search-box input::placeholder {
    color: #8695b7;
}

button {
    background: #52a2e4;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    transition: all 0.3s;
}

button:hover {
    background: #3889d4;
    box-shadow: 0 2px 8px rgba(82, 162, 228, 0.3);
}

.main-content {
    background: #1b2d4a;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    margin-top: 20px;
}

.user-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    color: #fff;
}

.user-table th {
    background: #263b5b;
    padding: 16px;
    text-align: left;
    font-weight: 500;
    border-bottom: 1px solid #304769;
}

.user-table td {
    padding: 16px;
    border-bottom: 1px solid #304769;
}

.user-table tr:hover {
    background: #263b5b;
}

/* 编辑和删除按钮样式 */
.user-table button:first-child {
    background: #52a2e4;
}

.user-table button:last-child {
    background: #e74c3c;
}

/* 分页控件样式 */
.pagination-container {
    padding: 15px;
    text-align: right;
    background: #1b2d4a;
    border-top: 1px solid #304769;
    color: #fff;
}

.pagination-container button {
    background: #263b5b;
    color: #fff;
    border: 1px solid #52a2e4;
    margin: 0 4px;
}

.pagination-container button:disabled {
    background: #1b2d4a;
    color: #8695b7;
    border: 1px solid #304769;
}

/* 模态框样式 */
.modal-content {
    background: #1b2d4a;
    color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.modal-content input,
.modal-content select {
    background: #263b5b;
    color: #fff;
    border: 1px solid #52a2e4;
}

.modal-content input:focus,
.modal-content select:focus {
    border-color: #52a2e4;
    box-shadow: 0 0 0 2px rgba(82, 162, 228, 0.2);
}

/* 添加新的动画效果 */
@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.loader {
    color: #52a2e4;
}
</style>
