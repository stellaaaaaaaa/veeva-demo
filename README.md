# 首次启动需配置数据库 点开config.py文件
启动项目先重新配置SQLALCHEMY_DATABASE_URI参数，格式为'mysql://username:password@localhost/<table_name>?charset=utf8mb4'
default:
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/local-demo?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
