<template>
    <div class="predictions-container">

        <div class="controls">
            <input v-model="searchQuery" class="search-input" placeholder="搜索文本内容..." @input="handleSearch" />

            <button class="refresh-btn" @click="fetchPredictions" :disabled="loading" :class="{ 'loading': loading }">
                <span v-if="!loading">⟳ 刷新数据</span>
                <span v-else>⏳ 加载中...</span>
            </button>
        </div>

        <div v-if="error" class="error-message">
            ⚠️ {{ error }}
        </div>

        <div v-if="filteredPredictions.length > 0" class="table-container">
            <table class="predictions-table">
                <thead>
                    <tr>
                        <th>输入文本</th>
                        <th>预测结果</th>
                        <th>创建时间</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(prediction, index) in paginatedPredictions" :key="index">
                        <td class="text-cell">{{ prediction.input_text }}</td>
                        <td>
                            <span class="result-tag" :class="getTagClass(prediction.prediction_result)">
                                {{ prediction.prediction_result }}
                            </span>
                        </td>
                        <td class="time-cell">{{ formatDate(prediction.created_at) }}</td>
                        <td class="action-cell">
                            <button class="action-btn details-btn" @click="handleDetails(prediction)">
                                详情
                            </button>
                            <button class="action-btn copy-btn" @click="handleCopy(prediction)">
                                复制
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="pagination">
                <button class="page-btn" @click="prevPage" :disabled="currentPage === 1">
                    « 上一页
                </button>
                <span class="page-info">第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
                <button class="page-btn" @click="nextPage" :disabled="currentPage >= totalPages">
                    下一页 »
                </button>
            </div>
        </div>

        <div v-if="filteredPredictions.length === 0 && !loading" class="empty-state">
            <div class="empty-icon">⎗</div>
            <p>暂无数据</p>
        </div>

        <div v-if="dialogVisible" class="dialog-overlay" @click="dialogVisible = false">
            <div class="detail-dialog" @click.stop>
                <h3 class="dialog-title">🛈 预测详情</h3>
                <div class="dialog-content">
                    <div class="detail-item">
                        <label>输入文本:</label>
                        <p>{{ selectedRow.input_text }}</p>
                    </div>
                    <div class="detail-item">
                        <label>预测结果:</label>
                        <p>{{ selectedRow.prediction_result }}</p>
                    </div>
                    <div class="detail-item">
                        <label>创建时间:</label>
                        <p>{{ formatDate(selectedRow.created_at) }}</p>
                    </div>
                </div>
                <button class="close-btn" @click="dialogVisible = false">
                    关闭
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/services/api';

export default {
    name: 'BeautifulPredictionsTable',
    data() {
        return {
            predictions: [],
            loading: false,
            error: null,
            currentPage: 1,
            itemsPerPage: 8,  // 修改为每页显示8条
            searchQuery: '',
            dialogVisible: false,
            selectedRow: {},
        };
    },
    computed: {
        // 排序后的预测结果（最新排前面）
        sortedPredictions() {
            return [...this.predictions].sort((a, b) => {
                return new Date(b.created_at) - new Date(a.created_at);
            });
        },

        filteredPredictions() {
            if (!this.searchQuery) return this.sortedPredictions;
            return this.sortedPredictions.filter(item =>
                item.input_text.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                item.prediction_result.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
        paginatedPredictions() {
            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return this.filteredPredictions.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.filteredPredictions.length / this.itemsPerPage);
        },
    },
    methods: {
        async fetchPredictions() {
            this.loading = true;
            this.error = null;

            try {
                const response = await api.getPredictions();

                if (response.data.code === 200) {
                    this.predictions = response.data.data;
                } else {
                    throw new Error(response.data.message);
                }
            } catch (err) {
                this.error = '获取预测数据失败，请稍后再试';
            } finally {
                this.loading = false;
            }
        },

        formatDate(date) {
            return new Date(date).toLocaleString();
        },

        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },

        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },

        handlePageChange(page) {
            if (page > 0 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },

        handleSearch() {
            this.currentPage = 1;
        },

        handleDetails(row) {
            this.selectedRow = row;
            this.dialogVisible = true;
        },

        async handleCopy(row) {
            try {
                await navigator.clipboard.writeText(row.input_text);
                alert('复制成功');
            } catch (err) {
                alert('复制失败');
            }
        },

        getTagClass(result) {
            const classes = {
                '腺性间变': 'success-tag',
                '鳞性间变': 'warning-tag',
                '其他': 'info-tag',
            };
            return classes[result] || 'info-tag';
        },
    },
    created() {
        this.fetchPredictions();
    },
};
</script>

<!-- 样式部分保持不变 -->


<style scoped>
/* 基础样式 */
.predictions-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: #333;
}

.page-title {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 2rem;
    font-size: 1.8rem;
    font-weight: 600;
}

.controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    align-items: center;
}

