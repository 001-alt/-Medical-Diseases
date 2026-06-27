# import jieba
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import tempfile
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import accuracy_score, recall_score
# from sqlalchemy import create_engine, text
#
# # 数据库连接
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
# stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())
#
# def tokensize(text):
#     words = [word for word in jieba.cut(text) if word not in stopwords]
#     return ' '.join(words)
#
# def getData():
#     try:
#         with conn.connect() as connection:
#             query = text('SELECT * FROM cases')
#             df = pd.read_sql(query, con=connection, index_col='id')
#             data = df[['content', 'type']]
#             data.loc[:, 'content'] = data['content'].apply(tokensize)  # 使用 .loc 避免 SettingWithCopyWarning
#             return data
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#
# # 设置 TF-IDF 参数
# vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=3, max_df=0.9, sublinear_tf=True)
#
# def model_train(data):
#     # 临时文件夹处理
#     temp_folder = tempfile.gettempdir()  # 使用系统默认的临时目录
#     os.environ['JOBLIB_TEMP_FOLDER'] = temp_folder
#
#     x_train, x_test, y_train, y_test = train_test_split(
#         data['content'],
#         data['type'],
#         test_size=0.2,
#         random_state=42,
#         stratify=data['type']
#     )
#
#     x_train_vectorized = vectorizer.fit_transform(x_train)
#
#     # 超参数网格搜索
#     param_grid = {
#         'max_depth': [None, 10, 20, 30],
#         'min_samples_split': [2, 5, 10],
#         'min_samples_leaf': [1, 2, 4]
#     }
#
#     model = GridSearchCV(
#         DecisionTreeClassifier(random_state=42),
#         param_grid,
#         cv=5,
#         scoring='accuracy',
#         n_jobs=1,  # 将 n_jobs 设置为 1 以避免并行计算引起的问题
#         verbose=1
#     )
#
#     model.fit(x_train_vectorized, y_train)
#
#     y_pred = model.predict(vectorizer.transform(x_test))
#     accuracy = accuracy_score(y_test, y_pred)
#     recall = recall_score(y_test, y_pred, average='weighted')
#
#     return accuracy, recall
#
# # 主程序
# if __name__ == '__main__':
#     data = getData()
#     if data is not None:
#         accuracy, recall = model_train(data)
#         print(f"Optimized Model Accuracy: {accuracy:.4f}")
#         print(f"Optimized Model Recall: {recall:.4f}")
#
#         # 可视化结果
#         plt.bar(['Accuracy', 'Recall'], [accuracy, recall], color=['blue', 'orange'])
#         plt.ylim(0, 1)
#         plt.title('Model Performance')
#         plt.ylabel('Score')
#         plt.show()


import jieba
import pandas as pd
import matplotlib.pyplot as plt
import os
import tempfile
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, recall_score
from sqlalchemy import create_engine, text

# 数据库连接
conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())

def tokensize(text):
    """对文本进行分词并去除停用词"""
    words = [word for word in jieba.cut(text) if word not in stopwords]
    return ' '.join(words)

def getData():
    """从数据库获取数据并进行预处理"""
    try:
        with conn.connect() as connection:
            query = text('SELECT * FROM cases')
            df = pd.read_sql(query, con=connection, index_col='id')
            data = df[['content', 'type']]
            data.loc[:, 'content'] = data['content'].apply(tokensize)  # 使用 .loc 避免 SettingWithCopyWarning
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# 设置 TF-IDF 参数
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=3, max_df=0.9, sublinear_tf=True)

def model_train(data):
    """训练决策树模型并使用网格搜索优化超参数"""
    # 临时文件夹处理
    temp_folder = tempfile.gettempdir()  # 使用系统默认的临时目录
    os.environ['JOBLIB_TEMP_FOLDER'] = temp_folder

    # 划分训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(
        data['content'],
        data['type'],
        test_size=0.2,
        random_state=42,
        stratify=data['type']
    )

    # 特征提取
    x_train_vectorized = vectorizer.fit_transform(x_train)

    # 超参数网格搜索
    param_grid = {
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [4, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    model = GridSearchCV(
        DecisionTreeClassifier(random_state=42),
        param_grid,
        cv=5,
        scoring='accuracy',
        n_jobs=1,
        verbose=1
    )

    # 训练
    model.fit(x_train_vectorized, y_train)

    # 预测
    y_pred = model.predict(vectorizer.transform(x_test))
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred, average='weighted')

    return accuracy, recall, model.best_params_

# 主程序
if __name__ == '__main__':
    data = getData()
    if data is not None:
        accuracy, recall, best_params = model_train(data)
        print(f"Optimized Model Accuracy: {accuracy:.4f}")
        print(f"Optimized Model Recall: {recall:.4f}")
        print(f"Best Hyperparameters: {best_params}")

        # 可视化结果
        plt.bar(['Accuracy', 'Recall'], [accuracy, recall], color=['blue', 'orange'])
        plt.ylim(0, 1)
        plt.title('Model Performance')
        plt.ylabel('Score')
        plt.show()
