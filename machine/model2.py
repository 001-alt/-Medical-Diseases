import os
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, recall_score
from sqlalchemy import create_engine, text
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置临时文件夹，避免使用默认路径
os.environ['JOBLIB_TEMP_FOLDER'] = 'C:/temp'  # 请确保此路径存在，并且没有特殊字符

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
            data = df[['content', 'type']].copy()  # 复制 DataFrame，避免因切片引发的问题
            data['content'] = data['content'].apply(tokensize)
            logging.info("Data loaded successfully.")
            return data
    except Exception as e:
        logging.error(f"An error occurred while fetching data: {e}")
        return None


vectorizer = TfidfVectorizer(max_features=10000)


def model_train(data):
    """训练模型并评估性能"""
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)

    # 向量化训练集
    x_train_vectorized = vectorizer.fit_transform(x_train)

    # 使用 GridSearchCV 进行超参数优化
    param_grid = {
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [3, 5, 10],
        'min_samples_leaf': [2, 2, 4]
    }

    model = GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=1,  # 将 n_jobs 设置为 1 以避免并行计算引起的问题
        verbose=1
    )

    model.fit(x_train_vectorized, y_train)

    # 向量化测试集
    x_test_vectorized = vectorizer.transform(x_test)
    y_pred = model.predict(x_test_vectorized)

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average='weighted')
    logging.info(f"Best Parameters: {model.best_params_}")
    return accuracy, recall


def plot_results(accuracy, recall):
    """绘制模型性能图"""
    plt.bar(['Accuracy', 'Recall'], [accuracy, recall], color=['blue', 'orange'])
    plt.ylim(0, 1)
    plt.title('Model Performance')
    plt.ylabel('Score')
    plt.show()


# 主程序
if __name__ == '__main__':
    data = getData()
    if data is not None:
        accuracy, recall = model_train(data)
        print(f"Optimized Model Accuracy: {accuracy:.4f}")
        print(f"Optimized Model Recall: {recall:.4f}")
        plot_results(accuracy, recall)