/* 搜索框样式 */
.search-input {
    flex-grow: 1;
    padding: 0.6rem 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    font-size: 1rem;
    transition: all 0.3s;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.search-input:focus {
    outline: none;
    border-color: #4285f4;
    box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
}

/* 按钮样式 */
.refresh-btn,
.action-btn,
.page-btn,
.close-btn {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

.refresh-btn {
    background-color: #4285f4;
    color: white;
}

.refresh-btn:hover:not(:disabled) {
    background-color: #3367d6;
}

.refresh-btn:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.refresh-btn.loading {
    opacity: 0.7;
}

.action-btn {
    padding: 0.4rem 0.8rem;
    margin: 0.2rem;
}

.details-btn {
    background-color: #5cb85c;
    color: white;
}

.details-btn:hover {
    background-color: #449d44;
}

.copy-btn {
    background-color: #5bc0de;
    color: white;
}

.copy-btn:hover {
    background-color: #31b0d5;
}

/* 表格样式 */
.table-container {
    overflow-x: auto;
    margin: 1.5rem 0;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.predictions-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.predictions-table th {
    background-color: #f8f9fa;
    color: #495057;
    text-align: left;
    padding: 1rem;
    font-weight: 600;
    border-bottom: 2px solid #e9ecef;
    position: sticky;
    top: 0;
}

.predictions-table td {
    padding: 1rem;
    border-bottom: 1px solid #e9ecef;
}

.predictions-table tr:hover td {
    background-color: #f8f9fa;
}

.text-cell {
    max-width: 400px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.time-cell {
    white-space: nowrap;
}

/* 结果标签样式 */
.result-tag {
    display: inline-block;
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
    font-size: 0.85rem;
    font-weight: 500;
    color: white;
}

.success-tag {
    background-color: #5cb85c;
}

.warning-tag {
    background-color: #f0ad4e;
}

.info-tag {
    background-color: #5bc0de;
}

/* 分页样式 */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    gap: 1rem;
}

.page-btn {
    background-color: #f8f9fa;
    color: #495057;
    border: 1px solid #ddd;
}

.page-btn:hover:not(:disabled) {
    background-color: #e9ecef;
}

.page-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.page-info {
    font-size: 0.9rem;
    color: #6c757d;
}

/* 空状态 */
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #6c757d;
}

.empty-icon {
    width: 100px;
    height: 100px;
    margin-bottom: 1rem;
    opacity: 0.6;
}

/* 错误提示 */
.error-message {
    background-color: #f8d7da;
    color: #721c24;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}

/* 对话框样式 */
.dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.detail-dialog {
    background-color: white;
    border-radius: 8px;
    width: 90%;
    max-width: 600px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    animation: fadeIn 0.3s ease;
}

.dialog-title {
    margin-top: 0;
    margin-bottom: 1.5rem;
    color: #2c3e50;
    font-size: 1.3rem;
}

.dialog-content {
    margin-bottom: 1.5rem;
}

.detail-item {
    margin-bottom: 1rem;
}

.detail-item label {
    display: block;
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: #495057;
}

.detail-item p {
    margin: 0;
    padding: 0.5rem;
    background-color: #f8f9fa;
    border-radius: 4px;
}

.close-btn {
    background-color: #6c757d;
    color: white;
    float: right;
}

.close-btn:hover {
    background-color: #5a6268;
}

/* 动画效果 */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 响应式设计 */
@media (max-width: 768px) {
    .controls {
        flex-direction: column;
        align-items: stretch;
    }

    .predictions-container {
        padding: 1rem;
    }

    .predictions-table th,
    .predictions-table td {
        padding: 0.75rem;
    }
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #b0bec5;
}

/* 主容器样式 */
.predictions-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
    background-color: #0d1b30;
    color: #fff;
}

/* 搜索框样式 */
.search-input {
    background: #1b2d4a;
    border: 1px solid #52a2e4;
    color: #fff;
    padding: 0.8rem 1rem;
}

.search-input:focus {
    border-color: #52a2e4;
    box-shadow: 0 0 0 2px rgba(82, 162, 228, 0.2);
}

/* 刷新按钮样式 */
.refresh-btn {
    background-color: #52a2e4;
    color: white;
    border: none;
}

.refresh-btn:hover:not(:disabled) {
    background-color: #3889d4;
}

/* 表格容器样式 */
.table-container {
    background: #1b2d4a;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

/* 表格样式 */
.predictions-table th {
    background-color: #263b5b;
    color: #fff;
    border-bottom: 2px solid #304769;
}

.predictions-table td {
    border-bottom: 1px solid #304769;
    color: #fff;
}

.predictions-table tr:hover td {
    background-color: #263b5b;
}

/* 结果标签样式 */
.result-tag {
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
}

.success-tag {
    background-color: #52a2e4;
}

.warning-tag {
    background-color: #e6a23c;
}

.info-tag {
    background-color: #909399;
}

/* 详情和复制按钮 */
.details-btn {
    background-color: #52a2e4;
}

.copy-btn {
    background-color: #409EFF;
}

/* 分页控件样式 */
.pagination {
    background: #1b2d4a;
}

.page-btn {
    background-color: #263b5b;
    color: #fff;
    border: 1px solid #52a2e4;
}

.page-btn:hover:not(:disabled) {
    background-color: #304769;
}

.page-info {
    color: #fff;
}

/* 对话框样式 */
.detail-dialog {
    background-color: #1b2d4a;
    color: #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.dialog-title {
    color: #fff;
}

.detail-item label {
    color: #fff;
}

.detail-item p {
    background-color: #263b5b;
    color: #fff;
}

/* 空状态样式 */
.empty-state {
    color: #8695b7;
}

/* 错误消息样式 */
.error-message {
    background-color: #ff4d4f1a;
    color: #ff4d4f;
    border: 1px solid #ff4d4f;
}
</style>
