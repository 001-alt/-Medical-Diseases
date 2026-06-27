import os
import jieba
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier  # 确保导入随机森林分类器
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sqlalchemy import create_engine, text
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 设置临时文件夹
os.environ['JOBLIB_TEMP_FOLDER'] = 'C:/temp'

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
    vectorizer = TfidfVectorizer(max_features=15000, ngram_range=(1, 2))  # 在此定义vectorizer
    try:
        x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2,
                                                            random_state=42)
        x_train_vectorized = vectorizer.fit_transform(x_train)
        logging.info(f"Training data vectorized. Shape: {x_train_vectorized.shape}")

        param_grid = {
            'n_estimators': [10],
            'max_depth': [None],
            'min_samples_split': [2],
            'min_samples_leaf': [1]
        }

        model = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=2, scoring='accuracy', n_jobs=1,
                             verbose=1)
        model.fit(x_train_vectorized, y_train)

        x_test_vectorized = vectorizer.transform(x_test)
        y_pred = model.predict(x_test_vectorized)

        accuracy = accuracy_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')
        logging.info(f"Best Parameters: {model.best_params_}")
        return accuracy, recall, f1
    except Exception as e:
        logging.error(f"An error occurred during model training: {e}")
        return None, None, None


def plot_results(accuracy, recall, f1):
    """绘制模型性能图"""
    plt.bar(['Accuracy', 'Recall', 'F1 Score'], [accuracy, recall, f1], color=['blue', 'orange', 'green'])
    plt.ylim(0, 1)
    plt.title('Optimized model')
    plt.ylabel('Score')

    # 设置 y 轴的刻度为 0.05 的倍数
    plt.yticks([i * 0.05 for i in range(21)])  # 0.00, 0.05, ..., 1.00

    plt.show()


# 主程序
if __name__ == '__main__':
    data = getData()
    if data is not None:
        accuracy, recall, f1 = model_train(data)

        # 添加处理None的逻辑
        if accuracy is not None and recall is not None and f1 is not None:
            print(f"Optimized Model Accuracy: {accuracy:.4f}")
            print(f"Optimized Model Recall: {recall:.4f}")
            print(f"Optimized Model F1 Score: {f1:.4f}")
            plot_results(accuracy, recall, f1)
        else:
            print("Model training failed, metrics are not available.")
