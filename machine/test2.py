import jieba
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine, text
import joblib  # 用于保存模型

# 数据库连接
conn = create_engine('mysql+pymysql://root:1234@127.0.0.1:3306/medicalinfo?charset=utf8')
stopwords = set(open('./stopword.txt', 'r', encoding='utf-8').read().splitlines())


def tokensize(text):
    words = [word for word in jieba.cut(text) if word not in stopwords]
    return ' '.join(words)


def getData():
    try:
        with conn.connect() as connection:
            query = text('SELECT * FROM cases')  # 确保查询的表名和字段正确
            df = pd.read_sql(query, con=connection, index_col='id')
            data = df[['content', 'type']]
            data['content'] = data['content'].apply(tokensize)  # 进行分词处理
            return data
    except Exception as e:
        print(f"An error occurred while retrieving data: {e}")
        return None


def model_train(data):
    vectorizer = TfidfVectorizer(max_features=10000)
    x_train, x_test, y_train, y_test = train_test_split(data['content'], data['type'], test_size=0.2, random_state=42)

    # Fit the vectorizer on training data and transform it
    x_train_vectorized = vectorizer.fit_transform(x_train)

    # Create and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train_vectorized, y_train)

    # Save the model and vectorizer
    joblib.dump(model, 'model/random_forest_model.pkl')
    joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')

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
