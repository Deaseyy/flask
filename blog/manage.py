
from flask import Flask
from flask_script import Manager

from back.models import db
from back.views import bblue
from web.views import wblue

app = Flask(__name__)
#第二步: 注册蓝图,可以使用蓝图blue管理路由了
app.register_blueprint(blueprint=bblue, url_prefix = '/back')
app.register_blueprint(blueprint=wblue, url_prefix = '/web')
# url_prefix 访问路由前缀


#配置session的加密方式
app.secret_key = 'asdfgh123456789qwert' #随便写


# 配置数据库信息
#mysql+pymysql://root:123456@127.0.0.1:3306/szflask1
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:450502@127.0.0.1:3306/szflask1'
db.init_app(app)


if __name__ == '__main__':
    manage = Manager(app)
    manage.run()