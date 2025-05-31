import os

class Config:
    """Flask应用的基本配置类"""
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed-in-production'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 最大上传限制50MB
    
    # 数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or '312237'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'smartprep'
    
    # 讯飞API配置
    XF_APP_ID = os.environ.get('XF_APP_ID') or 'b341104d'
    XF_API_KEY = os.environ.get('XF_API_KEY') or '569e475ac59475111c80757a163407b9'
    XF_API_SECRET = os.environ.get('XF_API_SECRET') or 'YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz'
    
    # 讯飞星火大模型配置
    SPARK_APP_ID = os.environ.get('SPARK_APP_ID') or 'b341104d'
    SPARK_API_KEY = os.environ.get('SPARK_API_KEY') or '569e475ac59475111c80757a163407b9'
    SPARK_API_SECRET = os.environ.get('SPARK_API_SECRET') or 'YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz'
    
    # 深思考模型配置
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY') or 'sk-YjWqwufd8oH0EWTaS3Kfts8rWcPpp9GNqsnblVKQ9fCj8vNt'
    DEEPSEEK_BASE_URL = os.environ.get('DEEPSEEK_BASE_URL') or 'https://api.lkeap.cloud.tencent.com/v1'
    
    # 知智AI配置
    ZHIPU_API_KEY = os.environ.get('ZHIPU_API_KEY') or '3f29f735972641eea247413ef035ed44.18B04xjjzbdjv1L9'

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 在生产环境中应使用更强的密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-secret-key'

# 设置配置映射
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}
