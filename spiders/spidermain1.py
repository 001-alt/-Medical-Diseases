# import re
# import requests
# from lxml import etree
# import csv
# import os
# from pymysql import *
# from utils.query import querys
# import pandas as pd
# import re
# import time
# from scipy.constants import value
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from utils.query import querys
#
# class Spider(object):
#     def __init__(self):
#         self.spiderUrl = 'https://www.haodf.com/citiao/jibing-gaoxueya/bingcheng.html'
#         service = Service('./chromedriver.exe')
#         option = webdriver.ChromeOptions()
#
#     def init(self):
#         # 检查 CSV 文件
#         if not os.path.exists('./temp.csv'):
#             with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
#                 writer = csv.writer(wf)
#                 writer.writerow(["type", "gender", "age", "time", "content", "docName", "docHospital", "department",
#                                  "detailUrl", "height", "weight", "illDuration", "allergy"])
#             try:
#                 conn = connect(host='localhost', user='root', password='1234', database='medicalinfo', port=3306,
#                                charset='utf8mb4')
#                 sql = '''
#                                CREATE TABLE IF NOT EXISTS cases (
#                                    id INT PRIMARY KEY AUTO_INCREMENT,
#                                    type VARCHAR(255),
#                                    gender VARCHAR(255),
#                                    age VARCHAR(255),
#                                    time VARCHAR(255),
#                                    content VARCHAR(255),
#                                    docName VARCHAR(255),
#                                    docHospital VARCHAR(255),
#                                    department VARCHAR(255),
#                                    detailUrl VARCHAR(2555),
#                                    height VARCHAR(255),
#                                    weight VARCHAR(255),
#                                    illDuration VARCHAR(255),
#                                    allergy VARCHAR(255)
#                                    )
#                                '''
#                 cursor = conn.cursor()
#                 cursor.execute(sql)
#                 conn.commit()
#             except:
#                 pass
#
#     def main(self):
#         pageHtml = requests.get(self.spiderUrl, headers=self.header).text
#         page_tree = etree.HTML(pageHtml)
#         print(pageHtml)
#         li = page_tree.xpath('//*[@id="me-content"]/main/section/div/ul/li[1]')
#         print(li)
#
#
# if __name__ == '__main__':
#     spiderObj = Spider()
#     # spiderObj.init()
#     spiderObj.main()
#


import re
import requests
from lxml import etree
import csv
import os
from pymysql import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class Spider(object):
    def __init__(self):
        self.spiderUrl = 'https://www.haodf.com/citiao/jibing-gaoxueya/bingcheng.html'

        # 设置 Selenium 的选项
        service = Service('./chromedriver.exe')  # 替换为你的 ChromeDriver 路径
        options = Options()
        options.add_argument('--headless')  # 无头模式（可选）
        options.add_argument('--disable-gpu')  # 禁用 GPU（可选）
        options.add_argument('--no-sandbox')  # 解决一些环境问题
        self.driver = webdriver.Chrome(service=service, options=options)

        # 设置请求头
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Cookie": "g=76943_1738204166494; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1738204167; HMACCOUNT=2D851943B5E651DB; g=HDF.63.67995f38bc5da; userinfo[id]=11028365846; userinfo[time]=1738238896; userinfo[hostid]=0; userinfo[key]=B3oHNlFiVTVSOgE%2BATBbPwJpAzdSZlM2UntRPlBiC2BQaVAkXG9RMlBnCWpRIFduVnQBPVN6; userinfo[ver]=1.0.2; userinfo[name]=hdflt13mdsk; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1738238954"
        }

    def init(self):
        # 检查 CSV 文件
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
                writer = csv.writer(wf)
                writer.writerow(["type", "gender", "age", "time", "content", "docName", "docHospital", "department",
                                 "detailUrl", "height", "weight", "illDuration", "allergy"])
            try:
                conn = connect(
                    host='localhost',
                    user='root',
                    password='1234',
                    database='medicalinfo',
                    port=3306,
                    charset='utf8mb4'
                )
                sql = '''
                CREATE TABLE IF NOT EXISTS cases (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    type VARCHAR(255),
                    gender VARCHAR(255),
                    age VARCHAR(255),
                    time VARCHAR(255),
                    content VARCHAR(255),
                    docName VARCHAR(255),
                    docHospital VARCHAR(255),
                    department VARCHAR(255),
                    detailUrl VARCHAR(2555),
                    height VARCHAR(255),
                    weight VARCHAR(255),
                    illDuration VARCHAR(255),
                    allergy VARCHAR(255)
                )
                '''
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print(f"数据库初始化失败：{e}")

    def main(self):
        # 使用 Selenium 打开网页
        self.driver.get(self.spiderUrl)

        # 等待页面加载（根据实际情况调整时间）
        time.sleep(5)

        # 获取页面源码
        page_source = self.driver.page_source

        # 使用 lxml 解析页面
        page_tree = etree.HTML(page_source)

        # 获取数据
        try:
            # 替换为你需要的 XPath，根据页面结构调整
            li_list = page_tree.xpath('//*[@id="me-content"]/main/section/div/ul/li')

            for li in li_list:
                # 示例：提取每个列表项中的某些字段
                title = li.xpath('.//a/text()')[0].strip()
                url = li.xpath('.//a/@href')[0].strip()

                # 打印结果
                print(f"标题：{title}, 链接：{url}")

        except Exception as e:
            print(f"提取数据失败：{e}")

        # 关闭 Selenium driver
        self.driver.quit()


if __name__ == '__main__':
    spiderObj = Spider()
    spiderObj.init()
    spiderObj.main()
