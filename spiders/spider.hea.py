from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re

class Spider(object):
    def __init__(self):
        # Chrome配置
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 无头模式，不显示浏览器
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.base_url = 'https://www.haodf.com/citiao/jibing-jingzhuibing/bingcheng.html'

    def get_decode_value(self):
        self.driver.get(self.base_url)
        # 获取页面源代码
        page_html = self.driver.page_source
        print(f"请求的 URL: {self.driver.current_url}")
        print(page_html)  # 可以打印出完整的HTML查看

        # 用正则匹配 decode__1282 参数
        match = re.search(r'decode__1282=([^&]+)', page_html)
        if match:
            return match.group(1)
        else:
            print("未找到 decode__1282 参数")
        return None

    def __del__(self):
        self.driver.quit()  # 关闭浏览器

if __name__ == '__main__':
    spider = Spider()
    decode_value = spider.get_decode_value()
    print(f"获取到的 decode__1282 值: {decode_value}")
