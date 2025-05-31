import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # 根据您的MySQL设置更改
    MYSQL_PASSWORD = '312237'  # 根据您的MySQL设置更改
    MYSQL_DB = 'smartprep'
    MYSQL_CURSORCLASS = 'DictCursor'

# 登录和注册模块的配置文件