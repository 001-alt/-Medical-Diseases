# 🏥 医疗疾病大数据分析系统

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Vue.js-2.x-brightgreen?logo=vue.js" alt="Vue">
  <img src="https://img.shields.io/badge/Flask-2.3-lightgrey?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql" alt="MySQL">
  <img src="https://img.shields.io/badge/Scikit--learn-1.3-yellow?logo=scikitlearn" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

---

## 📖 项目简介

基于 **Flask + Vue.js + MySQL** 的综合性医疗大数据分析平台，集成网络爬虫、机器学习预测与可视化仪表盘，辅助医疗机构洞察疾病趋势、优化诊疗决策。

> ✨ 核心亮点：自动化数据采集 → 智能分析建模 → 多维度可视化 → 用户权限管理，一站式闭环。

---

## 🧩 功能模块

| 模块 | 描述 |
|------|------|
| 🔍 **智能爬虫** | Selenium 驱动的自动化采集，支持多源医学数据库 |
| 🧠 **机器学习** | 决策树 / 随机森林模型，TF-IDF 文本向量化预测 |
| 📊 **可视化大屏** | ECharts 图表 + DataV 组件，实时仪表盘监控 |
| 👤 **用户系统** | JWT 认证、角色管理、操作日志审计 |
| 🗄️ **数据管理** | MySQL 存储 + CRUD 接口，支持病例检索导出 |

---

## 🛠️ 技术栈

### 后端

| 技术 | 用途 |
|------|------|
| Python 3.8 | 主语言 |
| Flask | Web 框架 & RESTful API |
| SQLAlchemy / PyMySQL | 数据库 ORM 与连接 |
| Scikit-learn | 决策树 & 随机森林建模 |
| Pandas / NumPy | 数据处理与分析 |
| Selenium | 网页数据自动化采集 |
| Flask-JWT-Extended | 用户认证与权限 |

### 前端

| 技术 | 用途 |
|------|------|
| Vue.js 2.x | 响应式 SPA 框架 |
| Vue Router / Vuex | 路由 & 状态管理 |
| ECharts 5 + DataV | 数据可视化大屏 |
| Element UI | 组件库 |
| Axios | HTTP 通信 |

### 数据库

| 表名 | 说明 |
|------|------|
| `cases` / `cases_copy1` | 病例原始数据 |
| `users` | 用户账户信息 |
| `predictions` | 模型预测历史 |
| `operation_logs` | 操作审计日志 |

---

## 🚀 快速开始

### 环境要求

- **Python** ≥ 3.8（推荐使用 Conda）
- **Node.js** ≥ 14
- **MySQL** ≥ 8.0
- **Chrome** 浏览器（爬虫采集用）

### 1. 克隆仓库

```bash
git clone https://github.com/001-alt/-Medical-Diseases.git
cd -Medical-Diseases
```

### 2. 创建 Python 虚拟环境（Conda）

```bash
conda create -p ./env python=3.8 -y
conda activate ./env
pip install -r requirements.txt
```

### 3. 配置 MySQL 数据库

```sql
CREATE DATABASE IF NOT EXISTS medicalinfo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `app.py` 和 `utils/query.py` 中的数据库连接信息：

```python
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='你的密码',  # ← 改为你的 MySQL 密码
    database='medicalinfo',
    port=3306,
    charset='utf8mb4'
)
```

### 4. 启动后端

```bash
python app.py
# 默认运行在 http://localhost:5000
```

### 5. 启动前端

```bash
cd front-end-template-1-master
npm install
npm run serve
# 默认运行在 http://localhost:8080
```

### 6. 访问系统

浏览器打开 **http://localhost:8080** 即可进入可视化界面。

---

## 🔑 默认管理员

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | `admin` | `admin123` |

> ⚠️ 首次登录后请及时修改默认密码。

---

## 📁 项目结构

```
├── app.py                  # Flask 主入口
├── requirements.txt        # Python 依赖清单
├── utils/                  # 工具函数
│   ├── query.py            # 数据库操作封装
│   ├── getAllData.py       # 数据分析函数
│   └── getPublicData.py    # 公共数据查询
├── machine/                # 机器学习模块
│   ├── tree.py             # 决策树 & 随机森林
│   ├── model/              # 训练好的模型文件 (.pkl)
│   └── visualizations/     # 模型可视化图片
├── spiders/                # 爬虫脚本
│   ├── spiderMain.py       # 主爬虫
│   └── chromedriver.exe    # Chrome 驱动
├── templates/              # Flask 模板页
├── front-end-template-1-master/  # Vue.js 前端
│   ├── src/views/          # 页面组件
│   ├── src/components/     # 通用组件
│   └── src/router/         # 路由配置
└── env/                    # Conda 虚拟环境（Git 忽略）
```

---

## 🖼️ 功能截图

> *启动项目后在此处放置界面截图*

- 首页数据大屏：年龄分布饼图、性别比例、疾病词云
- 病例数据表格：分页浏览、Excel 导出
- 机器学习预测：输入症状文本，输出疾病类型预测
- 用户管理：增删改查、角色分配、操作日志

---

## 🔮 待规划

- [ ] 集成深度学习模型（LSTM / Transformer）提升预测精度
- [ ] Docker 容器化部署
- [ ] 移动端适配优化
- [ ] 数据导出支持 PDF / Word 格式
- [ ] CI/CD 自动化测试与部署

---

## 📄 License

 © [001-alt](https://github.com/001-alt)
