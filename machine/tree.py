import jieba
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine, text

# 数据库连接
conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
stopwords = set(open('./machine/stopword.txt', 'r', encoding='utf-8').read().splitlines())


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

def model_train(data):
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
    x_train_vectorized = vectorizer.fit_transform(x_train)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train_vectorized, y_train)

    y_pred = model.predict(vectorizer.transform(x_test))
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy}")

    return model


def predict(model, content):
    content_vectorized = vectorizer.transform([tokensize(content)])
    prediction = model.predict(content_vectorized)
    return prediction[0]


def train_and_predict(content):
    trainData = getData()
    if trainData is None or trainData.empty:
        return None, "Failed to retrieve training data"

    model = model_train(trainData)
    result = predict(model, content)
    return result, None  # 返回结果和错误信息


# import jieba  # 导入中文分词库
# import pandas as pd  # 导入数据处理库
# from sklearn.tree import DecisionTreeClassifier  # 引入决策树分类器
# from sklearn.model_selection import train_test_split  # 引入数据集划分工具
# from sklearn.feature_extraction.text import TfidfVectorizer  # 引入TF-IDF向量化工具
# from sklearn.metrics import accuracy_score  # 引入准确率评估函数
# from sqlalchemy import create_engine, text  # 导入SQLAlchemy用于数据库操作
#
# # 数据库连接，使用SQLAlchemy创建连接引擎
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
# # 读取停用词文件并存储到集合中，以便后续分词时过滤
# stopwords = set(open('./machine/stopword.txt', 'r', encoding='utf-8').read().splitlines())
#
# def getData():
#     """从数据库获取数据并进行预处理"""
#     try:
#         # 连接到数据库并执行查询
#         with conn.connect() as connection:
#             query = text('SELECT * FROM cases')  # SQL查询
#             df = pd.read_sql(query, con=connection, index_col='id')  # 将查询结果读入DataFrame
#             data = df[['content', 'type']]  # 选择特定的列
#             data.loc[:, 'content'] = data['content'].apply(tokensize)  # 对文本内容进行分词处理
#             return data  # 返回处理后的数据
#     except Exception as e:
#         print(f"An error occurred: {e}")  # 打印错误信息
#         return None  # 返回None表示获取数据失败
#
# def tokensize(text):
#     """对输入文本进行分词并去除停用词"""
#     # 使用jieba进行中文分词，然后过滤掉停用词
#     words = [word for word in jieba.cut(text) if word not in stopwords]
#     return ' '.join(words)  # 将分词结果用空格连接成字符串返回
# # 初始化TF-IDF向量化器，设置最大特征数为10000
# vectorizer = TfidfVectorizer(max_features=10000)
# def model_train(data):
#     """训练决策树模型并返回训练好的模型"""
#     # 将数据集划分为训练集和测试集，测试集占20%
#     x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
#     x_train_vectorized = vectorizer.fit_transform(x_train)
#     model = DecisionTreeClassifier(random_state=42)
#     model.fit(x_train_vectorized, y_train)
#     y_pred = model.predict(vectorizer.transform(x_test))
#     accuracy = accuracy_score(y_test, y_pred)
#     print(f"Model accuracy: {accuracy}")
#     return model
#
# def predict(model, content):
#     """使用训练好的模型进行预测"""
#     # 对输入文本进行分词和TF-IDF向量化
#     content_vectorized = vectorizer.transform([tokensize(content)])
#     prediction = model.predict(content_vectorized)  # 使用模型进行预测
#     return prediction[0]  # 返回预测结果
#
# def train_and_predict(content):
#     """获取训练数据、训练模型并进行预测"""
#     trainData = getData()  # 获取训练数据
#     if trainData is None or trainData.empty:  # 检查数据是否有效
#         return None, "Failed to retrieve training data"  # 返回错误信息
#
#     model = model_train(trainData)  # 训练模型
#     result = predict(model, content)  # 进行预测
#     return result, None  # 返回预测结果和错误信息

# import jieba
# import pandas as pd
# from sklearn.tree import DecisionTreeClassifier  # 引入决策树分类器
# from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import accuracy_score
# from sqlalchemy import create_engine, text
#
# # 数据库连接
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
# stopwords = set(open('./machine/stopword.txt', 'r', encoding='utf-8').read().splitlines())
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
#             query = text('SELECT * FROM cases9')
#             df = pd.read_sql(query, con=connection, index_col='id')
#             data = df[['content', 'type']]
#             data.loc[:, 'content'] = data['content'].apply(tokensize)
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
#     # 切分数据集
#     x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
#     x_train_vectorized = vectorizer.fit_transform(x_train)
#
#     # 定义超参数网格
#     param_grid = {
#         'max_depth': [None, 10, 20, 30],
#         'min_samples_split': [2, 5, 10],
#         'min_samples_leaf': [1, 2, 4]
#     }
#
#     # 网格搜索
#     model = DecisionTreeClassifier(random_state=42)
#     grid_search = GridSearchCV(model, param_grid, cv=5)  # 使用5折交叉验证
#     grid_search.fit(x_train_vectorized, y_train)
#
#     best_model = grid_search.best_estimator_  # 获取最佳模型
#
#     # K折交叉验证
#     cv_scores = cross_val_score(best_model, x_train_vectorized, y_train, cv=5)
#     print(f"K-Fold CV Scores: {cv_scores}")
#     print(f"Mean CV Score: {cv_scores.mean()}")
#
#     # 测试集上的预测与准确率
#     y_pred = best_model.predict(vectorizer.transform(x_test))
#     accuracy = accuracy_score(y_test, y_pred)
#     print(f"Model accuracy on test set: {accuracy}")
#
#     return best_model
#
#
# def predict(model, content):
#     content_vectorized = vectorizer.transform([tokensize(content)])
#     prediction = model.predict(content_vectorized)
#     return prediction[0]
#
#
# def train_and_predict(content):
#     trainData = getData()
#     if trainData is None or trainData.empty:
#         return None, "Failed to retrieve training data"
#
#     model = model_train(trainData)
#     result = predict(model, content)
#     return result, None  # 返回结果和错误信息


