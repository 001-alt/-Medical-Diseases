# import jieba
# import pandas as pd
# from sklearn.tree import DecisionTreeClassifier  # 引入决策树分类器
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
# from sqlalchemy import create_engine, text
#
# # 数据库连接
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
# stopwords = set(open('stopword.txt', 'r', encoding='utf-8').read().splitlines())
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
#             data.loc[:, 'content'] = data['content'].apply(tokensize)
#             return data
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None
#
# vectorizer = TfidfVectorizer(max_features=10000)
#
# def model_train(data):
#     x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
#     x_train_vectorized = vectorizer.fit_transform(x_train)
#
#     # 使用决策树分类器
#     model = DecisionTreeClassifier(random_state=42)  # 创建决策树模型
#     model.fit(x_train_vectorized, y_train)
#
#     y_pred = model.predict(vectorizer.transform(x_test))
#
#     # 计算各类性能指标
#     accuracy = accuracy_score(y_test, y_pred)
#     precision = precision_score(y_test, y_pred, average='weighted')  # 加权精确率
#     recall = recall_score(y_test, y_pred, average='weighted')  # 加权召回率
#     f1 = f1_score(y_test, y_pred, average='weighted')  # 加权 F1 分数
#     cm = confusion_matrix(y_test, y_pred)  # 混淆矩阵
#
#     print(f"Model accuracy: {accuracy}")
#     print(f"Precision: {precision}")
#     print(f"Recall: {recall}")
#     print(f"F1 Score: {f1}")
#     print(f"Confusion Matrix:\n{cm}")
#
#     return model
#
# def predict(model, content):
#     content_vectorized = vectorizer.transform([tokensize(content)])
#     prediction = model.predict(content_vectorized)
#     return prediction[0]
#
# def train_and_predict(content):
#     trainData = getData()
#     if trainData is None or trainData.empty:
#         print("Failed to retrieve training data")
#         return
#
#     model = model_train(trainData)
#     result = predict(model, content)
#     print(f"Predicted result: {result}")  # 直接打印预测结果
#
# # 调用示例
# train_and_predict("头晕")  # 在这里替换为您要预测的实际内容

# import jieba
# import pandas as pd
# import os
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split, KFold, GridSearchCV
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from sqlalchemy import create_engine, text
# import matplotlib.pyplot as plt
# import tempfile
#
# # 设置临时文件夹为ASCII路径
# os.environ['JOBLIB_TEMP_FOLDER'] = tempfile.gettempdir()
#
# # 数据库连接
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
#
# # 加载停用词
# try:
#     stopwords = set(open('stopword.txt', 'r', encoding='utf-8').read().splitlines())
# except FileNotFoundError:
#     print("停用词文件未找到，将不使用停用词")
#     stopwords = set()
#
#
# def tokensize(text):
#     words = [word for word in jieba.cut(text) if word not in stopwords and len(word) > 1]
#     return ' '.join(words)
#
#
# def getData():
#     try:
#         with conn.connect() as connection:
#             query = text('SELECT * FROM cases')
#             df = pd.read_sql(query, con=connection, index_col='id')
#             data = df[['content', 'type']].dropna()
#             data.loc[:, 'content'] = data['content'].apply(tokensize)
#             return data
#     except Exception as e:
#         print(f"数据获取错误: {e}")
#         return None
# # TF-IDF参数优化
# vectorizer = TfidfVectorizer(
#     max_features=5000,
#     min_df=5,
#     max_df=0.8,
#     ngram_range=(1, 2)
# )
#
#
# def model_train(data):
#     # 简化参数网格以减少计算量
#     param_grid = {
#         'max_depth': [10, None],
#         'min_samples_split': [5, 10],
#         'min_samples_leaf': [2, 4]
#     }
#
#
#     grid_search = GridSearchCV(
#         estimator=DecisionTreeClassifier(random_state=42),
#         param_grid=param_grid,
#         cv=5,
#         scoring='accuracy',
#         n_jobs=1,  # 暂时禁用并行计算
#         verbose=1
#     )
#
#     x = vectorizer.fit_transform(data['content'])
#     y = data['type']
#
#     grid_search.fit(x, y)
#
#     print(f"最佳参数: {grid_search.best_params_}")
#     print(f"交叉验证最佳得分: {grid_search.best_score_:.4f}")
#
#     return grid_search.best_estimator_
#
#
# def predict(model, content):
#     content_vectorized = vectorizer.transform([tokensize(content)])
#     return model.predict(content_vectorized)[0]
#
#
# def train_and_predict(content):
#     trainData = getData()
#     if trainData is None or trainData.empty:
#         print("获取训练数据失败")
#         return
#
#     model = model_train(trainData)
#
#     # 测试集评估
#     x_train, x_test, y_train, y_test = train_test_split(
#         trainData['content'], trainData['type'],
#         test_size=0.2, random_state=42, stratify=trainData['type']
#     )
#
#     x_test_vectorized = vectorizer.transform(x_test)
#     y_pred = model.predict(x_test_vectorized)
#
#     print("\n测试集评估结果:")
#     print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
#     print(f"精确率: {precision_score(y_test, y_pred, average='weighted'):.4f}")
#     print(f"召回率: {recall_score(y_test, y_pred, average='weighted'):.4f}")
#     print(f"F1分数: {f1_score(y_test, y_pred, average='weighted'):.4f}")
#
#     # 预测结果
#     result = predict(model, content)
#     print(f"\n预测结果: {result}")
#
#
# # 调用示例
# if __name__ == "__main__":
#     train_and_predict(
#         "医生您好受伤原因：本人今年24岁，在今年6月18日玩飞盘... 想了解恢复情况，是否可以下地走路和康复训练，是否存在后续疾病隐患")

