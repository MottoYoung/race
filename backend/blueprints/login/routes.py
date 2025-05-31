from flask import request, jsonify
from flask_cors import CORS
from .auth import register_user, login_user
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from . import bp

@bp.route('/register', methods=['POST'])
def register():
    logger.info("收到注册请求")
    data = request.get_json()
    
    if not data:
        logger.error("请求数据为空")
        return jsonify({'success': False, 'message': '无效的请求数据'}), 400
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    logger.info(f"注册信息: 邮箱={email}, 角色={role}")
    
    if not all([email, password, role]):
        logger.error("缺少必要字段")
        return jsonify({'success': False, 'message': '所有字段都是必填的'}), 400
    
    try:
        response, status_code = register_user(email, password, role)
        logger.info(f"注册结果: {response}, 状态码={status_code}")
        return jsonify(response), status_code
    except Exception as e:
        logger.exception("注册过程发生错误")
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login():
    logger.info("收到登录请求")
    data = request.get_json()
    
    if not data:
        logger.error("请求数据为空")
        return jsonify({'success': False, 'message': '无效的请求数据'}), 400
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    logger.info(f"登录信息: 邮箱={email}, 角色={role}")
    
    if not all([email, password, role]):
        logger.error("缺少必要字段")
        return jsonify({'success': False, 'message': '所有字段都是必填的'}), 400
    
    try:
        response, status_code = login_user(email, password, role)
        logger.info(f"登录结果: {response}, 状态码={status_code}")
        return jsonify(response), status_code
    except Exception as e:
        logger.exception("登录过程发生错误")
        return jsonify({'success': False, 'message': f'服务器错误: {str(e)}'}), 500

@bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'API服务正常运行'}), 200
