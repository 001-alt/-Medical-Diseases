import jieba
import pandas as pd
from sklearn.tree import DecisionTreeClassifier  # 引入决策树分类器
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib  # 用于保存模型
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
            data = df[['content', 'type']]
            data['content'] = data['content'].apply(tokensize)
            return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

vectorizer = TfidfVectorizer(max_features=10000)

def model_train(data):
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)
    x_train_vectorized = vectorizer.fit_transform(x_train)

    # 创建决策树模型
    model = DecisionTreeClassifier(random_state=42)
    model.fit(x_train_vectorized, y_train)

    # 保存模型和向量化器
    joblib.dump(model, 'model/decision_tree_model.pkl')  # 保存模型到指定目录
    joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')  # 保存向量化器

    print("Model trained and saved successfully.")

def main():
    trainData = getData()
    if trainData is not None and not trainData.empty:
        model_train(trainData)  # 训练模型并保存
    else:
        print("Failed to retrieve training data or data is empty.")

# 运行主函数
if __name__ == "__main__":
    main()
