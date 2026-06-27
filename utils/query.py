import pymysql
import os
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('database')

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'root'),
    'database': os.environ.get('DB_NAME', 'medicalinfo'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'charset': 'utf8mb4'
}

def querys(sql, params, type='no_select'):
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if type == 'select':
                return cursor.fetchall()
            elif type == 'insert':
                connection.commit()
                return cursor.lastrowid
            else:
                connection.commit()
                return True
    except Exception as e:
        logger.error(f"Database error: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def checkUserExist(username):
    sql = "SELECT * FROM users WHERE username = %s"
    result = querys(sql, (username,), 'select')
    return result[0] if result else None

def addUser(username, password, email, gender):
    sql = """INSERT INTO users (username, password, email, gender) VALUES (%s, %s, %s, %s)"""
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
        return False
    sql = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
    params.append(user_id)
    return querys(sql, tuple(params), 'no_select')

def deleteUser(user_id):
    sql = "DELETE FROM users WHERE id = %s"
    return querys(sql, (user_id,), 'no_select')

def getAllUsers():
    sql = "SELECT * FROM users"
    return querys(sql, (), 'select')

def log_operation(user_id, action, details=None):
    sql = """INSERT INTO operation_logs (user_id, action, details) VALUES (%s, %s, %s)"""
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
            }
            logs.append(log_entry)
        return {"status": "success", "message": "获取操作日志成功", "logs": logs}
    except Exception as e:
        logger.error(f"获取操作日志失败: {str(e)}")
        return {"status": "error", "message": f"获取操作日志失败: {str(e)}", "logs": []}
