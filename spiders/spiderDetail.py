import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from utils.query import querys

class spider(object):
    def __init__(self, spiderUrl):
        self.spiderUrl = spiderUrl  # 这里确保 spiderUrl 是一个字符串

    def startBrowser(self):
        service = Service('./chromedriver.exe')
        option = webdriver.ChromeOptions()
        option.add_experimental_option("debuggerAddress", "localhost:9223")
        browser = webdriver.Chrome(service=service, options=option)
        return browser

    def main(self, id):
        browser = self.startBrowser()
        print('列表URL为: ' + self.spiderUrl)
        browser.get(self.spiderUrl)
        #身高
        try:
            height = re.findall('\d+',browser.find_element(by=By.XPATH,value='//span[contains(text(),"身高体重")]/following-sibling::span[1]').text)[0]
        except:
            height = '无'
        #体重
        try:
            weight = re.findall('\d+',browser.find_element(by=By.XPATH,value='//span[contains(text(),"身高体重")]/following-sibling::span[1]').text)[1]
        except:
            weight = '无'
        #患病时间
        try:
            illDuration = browser.find_element(by=By.XPATH,value='//span[contains(text(),"患病时长")]/following-sibling::span[1]').text
        except:
            illDuration = '无'
        #过敏史
        try:
            allergy = re.search(r'([\u4e00-\u9fa5]+)\(',browser.find_element(by=By.XPATH,value='//span[contains(text(),"过敏史")]/following-sibling::span[1]').text).group(1)
        except:
            allergy = '暂无信息'

        print(height,weight,illDuration,allergy)

        querys("UPDATE cases5 SET height=%s,weight=%s,illDuration=%s,allergy=%s WHERE id = %s",
               [height,weight,illDuration,allergy,id])

if __name__ == '__main__':
    caseList = querys('select * from cases5', [], 'select')
    for i in caseList:
        spiderObj = spider(i[9])
        spiderObj.main(i[0])




