from flask import Flask, request, jsonify
from machine.tree import *
from utils.getPublicData import *
from utils.getAllData import *
import bcrypt
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from utils.query import *  # 确保这个模块中有数据库操作相关函数
import logging
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
app = Flask(__name__)

# 数据库连接配置
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='medicalinfo',
    port=3306,
    charset='utf8mb4'
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置 CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# JWT 配置
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 更换为您的密钥
jwt = JWTManager(app)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getHomeData', methods=['GET', 'POST'])
def getHomeData():
    try:
        pieData = getPieData()
        configOne = getConfigOne()
        casesData = list(getAllCasesData())
        maxNum, maxType, maxDep, maxHos, maxAge, minAge = getFoundData()
        boyList, girlList, ratioData = getGenderData()
        circleData = getCircleData()
        wordData = getWordData()
        xData, y1Data, y2Data = getBodyData()

        return jsonify({
            'message': 'success',
            'code': 200,
            'data': {
                'pieData': pieData,
                'configOne': configOne,
                'casesData': casesData,
                'maxNum': maxNum,
                'maxType': maxType,
                'maxDep': maxDep,
                'maxHos': maxHos,
                'maxAge': maxAge,
                'minAge': minAge,
                'boyList': boyList,
                'girlList': girlList,
                'ratioData': ratioData,
                'circleData': circleData,
                'wordData': wordData,
                'lastData': {
                    'xData': xData,
                    'y1Data': y1Data,
                    'y2Data': y2Data,
                }
            }
        })
    except Exception as e:
        logger.error(f"获取首页数据失败: {str(e)}")
        return jsonify({"code": 500, "message": "获取数据失败", "data": {}}), 500

def save_prediction(input_text, prediction_result):
    try:
        with connection.cursor() as cursor:
            # 插入数据的 SQL 语句
            sql = """
            INSERT INTO predictions (input_text, prediction_result)
            VALUES (%s, %s)
            """
            # 执行插入操作
            cursor.execute(sql, (input_text, prediction_result))
            connection.commit()  # 提交事务
            logger.info("预测数据已成功插入到数据库。")
    except Exception as e:
        logger.error(f"插入数据时出错: {e}")
        connection.rollback()  # 出现异常时回滚事务

@app.route('/submitModel', methods=['GET', 'POST'])
def submitModel():
    if request.method == 'POST':
        content = request.json.get('content', '')
        logger.info(f"Received content: {content}")
        # 运行模型进行预测
        result, error = train_and_predict(content)
        if error:
            return jsonify({
                'code': 500,
                'message': error,
                'data': {}
            })
        # 保存输入和结果到数据库
        save_prediction(content, result)
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'inputContent': content,     # 返回输入内容
                'resultData': result         # 返回预测结果
            }
        })
    else:
        return jsonify({'code': 200, 'message': 'success', 'data': {}})


@app.route('/getPredictions', methods=['GET'])
def get_predictions():
    try:
        # 从数据库中查询预测结果，选择所需的字段
        predictions = querys('SELECT input_text, prediction_result, created_at FROM predictions', [], 'select')
        # 处理查询结果，转化为返回格式
        result_data = []
        for prediction in predictions:
            result_data.append({
                'input_text': prediction[0],  # input_text 在第一列
                'prediction_result': prediction[1],  # prediction_result 在第二列
                'created_at': prediction[2].isoformat()  # created_at 在第三列，转换为 ISO 8601 格式字符串
            })
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result_data
        })
    except Exception as e:
        logger.error(f"Error fetching predictions: {e}")
        return jsonify({
            'code': 500,
            'message': 'Failed to fetch predictions',
            'data': {}
        })

@app.route('/tableData', methods=['GET', 'POST'])
def tableData():
    try:
        tableDataList = getAllCasesData()
        # 只获取前500行数据
        resultData = [x[1:] for x in tableDataList][:500]
        logger.info(f"返回表格数据: {resultData}")
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'resultData': resultData
            }
        })
    except Exception as e:
        logger.error(f"获取表格数据失败: {str(e)}")
        return jsonify({"code": 500, "message": "获取数据失败", "data": {}}), 500

@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    try:
        users = getUserData()
        if not users:
            return jsonify({
                "status": "success",
                "message": "没有找到用户数据",
                "users": []
            })

        return jsonify({
            "status": "success",
            "message": "获取用户数据成功",
            "users": users
        })
    except Exception as e:
        logger.error(f"获取用户数据失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"获取用户数据失败: {str(e)}",
            "users": []
        })

@app.route('/addUser', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    email = data.get('email')
    gender = data.get('gender')

    if not name or not password or not email:
        return jsonify({"status": "error", "message": "缺少必要字段"}), 400

    hashed_password = generate_password_hash(password)
    try:
        user_id = addUser(name, hashed_password, email, gender)
        log_operation(user_id, "添加用户", f"用户 {name} 被添加.")
        return jsonify({"status": "success", "message": "用户添加成功"}), 201
    except Exception as e:
        logger.error(f"添加用户失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/updateUser/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    username = data.get('name')
    password = data.get('password')
    email = data.get('email')
    gender = data.get('gender')

    try:
        user = getUserById(user_id)
        if user is None:
            return jsonify({"status": "error", "message": "用户未找到"}), 404

        updateUser(user_id, username=username, password=generate_password_hash(password), email=email, gender=gender)
        log_operation(user_id, "更新用户", f"用户 {user_id} 信息已更新.")
        return jsonify({"status": "success", "message": "用户信息更新成功"}), 200
    except Exception as e:
        logger.error(f"更新用户失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/deleteUser/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = getUserById(user_id)
        if user is None:
            return jsonify({"status": "error", "message": "用户未找到"}), 404

        deleteUser(user_id)
        log_operation(user_id, "删除用户", f"用户 {user_id} 被删除.")
        return jsonify({"status": "success", "message": "用户删除成功"}), 200
    except Exception as e:
        logger.error(f"删除用户失败: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = checkUserExist(username)
    if not user:
        return jsonify({"status": "error", "message": "用户不存在"}), 401

    if check_password_hash(user[2], password):
        access_token = create_access_token(identity=username)
        log_operation(user[0], "用户登录", f"用户 {username} 登录成功.")
        return jsonify({
            "status": "success",
            "message": "登录成功",
            "access_token": access_token,
            "user_info": {
                "id": user[0],
                "username": user[1],
                "email": user[3],
                "gender": user[4]
            }
        }), 200
    else:
        return jsonify({"status": "error", "message": "密码错误"}), 401

@app.route('/getOperationLogs', methods=['GET'])
def get_operation_logs():
    try:
        logs_data = getAllOperationLogs()
        if logs_data['status'] == 'success':
            return jsonify({
                'status': 'success',
                'message': '获取日志成功',
                'logs': logs_data['logs']
            })
        else:
            return jsonify(logs_data), 500
    except Exception as e:
        logger.error(f"获取操作日志失败: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"获取操作日志失败: {str(e)}",
            "logs": []
        }), 500



if __name__ == "__main__":
    app.run(debug=True)

# 确保在应用关闭时关闭数据库连接
@app.teardown_appcontext
def close_connection(exception):
    if connection:
        connection.close()