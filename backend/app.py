import os
from flask import Flask
from flask_cors import CORS
from config import config_by_name

def create_app(config_name='dev'):
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config_by_name[config_name])
    
    # 配置CORS，允许跨域请求
    CORS(app)
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 注册所有蓝图
    register_blueprints(app)
    
    # 返回创建好的应用
    return app

def register_blueprints(app):
    """注册所有蓝图模块"""
    # 登录注册模块
    from blueprints.login import bp as login_bp
    app.register_blueprint(login_bp)
    
    # 教案生成模块
    from blueprints.jiaoan import bp as jiaoan_bp
    app.register_blueprint(jiaoan_bp)
    
    # 练习题生成模块
    from blueprints.exercise import bp as exercise_bp
    app.register_blueprint(exercise_bp)
    
    # 图片生成模块
    from blueprints.picturegenerater import bp as picturegenerater_bp
    app.register_blueprint(picturegenerater_bp)
    
    # PPT生成模块
    from blueprints.ppt import bp as ppt_bp
    app.register_blueprint(ppt_bp)
    
    # PPT视频转换模块
    from blueprints.pptvideo import bp as pptvideo_bp
    app.register_blueprint(pptvideo_bp)
    
    # 视频生成模块
    from blueprints.videomaker import bp as videomaker_bp
    app.register_blueprint(videomaker_bp)
    
    # 添加EXE执行器模块
    from blueprints.exerunner import bp as exerunner_bp
    app.register_blueprint(exerunner_bp)
    
    # 推荐模块
    from blueprints.recommend.backend.routes import bp as recommend_bp
    app.register_blueprint(recommend_bp)
    
    # 可以在这里注册其他蓝图...

if __name__ == '__main__':
    # 创建应用实例
    app = create_app(os.getenv('FLASK_ENV', 'dev'))
    
    # 打印应用路由表，便于调试
    print("====================================")
    print("综合服务启动中...")
    print("以下服务已合并到同一个端口:")
    for rule in app.url_map.iter_rules():
        print(f"接口名{rule.endpoint}----------接口路径{rule.rule}")
    
    # 运行应用
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 2200))
    debug = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
