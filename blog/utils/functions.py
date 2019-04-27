
# 外层函数嵌套内层函数
# 外岑函数返回内层函数
# 内层函数调用外层函数的参数

from functools import wraps

from flask import session, render_template, redirect, url_for,request


# 用装饰器封装函数,校验登录状态
from werkzeug.security import check_password_hash, generate_password_hash

from back.models import  User


def login_required(func):
    @wraps(func)  #调用func时,打印func还是func,只是增加了装饰器一些功能,不再是装饰器函数
    def check(*args,**kwargs):
        try:
            # 登陆情况
            #func()为被login_required装饰的函数
            user_id = session['user_id'] # []方法取值 ,如果取不到就会报错, get()会返回一个None

            # 在后端页面head部分显示用户名和个人信息修改
            userid = session.get('user_id')
            user = User.query.filter(User.id==userid).first()
            # 给request动态绑定一个属性user,将从session获取到的user存进user
            request.user = user # 发出网页请求时,位于页面上的{{ request }}可以被动态解析,从request上获取到user

            return func(*args,**kwargs)
        except Exception as e:    # 报错后直接执行该语句
            print(e)
            #没登陆的情况
            # error = '<h2 style="color:red; font-size:30px; width:300px; margin:0 auto "> 未登录,请先登陆! <h2>'
            return redirect(url_for('first.login',error='error'))  #传一个get求参数到login页面,(路由/login/后不带<>时,默认为?error=error)

    return check
