# 此文件已被迁移到routes.py中，保留此文件仅作为参考
# 如果直接运行此文件，则使用独立模式启动服务

from flask import Flask
from flask_cors import CORS  # 引入 CORS
from routes import bp

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)  # 启用 CORS
    
    # 注册蓝图
    app.register_blueprint(bp, url_prefix='/api')
    
    app.run(port=2204, debug=True)