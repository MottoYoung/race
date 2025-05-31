from flask import request, jsonify
from flask_cors import CORS
from .word2picture import generate_image
from .math_draw import execute_math_code
from .sparkAPI import generate_code
import logging
import ast
from . import bp

# 配置信息
CONFIG = {
    # sparkAPI配置信息
    'APPID': 'b341104d',
    'APIKEY': '569e475ac59475111c80757a163407b9',
    'APISECRET': 'YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz',
    # 图片生成
    'PAPPID': 'b341104d',
    'PAPIKEY': '569e475ac59475111c80757a163407b9',
    'PAPISECRET': 'YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz'
}

# 设置日志记录
logging.basicConfig(level=logging.DEBUG)

# 生成图片接口
@bp.route('/generate', methods=['POST'])
def handle_generate():
    data = request.get_json()
    mode = data.get('mode', 'normal')  # 新增模式参数
    print(f"收到请求: {data}")  # 添加日志
    # 根据模式选择不同的处理逻辑  数学/普通
    if mode == 'math':
        return handle_math_generation(data)
    else:
        return handle_normal_generation(data)

# 1.处理普通文本生成图片
def handle_normal_generation(data):
    # 获取输入参数
    text = data.get('text')
    resolution = data.get('resolution', '512x512')
    # 检查输入参数
    if not text:
        return jsonify({'error': 'Missing text input'}), 400
    # 解析分辨率
    try:
        width, height = map(int, resolution.split('x'))
    except Exception as e:
        logging.error(f"Invalid resolution format: {str(e)}")
        return jsonify({'error': 'Invalid resolution format'}), 400
    # 生成图片
    try:
        image_base64 = generate_image(text, CONFIG['PAPPID'], 
                                    CONFIG['PAPIKEY'], CONFIG['PAPISECRET'],
                                    width, height)
        return jsonify({'image': image_base64})
    except Exception as e:
        logging.error(f"Error in handle_normal_generation: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 2.处理数学文本生成图片
def handle_math_generation(data):
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Missing math description'}), 400
    
    try:
        # 第一步：生成绘图代码
        code = generate_code(
            text,
            CONFIG['APPID'],
            CONFIG['APIKEY'],
            CONFIG['APISECRET']
        )
        print(f"生成的绘图代码: {code}")  # 添加日志
        
        # 代码预处理，清洗掉不必要的内容
        code = (
            code.replace('```python', '')
                .replace('```', '')
                .replace('plt.show()', '')
                .replace('plt.savefig(', '# plt.savefig(')  # 注释掉保存语句
                .strip()
        )
        # 添加必要的头文件校验
        required_imports = [
            'import matplotlib.pyplot as plt',
            'import numpy as np'
        ]
        for imp in required_imports:
            if imp not in code:
                code = imp + '\n' + code
        
        # 检查生成的代码是否有语法错误
        try:
            ast.parse(code)
        except SyntaxError as e:
            logging.error(f"Syntax error in generated code: {str(e)}")
            return jsonify({'error': f'Syntax error in generated code: {str(e)}'}), 400
        
        # 第二步：执行生成的代码
        image_base64 = execute_math_code(code)
        if not image_base64.startswith('iVBORw0KGgo'):
            raise ValueError('生成的图片数据异常')
        return jsonify({'image': image_base64})
    
    except Exception as e:
        logging.error(f"Error in handle_math_generation: {str(e)}")
        return jsonify({'error': str(e)}), 500
