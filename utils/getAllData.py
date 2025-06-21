from collections import UserList

from utils.getPublicData import getAllCasesData
from utils.getPublicData import getAllUsersData
import datetime


def getPieData():
    caseList = getAllCasesData()
    ageDic = {'0-10岁': 0, '10-20岁': 0, '20-30岁': 0, '30-40岁': 0, '40-50岁': 0, '50-60岁': 0, '60岁以上': 0, }
    for caseItem in caseList:
        if int(caseItem[3]) < 10:
            ageDic['0-10岁'] += 1
        elif int(caseItem[3]) < 20:
            ageDic['10-20岁'] += 1
        elif int(caseItem[3]) < 30:
            ageDic['20-30岁'] += 1
        elif int(caseItem[3]) < 40:
            ageDic['30-40岁'] += 1
        elif int(caseItem[3]) < 50:
            ageDic['40-50岁'] += 1
        elif int(caseItem[3]) < 60:
            ageDic['50-60岁'] += 1
        else:
            ageDic['60岁以上'] += 1
    # print(ageDic)
    listResult = []
    for k, v in ageDic.items():
        listResult.append({
            'name': k,
            'value': v,
        })
    # print(listResult)
    return listResult


def getConfigOne():
    caseList = getAllCasesData()
    caseDic = {}
    for caseItem in caseList:
        if caseDic.get(caseItem[1], -1) == -1:
            caseDic[caseItem[1]] = 1
        else:
            caseDic[caseItem[1]] += 1
    listResult = []
    for k, v in caseDic.items():
        listResult.append({
            'name': k,
            'value': v,
        })

    return listResult[:8]


def getFoundData():
    caseList = getAllCasesData()
    maxNum = len(list(caseList))
    typeDic = {}
    depDic = {}
    hosDic = {}
    maxAge = float('-inf')  # 初始化为负无穷
    minAge = float('inf')  # 初始化为正无穷
    for caseItem in caseList:
        # 类型
        if typeDic.get(caseItem[1], -1) == -1:
            typeDic[caseItem[1]] = 1
        else:
            typeDic[caseItem[1]] += 1
        # 科室
        if depDic.get(caseItem[8], -1) == -1:
            depDic[caseItem[8]] = 1
        else:
            depDic[caseItem[8]] += 1
        # 医院
        if hosDic.get(caseItem[7], -1) == -1:
            hosDic[caseItem[7]] = 1
        else:
            hosDic[caseItem[7]] += 1
        # 年龄
        currentAge = int(caseItem[3])
        if currentAge > maxAge:
            maxAge = currentAge
        if currentAge < minAge:
            minAge = currentAge

    typeSort = sorted(typeDic.items(), key=lambda data: data[1], reverse=True)
    depSort = sorted(depDic.items(), key=lambda data: data[1], reverse=True)
    hosSort = sorted(hosDic.items(), key=lambda data: data[1], reverse=True)
    maxType = typeSort[0][0]
    maxDep = depSort[0][0]
    maxHos = hosSort[0][0]
    return maxNum,maxType,maxDep,maxHos,maxAge,minAge


def getGenderData():
    caseList = getAllCasesData()
    boyDic = {}
    girlDic = {}
    girlNum = 0
    boyNum = 0
    for caseItem in caseList:
        if caseItem[2] == '男':
            boyNum += 1
            if boyDic.get(caseItem[1], -1) == -1:
                boyDic[caseItem[1]] = 1
            else:
                boyDic[caseItem[1]] += 1
        elif caseItem[2] == '女':
            girlNum += 1
            if girlDic.get(caseItem[1], -1) == -1:
                girlDic[caseItem[1]] = 1
            else:
                girlDic[caseItem[1]] += 1
    ratioData =[]
    boyRatio = int(round(boyNum / len(caseList) * 100, 0))
    girlRatio = int(round(girlNum / len(caseList) * 100, 0))
    print(boyRatio, girlRatio)
    ratioData.append(boyRatio)
    ratioData.append(girlRatio)
    boyList = []
    girlList = []
    for k, v in boyDic.items():
        boyList.append({
            'name': k,
            'value': v,
        })
    for k, v in girlDic.items():
        girlList.append({
            'name': k,
            'value': v,
        })
    return boyList, girlList, ratioData

def getCircleData():
    casesList = getAllCasesData()
    depDic = {}
    for caseItem in casesList:
        if depDic.get(caseItem[8], -1) == -1:
            depDic[caseItem[8]] = 1
        else:
            depDic[caseItem[8]] += 1
    dataSort = sorted(depDic.items(), key=lambda data: data[1], reverse=True)
    dataResultList = []
    for i in dataSort:
        dataResultList.append({
            'name': i[0],
            'value': i[1],
        })
    return dataResultList

def getWordData():
    caseList = getAllCasesData()
    caseDic = {}
    for caseItem in caseList:
        if caseDic.get(caseItem[1], -1) == -1:
            caseDic[caseItem[1]] = 1
        else:
            caseDic[caseItem[1]] += 1
    wordResult = []
    for k, v in caseDic.items():
        wordResult.append({
            'name': k,
            'value': v,
        })
    return wordResult

def getBodyData():
    caseList = getAllCasesData()
    dataDic = {}
    xData = []
    sumData = []
    for caseItem in caseList:
        if dataDic.get(caseItem[1], -1) == -1:
            dataDic[caseItem[1]] = 1
        else:
            dataDic[caseItem[1]] += 1
    dataSort = sorted(dataDic.items(), key=lambda data: data[1], reverse=True)
    for i in dataSort:
        xData.append(i[0])
        sumData.append(i[1])
    y1Data = [0 for x in range(len(xData))]
    y2Data = [0 for x in range(len(xData))]
    for caseItem in caseList:
        for index,x in enumerate(xData):
            if caseItem[1] == x:
                if caseItem[10] and caseItem[11] == '无':
                    y1Data[index] += 0
                    y2Data[index] += 0
                else:
                    y1Data[index] += int(caseItem[10])
                    y2Data[index] += int(caseItem[11])
    for index,s in enumerate(sumData):
        y1Data[index] = round(y1Data[index] / sumData[index],0)
        y2Data[index] = round(y2Data[index] / sumData[index],0)
    print(xData,y1Data,y2Data)
    return xData,y1Data,y2Data

def getUserData():
    users = getAllUsersData()
    # 直接返回用户数据
    return users


