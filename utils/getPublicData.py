from utils.query import querys

def getAllCasesData():
    allCasesData = querys('select * from cases_copy1',[],'select')
    return allCasesData

def getAllUsersData():
    getAllUsersData = querys('select * from users',[],'select')
    return getAllUsersData