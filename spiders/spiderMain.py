import re
import requests
from lxml import etree
import csv
import os
from pymysql import connect
from utils.query import querys

class Spider(object):
    def __init__(self):
        self.spiderUrl = 'https://www.haodf.com/citiao/jibing-tangniaobing/bingcheng.html?p=%s'
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        self.max_count = 200
        self.current_page = 1  # 当前页码

    def init(self):
        if not os.path.exists('./temp.csv'):
            with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
                write = csv.writer(wf)
                write.writerow(["type", "gender", "age", "time", "content", "docName", "docHospital", "department",
                                "detailUrl", "height", "weight", "illDuration", "allergy"])

        try:
            conn = connect(host='localhost', user='root', password='1234', database='medicalinfo', port=3306,
                           charset='utf8mb4')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cases (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    type varchar(255),
                    gender varchar(255),
                    age varchar(255),
                    time varchar(255),
                    content varchar(255),
                    docName varchar(255),
                    docHospital varchar(255),
                    department varchar(255),
                    detailUrl varchar(2555),
                    height varchar(255),
                    weight varchar(255),
                    illDuration varchar(255),
                    allergy varchar(255)
                )
            ''')
            conn.commit()
        except Exception as e:
            print(f"Database initialization error: {e}")
        finally:
            conn.close()

    def main(self, entry_type):
        count = 0
        while count < self.max_count:
            # 打印即将请求的 URL
            current_url = self.spiderUrl % self.current_page
            print(f"正在请求的 URL: {current_url}")

            try:
                pageHtml = requests.get(current_url, headers=self.header).text
                page_tree = etree.HTML(pageHtml)
                li_list = page_tree.xpath('//*[@id="me-content"]/main/section/div/ul/li')

                if not li_list:  # 如果没有数据，停止爬取
                    print("没有找到更多数据，退出爬取。")
                    break

                for li in li_list:
                    if count >= self.max_count:  # 如果已经爬取到 200 条数据，结束
                        break

                    print(f"正在爬取页面 {self.current_page} 的数据，已爬取 {count + 1} 条数据")
                    initData = self.extract_data(li, entry_type)
                    if initData:
                        self.save_to_csv(initData)
                        count += 1

                self.current_page += 1  # 进入下一页

            except Exception as e:
                print(f"请求数据时发生错误: {e}")
                break

    def extract_data(self, li, entry_type):
        try:
            gender = li.xpath('./a/div/span[@class="patient-name"]/text()')[0][3]
            age = re.search(r'\d+', li.xpath('./a/div/span[@class="patient-name"]/text()')[0]).group()
            time = self.extract_time(li)
            content = li.xpath('./a/h3[@class="title"]/text()')[0]
            docName = li.xpath('div/div[@class="svc-info"]/a[@class="name"]/text()')[0]
            docHospital = li.xpath('div/div[@class="svc-info"]/a[@class="hospital"]/text()')[0]
            department = li.xpath('div/div[@class="svc-info"]/a[@class="faculty"]/text()')[0]
            detailUrl = li.xpath('./a/@href')[0]
            return [entry_type, gender, age, time, content, docName, docHospital, department, detailUrl]
        except Exception as e:
            print(f"数据提取错误: {e}")
            return None

    def extract_time(self, li):
        date_str = li.xpath('./a/div/span[@class="date"]/text()')[0]
        try:
            return re.search(r'\d{1,4}.\d{1,2}.\d{1,2}', date_str).group()
        except:
            return re.search(r'\d{1,2}.\d{1,2}', date_str).group()

    def save_to_csv(self, resultData):
        with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(resultData)

    def save_to_sql(self):
        with open('./temp.csv', 'r', encoding='utf-8') as r_f:
            reader = csv.reader(r_f)
            next(reader)  # Skip header
            for i in reader:
                querys('''
                    INSERT INTO cases5(type, gender, age, time, content, docName, docHospital, department, detailUrl)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', i[:9])  # Only take the first 9 columns

if __name__ == '__main__':
    spiderObj = Spider()
    # spiderObj.init()
    spiderObj.main('颈椎病')  # 在这里调用主函数
    # spiderObj.save_to_sql()


