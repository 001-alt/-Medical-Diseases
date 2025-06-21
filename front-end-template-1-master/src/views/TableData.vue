<template>
    <div class="tableData-container">
        <div class="button-group">
            <el-button type="primary" @click="downloadData">导出Excel</el-button>
        </div>
        <transition name="fade" mode="out-in">
            <dv-loading v-if="!config.data.length">
                loading
            </dv-loading>
            <div v-else class="content">
                <dv-scroll-board :config="config" style="width:85%;height:800px" />
            </div>
        </transition>
    </div>
</template>

<script>
import fileDownload from 'js-file-download'
import ExcelJS from 'exceljs'

export default {
    data() {
        return {
            config: {
                header: [],
                data: [],
                index: true,
                align: [],
                headerBGC: "#3077b1",
            },
            tableList: []
        }
    },
    async created() {
        await this.delay(1500)
        this.getTableList()
    },
    methods: {
        delay(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        },
        async getTableList() {
            const res = await this.$http.get('/tableData')
            this.tableList = res.data.resultData
            this.config.header = ['类型', '性别', '年龄', '时间', '描述', '求诊医生', '求诊医院', '求诊科室', '详细链接', '身高', '体重', '患病时间', '过敏史']
            this.config.data = res.data.resultData
            this.config.align = this.config.header.map(item => 'center')
            this.config.align.push('center')
            console.log('Config Data:', this.config.data)
            if (this.config.data.length === 0) {
                console.log('No data available')
            } else {
                console.log('Data sample:', this.config.data[0])
            }
        },
        async downloadData() {
            try {
                if (this.config.data.length === 0) {
                    alert('没有数据可以导出');
                    return;
                }

                const workbook = new ExcelJS.Workbook();
                const worksheet = workbook.addWorksheet('用户数据');

                const headerRow = worksheet.addRow();
                this.config.header.forEach((item, index) => {
                    const cell = headerRow.getCell(index + 1);
                    if (!cell) {
                        headerRow.createCell(index + 1).value = item;
                    } else {
                        cell.value = item;
                    }
                });

                this.config.data.forEach((row, rowIndex) => {
                    const dataRow = worksheet.addRow();
                    if (Array.isArray(row)) {
                        row.forEach((value, cellIndex) => {
                            const cell = dataRow.getCell(cellIndex + 1);
                            if (!cell) {
                                dataRow.createCell(cellIndex + 1).value = value;
                            } else {
                                cell.value = value;
                            }
                        });
                    } else if (row !== null && typeof row === 'object') {
                        Object.values(row).forEach((value, cellIndex) => {
                            const cell = dataRow.getCell(cellIndex + 1);
                            if (!cell) {
                                dataRow.createCell(cellIndex + 1).value = value;
                            } else {
                                cell.value = value;
                            }
                        });
                    } else {
                        console.warn('Unexpected data type:', typeof row);
                    }
                });

                const buffer = await workbook.xlsx.writeBuffer();
                const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                fileDownload(blob, '用户数据.xlsx');

                alert('数据导出成功');
            } catch (error) {
                console.error('下载Excel文件出错:', error);
                alert('数据导出失败，请检查控制台日志');
            }
        }
    }
}
</script>

<style scoped>
.content {
    display: flex;
    justify-content: center;
}

.button-group {
    margin: 20px 0;
    text-align: center;
}

.button-group .el-button {
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
    opacity: 0;
}
</style>
