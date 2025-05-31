import os

class PPTvConfig:
    # 基本路径配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'static', 'outputs')
    
    # 文件大小限制 (50MB)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    
    # API密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # 讯飞API配置
    XF_APP_ID = os.environ.get('XF_APP_ID') or 'b341104d'
    XF_API_KEY = os.environ.get('XF_API_KEY') or '569e475ac59475111c80757a163407b9'
    XF_API_SECRET = os.environ.get('XF_API_SECRET') or 'YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz'
    
    # 星火大模型配置
    SPARK_APP_ID = os.environ.get('SPARK_APP_ID') or 'b341104d'
    SPARK_API_KEY = os.environ.get('SPARK_API_KEY') or '569e475ac59475111c80757a163407b9'
    SPARK_API_SECRET = os.environ.get('SPARK_API_SECRET') or 'YWI5ZDRhNTdmNGZjNmVjYjg3OWMwZGUz' 