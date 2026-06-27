# 使用Python pandas库转换（机器学习项目常用方法）
import pandas as pd

# 读取CSV文件
df = pd.read_csv('heart_disease.csv')

# 保存为Excel
df.to_excel('heart_disease.xlsx', index=False)