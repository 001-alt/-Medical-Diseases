import jieba
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sqlalchemy import create_engine, text
import joblib  # 用于保存和加载模型

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

def model_train(data):
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
    x_train_vectorized = vectorizer.fit_transform(x_train)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train_vectorized, y_train)

    y_pred = model.predict(vectorizer.transform(x_test))
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy}")

    # 保存模型和向量化器
    joblib.dump(model, 'model/random_forest_model.pkl')
    joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')

    return model

def predict(model, content):
    content_vectorized = vectorizer.transform([tokensize(content)])
    prediction = model.predict(content_vectorized)
    return prediction[0]

def train_and_predict(content):
    trainData = getData()
    if trainData is None or trainData.empty:
        return None, "Failed to retrieve training data"

    model = model_train(trainData)  # 训练模型并保存
    result = predict(model, content)  # 进行预测
    return result, None  # 返回结果和错误信息

def load_model():
    """加载已保存的模型和向量化器"""
    model = joblib.load('model/random_forest_model.pkl')
    vectorizer = joblib.load('model/tfidf_vectorizer.pkl')
    return model, vectorizer

# 使用示例
# 如果要进行预测，请先加载模型
def main(content):
    # 尝试加载已保存的模型
    try:
        model, vectorizer = load_model()
        result = predict(model, content)
    except Exception as e:
        print("Loading model failed. Training a new model.")
        result, _ = train_and_predict(content)

    return result

# 调用main函数进行预测
result = main("待预测的内容")
