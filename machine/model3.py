import jieba
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sqlalchemy import create_engine, text

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
            data = df[['content', 'type']].copy()  # 复制 DataFrame，避免因切片引发的问题
            data['content'] = data['content'].apply(tokensize)  # 使用 .loc 方法避免警告
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


vectorizer = TfidfVectorizer(max_features=10000)


def model_train(data):
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)

    x_train_vectorized = vectorizer.fit_transform(x_train)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(x_train_vectorized, y_train)

    y_pred = model.predict(vectorizer.transform(x_test))
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')  # 计算 F1 Score
    return accuracy, recall, f1


def plot_results(accuracy, recall, f1):
    """绘制模型性能图"""
    metrics = [accuracy, recall, f1]
    labels = ['Accuracy', 'Recall', 'F1 Score']

    plt.bar(labels, metrics, color=['blue', 'orange', 'green'])
    plt.ylim(0, 1)
    plt.title('Model Performance')
    plt.ylabel('Score')

    # 设置 y 轴的刻度为 0.05 的倍数
    plt.yticks([i * 0.05 for i in range(21)])  # 0.00, 0.05, ..., 1.00

    plt.show()


# 主程序
if __name__ == '__main__':
    data = getData()
    if data is not None:
        accuracy, recall, f1 = model_train(data)
        print(f"Original Model Accuracy: {accuracy:.4f}")
        print(f"Original Model Recall: {recall:.4f}")
        print(f"Original Model F1 Score: {f1:.4f}")

        plot_results(accuracy, recall, f1)  # 绘制性能图

# import jieba
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import accuracy_score, recall_score, f1_score
# from sqlalchemy import create_engine, text
# from sklearn.metrics import log_loss
# import numpy as np
#
# # 数据库连接
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
# stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())
#
#
# def tokensize(text):
#     words = [word for word in jieba.cut(text) if word not in stopwords]
#     return ' '.join(words)
#
#
# def getData():
#     try:
#         with conn.connect() as connection:
#             query = text('SELECT * FROM cases')
#             df = pd.read_sql(query, con=connection, index_col='id')
#             data = df[['content', 'type']].copy()  # 复制 DataFrame，避免因切片引发的问题
#             data['content'] = data['content'].apply(tokensize)  # 使用 .loc 方法避免警告
#             return data
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#
#
# vectorizer = TfidfVectorizer(max_features=10000)
#
#
# def model_train(data):
#     x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
#
#     x_train_vectorized = vectorizer.fit_transform(x_train)
#     model = DecisionTreeClassifier(random_state=42)
#     model.fit(x_train_vectorized, y_train)
#
#     # 记录损失值
#     y_pred_prob = model.predict_proba(x_train_vectorized)
#     loss = log_loss(y_train, y_pred_prob)
#
#     y_pred = model.predict(vectorizer.transform(x_test))
#     accuracy = accuracy_score(y_test, y_pred)
#     recall = recall_score(y_test, y_pred, average='weighted')
#     f1 = f1_score(y_test, y_pred, average='weighted')
#
#     return accuracy, recall, f1, loss
#
#
# def plot_results(accuracy, recall, f1, loss):
#     """绘制模型性能和损失的折线图"""
#     metrics = [accuracy, recall, f1]
#     labels = ['Accuracy', 'Recall', 'F1 Score']
#
#     # 绘制性能图
#     plt.figure(figsize=(10, 5))
#
#     plt.subplot(1, 2, 1)  # 第一幅图
#     plt.plot(labels, metrics, marker='o', linestyle='-', color='b')
#     plt.ylim(0, 1)
#     plt.title('Model Performance')
#     plt.ylabel('Score')
#     plt.grid(True)
#
#     # 绘制损失函数图
#     plt.subplot(1, 2, 2)  # 第二幅图
#     plt.plot([1], [loss], marker='o', color='r', label='Loss')
#     plt.title('Loss Function')
#     plt.ylabel('Loss')
#     plt.xticks([])  # 不显示 x 轴的刻度
#     plt.grid(True)
#
#     plt.tight_layout()
#     plt.show()
#
#
# # 主程序
# if __name__ == '__main__':
#     data = getData()
#     if data is not None:
#         accuracy, recall, f1, loss = model_train(data)
#         print(f"Original Model Accuracy: {accuracy:.4f}")
#         print(f"Original Model Recall: {recall:.4f}")
#         print(f"Original Model F1 Score: {f1:.4f}")
#         print(f"Model Log Loss: {loss:.4f}")
#
#         plot_results(accuracy, recall, f1, loss)  # 绘制性能和损失图

