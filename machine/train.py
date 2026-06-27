import os
import matplotlib.pyplot as plt
import seaborn as sns
import jieba
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import create_engine, text
from tensorflow import keras
from tensorflow.keras import layers

# 数据库连接
conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())
vectorizer = TfidfVectorizer(max_features=10000)


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


def train_and_evaluate_models(data):
    # 数据分割
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
    x_train_vectorized = vectorizer.fit_transform(x_train)
    x_test_vectorized = vectorizer.transform(x_test)

    # 将目标变量转换为数值型
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.transform(y_test)

    # 定义模型
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'SVM': SVC(kernel='linear', random_state=42),
        'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'DecisionTree': DecisionTreeClassifier(random_state=42),  # 添加决策树模型
        'NeuralNetwork': create_neural_network_model(x_train_vectorized.shape[1])  # 添加神经网络模型
    }

    results = {}

    # 训练和评估每个模型
    for name, model in models.items():
        if name == 'NeuralNetwork':
            model.fit(x_train_vectorized.toarray(), y_train, epochs=10, batch_size=32, verbose=0)
            y_pred_prob = model.predict(x_test_vectorized.toarray())
            y_pred = (y_pred_prob > 0.5).astype(int)  # 将概率转为标签
        else:
            model.fit(x_train_vectorized, y_train)
            y_pred = model.predict(x_test_vectorized)

        # 计算评估指标
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }

    return results


def create_neural_network_model(input_dim):
    # 创建一个简单的神经网络模型
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_dim=input_dim),
        layers.Dropout(0.5),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # 输出层，二分类问题
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model


def plot_results(results):
    # 将结果转换为 DataFrame 方便绘图
    metrics_df = pd.DataFrame.from_dict(results, orient='index')
    metrics_df = metrics_df.reset_index().rename(columns={'index': 'Model'})

    # 设置绘图风格
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))

    # 绘制柱状图
    for i, metric in enumerate(['accuracy', 'precision', 'recall', 'f1'], 1):
        plt.subplot(2, 2, i)
        sns.barplot(x='Model', y=metric, data=metrics_df, palette='viridis', hue='Model', legend=False)
        plt.title(f'{metric.capitalize()} Comparison')
        plt.ylim(0, 1)  # 设置 y 轴范围
        plt.ylabel(metric.capitalize())
        plt.xlabel('Model')

    plt.tight_layout()

    # 保存为当前目录的图片
    plt.savefig('model_performance_comparison.png')
    plt.show()  # 显示图片


def compare_models():
    trainData = getData()
    if trainData is None or trainData.empty:
        print("Failed to retrieve training data")
        return

    # 训练和评估模型
    results = train_and_evaluate_models(trainData)

    # 打印结果
    for model_name, metrics in results.items():
        print(f"{model_name} Performance:")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1 Score: {metrics['f1']:.4f}")
        print("-" * 30)

    # 绘制性能对比图
    plot_results(results)


# 运行对比分析
compare_models()
