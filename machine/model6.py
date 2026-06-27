import os
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine, text
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置临时文件夹
os.environ['JOBLIB_TEMP_FOLDER'] = 'D:/model'

# 数据库连接
conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())


def tokensize(text):
    """对文本进行分词并删除停用词"""
    words = [word for word in jieba.cut(text) if word not in stopwords]
    return ' '.join(words)


def getData():
    """从数据库获取数据"""
    try:
        with conn.connect() as connection:
            query = text('SELECT * FROM cases')
            df = pd.read_sql(query, con=connection, index_col='id')
            data = df[['content', 'type']].copy()
            data['content'] = data['content'].apply(tokensize)
            logging.info(f"Data loaded successfully. Shape: {data.shape}")
            return data
    except Exception as e:
        logging.error(f"An error occurred while fetching data: {e}")
        return None


def model_train(data):
    """训练模型并评估性能"""
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))  # 减少特征数量
    try:
        # 先将数据向量化
        X = vectorizer.fit_transform(data['content'])
        y = data['type']

        logging.info(f"Training data vectorized. Shape: {X.shape}")

        # K折交叉验证
        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        train_accuracies = []
        validation_accuracies = []


        model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)  # 减少树的数量和深度

        for train_index, val_index in kf.split(X):
            X_train, X_val = X[train_index], X[val_index]
            y_train, y_val = y.iloc[train_index], y.iloc[val_index]

            model.fit(X_train, y_train)

            # 计算训练和验证准确率
            train_pred = model.predict(X_train)
            val_pred = model.predict(X_val)

            train_accuracy = accuracy_score(y_train, train_pred)
            val_accuracy = accuracy_score(y_val, val_pred)

            train_accuracies.append(train_accuracy)
            validation_accuracies.append(val_accuracy)

        return train_accuracies, validation_accuracies
    except Exception as e:
        logging.error(f"An error occurred during model training: {e}")
        return None, None


def plot_k_fold_results(train_accuracies, validation_accuracies):
    """绘制 K 折交叉验证的训练和验证准确率折线图"""
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(train_accuracies) + 1), train_accuracies, marker='o', label='Training Accuracy', color='blue')
    plt.plot(range(1, len(validation_accuracies) + 1), validation_accuracies, marker='x', label='Validation Accuracy', color='orange')

    plt.title('K-Fold Cross-Validation Accuracy')
    plt.xlabel('Fold')
    plt.ylabel('Accuracy')
    plt.ylim(0, 1)
    plt.xticks(range(1, len(train_accuracies) + 1))  # 设置 x 轴刻度
    plt.legend()
    plt.grid()
    plt.show()


# 主程序
if __name__ == '__main__':
    data = getData()
    if data is not None:
        train_accuracies, validation_accuracies = model_train(data)

        # 添加处理None的逻辑
        if train_accuracies is not None and validation_accuracies is not None:
            plot_k_fold_results(train_accuracies, validation_accuracies)  # 绘制 K 折交叉验证准确率图
        else:
            print("Model training failed, metrics are not available.")