#
#
# import re
# import requests
# from lxml import etree
# import csv
# import os
# from pymysql import connect
# from utils.query import querys
#
# class Spider(object):
#     def __init__(self):
#         self.spiderUrl = 'https://www.haodf.com/citiao/jibing-jingzhuibing/bingcheng.html?p=%s'
#         self.fixed_url = 'https://www.haodf.com/citiao/jibing-jingzhuibing/bingcheng.html?decode__1282=n4%2BxcDnD9DuDRiGYDsD7Ie0%3DtitDC7YBRY%3Dl0eD'
#         self.header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
#         }
#         self.max_count = 200
#         self.current_page = 1  # 当前页码
#
#     def init(self):
#         if not os.path.exists('./temp.csv'):
#             with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
#                 write = csv.writer(wf)
#                 write.writerow(["type", "gender", "age", "time", "content", "docName", "docHospital", "department",
#                                 "detailUrl", "height", "weight", "illDuration", "allergy"])
#
#         try:
#             conn = connect(host='localhost', user='root', password='1234', database='medicalinfo', port=3306,
#                            charset='utf8mb4')
#             cursor = conn.cursor()
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS cases5 (
#                     id INT PRIMARY KEY AUTO_INCREMENT,
#                     type varchar(255),
#                     gender varchar(255),
#                     age varchar(255),
#                     time varchar(255),
#                     content varchar(255),
#                     docName varchar(255),
#                     docHospital varchar(255),
#                     department varchar(255),
#                     detailUrl varchar(2555),
#                     height varchar(255),
#                     weight varchar(255),
#                     illDuration varchar(255),
#                     allergy varchar(255)
#                 )
#             ''')
#             conn.commit()
#         except Exception as e:
#             print(f"Database initialization error: {e}")
#         finally:
#             conn.close()
#
#     def main(self, entry_type):
#         count = 0
#         while count < self.max_count:
#             # 根据当前页码决定请求的 URL
#             if self.current_page == 1:
#                 current_url = self.fixed_url
#             else:
#                 current_url = self.spiderUrl % self.current_page + '&decode__1282=eqfx97DQD%3Dn4umDl%3D5GkDRDRxGTnf2GaoD'
#
#             print(f"正在请求的 URL: {current_url}")
#
#             try:
#                 pageHtml = requests.get(current_url, headers=self.header).text
#                 page_tree = etree.HTML(pageHtml)
#                 li_list = page_tree.xpath('//*[@id="me-content"]/main/section/div/ul/li')
#
#                 if not li_list:  # 如果没有数据，停止爬取
#                     print("没有找到更多数据，退出爬取。")
#                     break
#
#                 for li in li_list:
#                     if count >= self.max_count:  # 如果已经爬取到 200 条数据，结束
#                         break
#
#                     print(f"正在爬取页面 {self.current_page} 的数据，已爬取 {count + 1} 条数据")
#                     initData = self.extract_data(li, entry_type)
#                     if initData:
#                         self.save_to_csv(initData)
#                         count += 1
#
#                 self.current_page += 1  # 进入下一页
#
#             except Exception as e:
#                 print(f"请求数据时发生错误: {e}")
#                 break
#
#     def extract_data(self, li, entry_type):
#         try:
#             gender = li.xpath('./a/div/span[@class="patient-name"]/text()')[0][3]
#             age = re.search(r'\d+', li.xpath('./a/div/span[@class="patient-name"]/text()')[0]).group()
#             time = self.extract_time(li)
#             content = li.xpath('./a/h3[@class="title"]/text()')[0]
#             docName = li.xpath('div/div[@class="svc-info"]/a[@class="name"]/text()')[0]
#             docHospital = li.xpath('div/div[@class="svc-info"]/a[@class="hospital"]/text()')[0]
#             department = li.xpath('div/div[@class="svc-info"]/a[@class="faculty"]/text()')[0]
#             detailUrl = li.xpath('./a/@href')[0]
#             return [entry_type, gender, age, time, content, docName, docHospital, department, detailUrl]
#         except Exception as e:
#             print(f"数据提取错误: {e}")
#             return None
#
#     def extract_time(self, li):
#         date_str = li.xpath('./a/div/span[@class="date"]/text()')[0]
#         try:
#             return re.search(r'\d{1,4}.\d{1,2}.\d{1,2}', date_str).group()
#         except:
#             return re.search(r'\d{1,2}.\d{1,2}', date_str).group()
#
#     def save_to_csv(self, resultData):
#         with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow(resultData)
#
#     def save_to_sql(self):
#         with open('./temp.csv', 'r', encoding='utf-8') as r_f:
#             reader = csv.reader(r_f)
#             next(reader)  # Skip header
#             for i in reader:
#                 querys('''
#                     INSERT INTO cases5(type, gender, age, time, content, docName, docHospital, department, detailUrl)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 ''', i[:9])  # Only take the first 9 columns
#
# if __name__ == '__main__':
#     spiderObj = Spider()
#     # spiderObj.init()
#     spiderObj.main('颈椎病')  # 在这里调用主函数
#     # spiderObj.save_to_sql()

# import re
# import requests
# from lxml import etree
# import csv
# import os
# from pymysql import connect
# from utils.query import querys
# import time  # 导入时间模块
#
#
# class Spider(object):
#     def __init__(self):
#         self.spiderUrl = 'https://www.haodf.com/citiao/jibing-pajinsen/bingcheng.html?p=%s'
#         self.fixed_url = 'https://www.haodf.com/citiao/jibing-pajinsen/bingcheng.html?decode__1282=n4jxnDRii%3DKQqDK4GNBeeqBKeY5DtKiidYtzC74D'
#
#         # 动态参数列表
#         self.decode_params = [
#             "n4%2Bxci0Q0%3DiteDKGQbDs03OokDCDnDxgmWIoD",
#             "n4%2Bxci0Q0%3DiteDKGQeDs03OokDCDnDrYpDUmoD",
#             "n4%2Bxci0Q0%3DiteDKGQiDsFRb9DBDAx%2B0khTRL%2BiD",
#             "n4%2Bxci0Q0%3DiteDKbq05mbFDO8DCDnYx7TRyH5ID",
#             "n4%2Bxci0Q0%3DiteDK4D5Ds03OxmE%3DxnY6D7u2bID",
#             "n4%2Bxci0Q0%3DiteDKR405mtxRnDBDArfohExTD",
#             "n4%2Bxci0Q0%3DiteDK40KDs03OxmEx0xGKA%3D%2B%3Dbd4x",
#             "n4%2Bxci0Q0%3DiteDIqGNBmjDRnDBDAx3dr32MbD",
#             "eqGxR7e7qGqqnDfx05OtDy7DgDNNph%3DGOUeD",
#             "eqGxR7e7qGqqnADlrmq0%3DKit0w9DWuDApD",
#             "eqGxR7e7qGqqnDUx05Ot%2BKiti47I4wAvdx",
#             "eqGxR7e7qGqqn0Dlrmq0%3DKiti47KwvdPNdx",
#             "eqGxR7e7qGqqnDRx05OtDy7%2Bi47KXYNjvdx",
#             "eqGxR7e7qGqqciDl%3D5GkQGC7D8YGOz%2F%2FBQmKeD",
#             "eqGxR7e7qGqqcQDlrmq0%3DKitQD%3DeGORK7fKeD",
#         ]
#
#         self.header = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
#         }
#         self.max_count = 300
#         self.current_page = 1
#
#     def init(self):
#         if not os.path.exists('./temp.csv'):
#             with open('./temp.csv', 'a', newline='', encoding='utf-8') as wf:
#                 write = csv.writer(wf)
#                 write.writerow(["type", "gender", "age", "time", "content", "docName", "docHospital", "department",
#                                 "detailUrl", "height", "weight", "illDuration", "allergy"])
#
#         try:
#             conn = connect(host='localhost', user='root', password='1234', database='medicalinfo', port=3306,
#                            charset='utf8mb4')
#             cursor = conn.cursor()
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS cases (
#                     id INT PRIMARY KEY AUTO_INCREMENT,
#                     type varchar(255),
#                     gender varchar(255),
#                     age varchar(255),
#                     time varchar(255),
#                     content varchar(255),
#                     docName varchar(255),
#                     docHospital varchar(255),
#                     department varchar(255),
#                     detailUrl varchar(2555),
#                     height varchar(255),
#                     weight varchar(255),
#                     illDuration varchar(255),
#                     allergy varchar(255)
#                 )
#             ''')
#             conn.commit()
#         except Exception as e:
#             print(f"Database initialization error: {e}")
#         finally:
#             conn.close()
#
#     def main(self, entry_type):
#         count = 0
#         while count < self.max_count:
#             # 根据当前页码决定请求的 URL
#             if self.current_page == 1:
#                 current_url = self.fixed_url
#             else:
#                 decode_param = self.decode_params[self.current_page - 2]  # 对应当前页的 decode__1282
#                 current_url = self.spiderUrl % self.current_page + '&decode__1282=' + decode_param
#
#             print(f"正在请求的 URL: {current_url}")
#
#             try:
#                 pageHtml = requests.get(current_url, headers=self.header).text
#                 page_tree = etree.HTML(pageHtml)
#                 li_list = page_tree.xpath('//*[@id="me-content"]/main/section/div/ul/li')
#
#                 if not li_list:  # 如果没有数据，停止爬取
#                     print("没有找到更多数据，退出爬取。")
#                     break
#
#                 for li in li_list:
#                     if count >= self.max_count:  # 如果已经爬取到 200 条数据，结束
#                         break
#
#                     print(f"正在爬取页面 {self.current_page} 的数据，已爬取 {count + 1} 条数据")
#                     initData = self.extract_data(li, entry_type)
#                     if initData:
#                         self.save_to_csv(initData)
#                         count += 1
#
#                 self.current_page += 1  # 进入下一页
#                 time.sleep(2)  # 请求之间的间隔
#
#             except Exception as e:
#                 print(f"请求数据时发生错误: {e}")
#                 break
#
#     def extract_data(self, li, entry_type):
#         try:
#             gender = li.xpath('./a/div/span[@class="patient-name"]/text()')[0][3]
#             age = re.search(r'\d+', li.xpath('./a/div/span[@class="patient-name"]/text()')[0]).group()
#             time = self.extract_time(li)
#             content = li.xpath('./a/h3[@class="title"]/text()')[0]
#             docName = li.xpath('div/div[@class="svc-info"]/a[@class="name"]/text()')[0]
#             docHospital = li.xpath('div/div[@class="svc-info"]/a[@class="hospital"]/text()')[0]
#             department = li.xpath('div/div[@class="svc-info"]/a[@class="faculty"]/text()')[0]
#             detailUrl = li.xpath('./a/@href')[0]
#             return [entry_type, gender, age, time, content, docName, docHospital, department, detailUrl]
#         except Exception as e:
#             print(f"数据提取错误: {e}")
#             return None
#
#     def extract_time(self, li):
#         date_str = li.xpath('./a/div/span[@class="date"]/text()')[0]
#         try:
#             return re.search(r'\d{1,4}.\d{1,2}.\d{1,2}', date_str).group()
#         except:
#             return re.search(r'\d{1,2}.\d{1,2}', date_str).group()
#
#     def save_to_csv(self, resultData):
#         with open('./temp.csv', 'a', newline='', encoding='utf-8') as f:
#             writer = csv.writer(f)
#             writer.writerow(resultData)
#
#     def save_to_sql(self):
#         with open('./temp.csv', 'r', encoding='utf-8') as r_f:
#             reader = csv.reader(r_f)
#             next(reader)  # Skip header
#             for i in reader:
#                 querys('''
#                     INSERT INTO cases7(type, gender, age, time, content, docName, docHospital, department, detailUrl)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 ''', i[:9])
#
#
# if __name__ == '__main__':
#     spiderObj = Spider()
#     # spiderObj.init()
#     # spiderObj.main('帕金森')
#     spiderObj.save_to_sql()


