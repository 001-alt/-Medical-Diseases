import jieba
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, log_loss
from sqlalchemy import create_engine, text
from sklearn.tree import plot_tree
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
import os

# 创建保存图片的目录
os.makedirs('visualizations', exist_ok=True)

# 设置中文字体和图表样式
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
plt.style.use('ggplot')

# 数据库连接
conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())


def tokensize(text):
    words = [word for word in jieba.cut(text) if word not in stopwords]
    return ' '.join(words)


def getData():
    try:
        with conn.connect() as connection:
            query = text('SELECT * FROM cases')
            df = pd.read_sql(query, con=connection, index_col='id')
            data = df[['content', 'type']]
            data.loc[:, 'content'] = data['content'].apply(tokensize)
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


vectorizer = TfidfVectorizer(max_features=10000)


def save_decision_tree(model, le, vectorizer):
    """保存决策树结构图"""
    plt.figure(figsize=(20, 10))
    plot_tree(model,
              max_depth=3,  # 只显示前3层避免过于密集
              filled=True,
              feature_names=vectorizer.get_feature_names_out(),
              class_names=le.classes_,
              fontsize=10,
              proportion=True,
              rounded=True)
    plt.title('决策树结构(前三层)', fontsize=14)
    plt.savefig('visualizations/decision_tree.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("决策树结构图已保存为 'visualizations/decision_tree.png'")


def save_decision_boundary(model, x_train_vectorized, y_train_encoded, le):
    """保存决策边界图"""
    plt.figure(figsize=(10, 8))

    # 降维到2D空间
    svd = TruncatedSVD(n_components=2)
    x_train_reduced = svd.fit_transform(x_train_vectorized)

    # 创建网格点
    h = .02
    x_min, x_max = x_train_reduced[:, 0].min() - 1, x_train_reduced[:, 0].max() + 1
    y_min, y_max = x_train_reduced[:, 1].min() - 1, x_train_reduced[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    # 预测网格点（近似）
    grid_proba = model.predict_proba(svd.inverse_transform(np.c_[xx.ravel(), yy.ravel()]))
    Z = grid_proba[:, 1].reshape(xx.shape)

    # 绘制决策边界
    plt.contourf(xx, yy, Z, alpha=0.8, cmap='Pastel2')

    # 绘制数据点
    scatter = plt.scatter(x_train_reduced[:, 0], x_train_reduced[:, 1],
                          c=y_train_encoded, cmap='Dark2',
                          edgecolors='k', s=60, alpha=0.7)

    # 添加图例和标签
    plt.legend(handles=scatter.legend_elements()[0],
               labels=list(le.classes_),
               title="疾病类型",
               bbox_to_anchor=(1.05, 1),
               loc='upper left')

    plt.title('决策边界可视化(SVD降维)', fontsize=14)
    plt.xlabel('主成分1', fontsize=12)
    plt.ylabel('主成分2', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.savefig('visualizations/decision_boundary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("决策边界图已保存为 'visualizations/decision_boundary.png'")


def save_feature_importance(model, vectorizer, top_n=15):
    """保存特征重要性图"""
    plt.figure(figsize=(12, 8))

    # 获取特征重要性
    importances = model.feature_importances_
    indices = np.argsort(importances)[-top_n:]
    features = vectorizer.get_feature_names_out()[indices]

    # 绘制水平条形图
    plt.barh(range(top_n), importances[indices], color='skyblue', edgecolor='black')
    plt.yticks(range(top_n), features, fontsize=10)
    plt.title(f'Top {top_n} 重要特征', fontsize=14)
    plt.xlabel('特征重要性得分', fontsize=12)
    plt.grid(True, axis='x', linestyle='--', alpha=0.6)

    # 在每个条形上添加数值标签
    for i, v in enumerate(importances[indices]):
        if v > 0.01:  # 只显示重要性大于1%的特征值
            plt.text(v + 0.005, i - 0.15, f"{v:.3f}", color='black', fontsize=9)

    plt.tight_layout()
    plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("特征重要性图已保存为 'visualizations/feature_importance.png'")


def model_train(data):
    # 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(
        data['content'],
        data['type'],
        test_size=0.2,
        random_state=42
    )

    # 特征提取
    x_train_vectorized = vectorizer.fit_transform(x_train)
    x_test_vectorized = vectorizer.transform(x_test)

    # 标签编码
    le = LabelEncoder()
    y_train_encoded = le.fit_transform(y_train)
    y_test_encoded = le.transform(y_test)

    # 使用决策树分类器
    model = DecisionTreeClassifier(random_state=42, max_depth=5)  # 限制深度便于可视化

    # 训练模型
    model.fit(x_train_vectorized, y_train_encoded)

    # 预测和评估
    y_pred = model.predict(x_test_vectorized)
    accuracy = accuracy_score(y_test_encoded, y_pred)
    print(f"\n模型准确率: {accuracy:.4f}")

    # 分别生成和保存三个可视化图表
    save_decision_tree(model, le, vectorizer)
    save_decision_boundary(model, x_train_vectorized, y_train_encoded, le)
    save_feature_importance(model, vectorizer)

    return model, le  # 返回模型和标签编码器以便后续使用


if __name__ == '__main__':
    data = getData()
    if data is not None:
        print("数据处理中...")
        model, label_encoder = model_train(data)
        print("\n所有可视化图表已生成并保存在 'visualizations' 文件夹中")