# import jieba
# import pandas as pd
# import os
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.model_selection import train_test_split, KFold, GridSearchCV
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from sqlalchemy import create_engine, text
# import matplotlib.pyplot as plt
# import tempfile
#
# # 设置临时文件夹为ASCII路径
# os.environ['JOBLIB_TEMP_FOLDER'] = tempfile.gettempdir()
#
# # 数据库连接
# conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
#
# # 加载停用词
# try:
#     stopwords = set(open('stopword.txt', 'r', encoding='utf-8').read().splitlines())
# except FileNotFoundError:
#     print("停用词文件未找到，将不使用停用词")
#     stopwords = set()
#
#
# def tokensize(text):
#     words = [word for word in jieba.cut(text) if word not in stopwords and len(word) > 1]
#     return ' '.join(words)
#
#
# def getData():
#     try:
#         with conn.connect() as connection:
#             query = text('SELECT * FROM cases')
#             df = pd.read_sql(query, con=connection, index_col='id')
#             data = df[['content', 'type']].dropna()
#             data.loc[:, 'content'] = data['content'].apply(tokensize)
#             return data
#     except Exception as e:
#         print(f"数据获取错误: {e}")
#         return None
#
#
# # TF-IDF参数优化
# vectorizer = TfidfVectorizer(
#     max_features=5000,
#     min_df=5,
#     max_df=0.8,
#     ngram_range=(1, 2)
# )
#
#
# def model_train(data):
#     kf = KFold(n_splits=5, shuffle=True, random_state=42)
#     train_accuracies = []
#     val_accuracies = []
#
#     param_grid = {
#         'max_depth': [10, None],
#         'min_samples_split': [5, 10],
#         'min_samples_leaf': [2, 4]
#     }
#
#     # 使用GridSearchCV寻找最佳参数
#     grid_search = GridSearchCV(
#         estimator=DecisionTreeClassifier(random_state=42),
#         param_grid=param_grid,
#         cv=5,  # 减少为5折验证
#         scoring='accuracy',
#         n_jobs=1,  # 暂时禁用并行计算
#         verbose=1
#     )
#
#     x = vectorizer.fit_transform(data['content'])
#     y = data['type']
#
#     # KFold交叉验证
#     for train_index, val_index in kf.split(data):
#         x_train, x_val = x[train_index], x[val_index]
#         y_train, y_val = y.iloc[train_index], y.iloc[val_index]
#
#         grid_search.fit(x_train, y_train)
#
#         # 记录训练和验证集的准确率
#         train_accuracy = grid_search.score(x_train, y_train)
#         val_accuracy = grid_search.score(x_val, y_val)
#
#         train_accuracies.append(train_accuracy)
#         val_accuracies.append(val_accuracy)
#
#     print(f"最佳参数: {grid_search.best_params_}")
#     print(f"交叉验证最佳得分: {grid_search.best_score_:.4f}")
#
#     # 绘制训练和验证准确率曲线
#     plt.plot(range(1, len(train_accuracies) + 1), train_accuracies, label='Training Accuracy', marker='o')
#     plt.plot(range(1, len(val_accuracies) + 1), val_accuracies, label='Validation Accuracy', marker='o')
#     plt.xlabel('Fold')
#     plt.ylabel('Accuracy')
#     plt.title('Training and Validation Accuracy per Fold')
#     plt.legend()
#     plt.grid()
#     plt.show()
#
#     return grid_search.best_estimator_
#
#
# def predict(model, content):
#     content_vectorized = vectorizer.transform([tokensize(content)])
#     return model.predict(content_vectorized)[0]
#
#
# def train_and_predict(content):
#     trainData = getData()
#     if trainData is None or trainData.empty:
#         print("获取训练数据失败")
#         return
#
#     model = model_train(trainData)
#
#     # 测试集评估
#     x_train, x_test, y_train, y_test = train_test_split(
#         trainData['content'], trainData['type'],
#         test_size=0.2, random_state=42, stratify=trainData['type']
#     )
#
#     x_train_vectorized = vectorizer.transform(x_train)
#     x_test_vectorized = vectorizer.transform(x_test)
#
#     model.fit(x_train_vectorized, y_train)
#
#     y_pred = model.predict(x_test_vectorized)
#
#     print("\n测试集评估结果:")
#     print(f"准确率: {accuracy_score(y_test, y_pred):.4f}")
#     print(f"精确率: {precision_score(y_test, y_pred, average='weighted'):.4f}")
#     print(f"召回率: {recall_score(y_test, y_pred, average='weighted'):.4f}")
#     print(f"F1分数: {f1_score(y_test, y_pred, average='weighted'):.4f}")
#
#     # 预测结果
#     result = predict(model, content)
#     print(f"\n预测结果: {result}")
#
#
# # 调用示例
# if __name__ == "__main__":
#     train_and_predict(
#         "医生您好受伤原因：本人今年24岁，在今年6月18日玩飞盘... 想了解恢复情况，是否可以下地走路和康复训练，是否存在后续疾病隐患"
#     )
