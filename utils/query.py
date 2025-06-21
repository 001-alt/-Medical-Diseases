import pymysql
import logging
import json
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('database')

def querys(sql, params, type='no_select'):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        database='medicalinfo',
        port=3306,
        charset='utf8mb4'
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if type == 'select':
                return cursor.fetchall()  # 返回查询结果
            elif type == 'insert':
                connection.commit()  # 提交插入操作
                return cursor.lastrowid  # 返回插入的行 ID
            else:
                connection.commit()  # 提交其他操作
                return True  # 返回 True 表示成功
    except Exception as e:
        logger.error(f"Database error: {e}")
        connection.rollback()
        return False  # 返回 False 表示失败
    finally:
        connection.close()

def checkUserExist(username):
    sql = "SELECT * FROM users WHERE username = %s"
    result = querys(sql, (username,), 'select')
    return result[0] if result else None

def addUser(username, password, email, gender):
    sql = """INSERT INTO users (username, password, email, gender)
             VALUES (%s, %s, %s, %s)"""
    return querys(sql, (username, password, email, gender), 'insert')

def getUserById(user_id):
    sql = "SELECT * FROM users WHERE id = %s"
    result = querys(sql, (user_id,), 'select')
    return result[0] if result else None

def updateUser(user_id, username=None, password=None, email=None, gender=None):
    updates = []
    params = []

    if username:
        updates.append("username = %s")
        params.append(username)
    if password:
        updates.append("password = %s")
        params.append(password)
    if email:
        updates.append("email = %s")
        params.append(email)
    if gender:
        updates.append("gender = %s")
        params.append(gender)

    if not updates:
        return False  # 如果没有更新的数据，返回 False

    sql = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
    params.append(user_id)

    return querys(sql, tuple(params), 'no_select')

def deleteUser(user_id):
    sql = "DELETE FROM users WHERE id = %s"
    return querys(sql, (user_id,), 'no_select')

def getAllUsers():
    sql = "SELECT * FROM users"
    return querys(sql, (), 'select')  # 返回所有用户

def log_operation(user_id, action, details=None):
    sql = """
    INSERT INTO operation_logs (user_id, action, details)
    VALUES (%s, %s, %s)
    """
    try:
        querys(sql, (user_id, action, details), 'insert')
    except Exception as e:
        logger.error(f"记录操作日志时出错: {e}")


def getAllOperationLogs():
    sql = "SELECT * FROM operation_logs ORDER BY timestamp DESC"
    try:
        rows = querys(sql, (), 'select')
        logs = []
        for row in rows:
            log_entry = {
                "id": row[0],
                "user_id": row[1],
                "action": row[2],
                "details": row[3],
                "timestamp": row[4].strftime("%Y-%m-%d %H:%M:%S") if row[4] else None
                # 直接调用时间对象的 strftime 方法
            }
            logs.append(log_entry)

        return {
            "status": "success",
            "message": "获取操作日志成功",
            "logs": logs
        }
    except Exception as e:
        logger.error(f"获取操作日志失败: {str(e)}")
        return {
            "status": "error",
            "message": f"获取操作日志失败: {str(e)}",
            "logs": []
        }


