from flask import Flask
from models import db, PageList, Object, ObjectField, PageListField, PageLayout, PageLayoutField

app = Flask(__name__)

# 配置数据库 URI（这里假设使用 MySQL）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/local_demo?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用对象修改追踪

# 初始化 SQLAlchemy
db.init_app(app)
with app.app_context():
    db.create_all()
@app.route('/')
def index():
    return "Hello, Flask with SQLAlchemy!"

if __name__ == "__main__":
    app.run(debug=True)

