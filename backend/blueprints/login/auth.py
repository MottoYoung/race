import re
import logging
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from pymysql.cursors import DictCursor

from .config import Config  # 修改为相对导入

# 配置日志
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        return connection
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        raise

def validate_password(password):
    # 密码必须含有大小写字母加数字的组合
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True

def validate_email(email):
    # 验证邮箱格式
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def register_user(email, password, role):
    logger.info(f"处理用户注册: 邮箱={email}, 角色={role}")
    
    # 管理员不能注册
    if role == 'admin':
        logger.warning("尝试注册管理员账号被拒绝")
        return {'success': False, 'message': '管理员账号不允许注册'}, 400
    
    # 验证邮箱格式
    if not validate_email(email):
        logger.warning(f"邮箱格式无效: {email}")
        return {'success': False, 'message': '请输入有效的邮箱地址'}, 400
    
    # 验证密码强度
    if not validate_password(password):
        logger.warning("密码强度不满足要求")
        return {'success': False, 'message': '密码必须包含大小写字母和数字，且长度至少为8位'}, 400
    
    # 哈希处理密码
    hashed_password = generate_password_hash(password)
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 检查邮箱是否已存在
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            if cursor.fetchone():
                logger.warning(f"邮箱已存在: {email}")
                return {'success': False, 'message': '该邮箱已被注册'}, 400
            
            # 插入新用户
            sql = 'INSERT INTO users (email, password, role) VALUES (%s, %s, %s)'
            cursor.execute(sql, (email, hashed_password, role))
            conn.commit()
            logger.info(f"用户注册成功: {email}")
            return {'success': True, 'message': '注册成功'}, 201
    except Exception as e:
        logger.exception(f"注册过程发生错误: {str(e)}")
        return {'success': False, 'message': f'注册失败: {str(e)}'}, 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def login_user(email, password, role):
    logger.info(f"处理用户登录: 邮箱={email}, 角色={role}")
    
    # 管理员特殊处理
    if role == 'admin':
        if email != 'admin' or password != 'admin':
            logger.warning("管理员登录失败: 账号或密码错误")
            return {'success': False, 'message': '管理员账号或密码错误'}, 401
        logger.info("管理员登录成功")
        return {
            'success': True, 
            'message': '管理员登录成功', 
            'user': {'id': 0, 'email': 'admin', 'role': 'admin'}
        }, 200
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE email = %s AND role = %s', (email, role))
            user = cursor.fetchone()
            
            if user and check_password_hash(user['password'], password):
                # 不要返回密码
                user.pop('password', None)
                logger.info(f"用户登录成功: {email}")
                return {'success': True, 'message': '登录成功', 'user': user}, 200
            else:
                logger.warning(f"用户登录失败: {email}")
                return {'success': False, 'message': '邮箱或密码错误，或角色选择有误'}, 401
    except Exception as e:
        logger.exception(f"登录过程发生错误: {str(e)}")
        return {'success': False, 'message': f'登录失败: {str(e)}'}, 500
    finally:
        if 'conn' in locals() and conn:
            conn.close()