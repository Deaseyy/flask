import math

from flask import Blueprint, request, render_template, redirect, \
    url_for, session, jsonify
from sqlalchemy import or_,and_,not_
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import db, User, Article, Atc_type
from utils.functions import login_required  # 导入装饰器

# 第一步: 生成蓝图对象
# 蓝图用于管理路由


bblue = Blueprint('first',__name__)

# 第三步: 使用蓝图对象管理路由
@bblue.route('/index/', methods=['GET'])
@login_required  # 校验登陆
def index():
    atcs = Article.query.filter().all()
    users = User.query.filter().all()
    return render_template('back/index.html', atcs=atcs, users=users)


# 增加文章
@bblue.route('/add-article/', methods=['GET','POST'])
@login_required
def add_article():
    if request.method == 'GET':
        # 显示所有栏目分类到后台页面
        types = Atc_type.query.filter().all()
        return render_template('back/add-article.html', types=types)

    if request.method == 'POST':
        atc = Article()
        # 获取前端页面填写的数据
        atc.title = request.form.get('title')
        atc.desc = request.form.get('describe')
        atc.content = request.form.get('content')
        atc.type = int(request.form.get('category'))
        atc.uid = session.get('user_id')  # 从session中获取正在登陆的用户id
        # 存入数据库时,判断数据合法性
        res_title = Article.query.filter(Article.title==atc.title).first()
        if atc.title==None or res_title:
            error = '标题为空或已存在!'
            return render_template('back/add-article.html', title_err=error)
        if not atc.content:
            error = '内容不能为空!'
            return render_template('back/add-article.html', content_err=error)
        atc.save_update()
        return redirect(url_for('first.article'))


# 文章界面
@bblue.route('/article/',methods=['GET','POST'])
@login_required  # 校验登陆
def article():
    if request.method == 'GET':
        atcs_all = Article.query.filter().all()
        pages = list(range(math.ceil(len(atcs_all)/3)))  # 计算应该显示的页数
        # 默认显示第一页的数据
        atcs = Article.query.offset(0).limit(3).all()
        return render_template('back/article.html', atcs=atcs, pages=pages, atcs_all=atcs_all)

    if request.method == 'POST':
        page = int(request.form.get('page'))
        atcs = Article.query.offset((page - 1) * 3).limit(3).all()
        atcss = []
        for atc in atcs:
            atc_dict = {}
            atc_dict['id'] =atc.id
            atc_dict['title'] = atc.title
            atc_dict['desc'] = atc.desc
            atc_dict['content'] = atc.content
            atc_dict['create_time'] = atc.create_time.strftime('%Y-%m-%d %X')
            atc_dict['type'] = atc.type        # type保存的时类型的id
            atc_dict['uid'] = atc.uid
            atc_dict['tname'] = atc.tp.tname    # 获取类型名

            atcss.append(atc_dict)
        # return jsonify({'status':200})
        return jsonify({'atcss':atcss})



# 修改文章
@bblue.route('/update-article/<int:id>/',methods=['GET','POST'])
@login_required  # 校验登陆
def update_article(id):
    if request.method == 'GET':
        # 循环
        # 显示所有栏目分类到后台页面
        types = Atc_type.query.filter().all()
        # 显示需要修改的文章到后台页面
        atc_res = Article.query.filter(Article.id==id).first()
        return render_template('back/update-article.html', update_types=types, update_atc=atc_res )

    if request.method == 'POST':
        atc_res = Article.query.filter(Article.id == id).first()  # 找到修改对象对应的id,id由前端页面反向解析传回
        # 从网页表单获取数据
        title = request.form.get('title')
        content = request.form.get('content')
        desc = request.form.get('describe')
        type = request.form.get('category')
        # 保存修改数据
        atc_res.title = title
        atc_res.content = content
        atc_res.desc = desc
        atc_res.type = type
        atc_res.save_update()
        return redirect(url_for('first.article'))


# 删除单个文章
@bblue.route('/del-atc/<int:id>/',methods=['GET'])
@login_required  # 校验登陆
def del_atc(id):
    atc_res = Article.query.filter(Article.id == id).first()
    atc_res.delete()
    return redirect(url_for('first.article'))


# 删除所有勾选文章
@bblue.route('/del_all_atc/',methods=['GET','POST'])
@login_required  # 校验登陆
def del_all_atc():
    if request.method == 'POST':
        id_list = request.form.getlist('checkbox[]')  #getlist获取复选框提交的多个数据
        for id in id_list:
            atc_res = Article.query.filter(Article.id == id).first()
            atc_res.delete()
        return redirect(url_for('first.article'))


#栏目(文章分类)
@bblue.route('/category/', methods=['GET','POST'])
@login_required  # 校验登陆
def category():
    if request.method == 'GET':
        atc_types_res = Atc_type.query.filter().all()
        return render_template('back/category.html', atc_types=atc_types_res)  # 网页里传值传左边变量

    if request.method == 'POST':
        atc_type = Atc_type()   # 创建模型对象,即表的实体对象
        name = request.form.get('name')  # name:input输入框的name='name'属性对应值,取后者name变量
        keyword = request.form.get('keywords')
        describle = request.form.get('describe')
        atc_type.tname = name
        atc_type.keyword = keyword
        atc_type.desc = describle
        atc_type.save_update()  # 提交保存
        atc_types = Atc_type.query.filter().all()  #查找数据渲染到前端页面
        return render_template('back/category.html', atc_types=atc_types)


# 修改栏目
@bblue.route('/update-category/<int:id>/', methods=['GET','POST'])
@login_required  # 校验登陆
def update_category(id):  # id由前端页面点击链接url_for()反向解析传回
    if request.method == 'GET':
        res_type = Atc_type.query.filter(Atc_type.id == id).first()
        return render_template('back/update-category.html', update_type=res_type)

    if request.method == 'POST':
        atc_type_res = Atc_type.query.filter(Atc_type.id == id).first()  # 找到修改对象对应的id,id由前端页面反向解析传回
        # 从网页表单获取数据
        name = request.form.get('name')
        keyword = request.form.get('keywords')
        desc = request.form.get('describe')
        #保存数据
        atc_type_res.tname = name
        atc_type_res.keyword = keyword
        atc_type_res.desc = desc
        atc_type_res.save_update()
        return redirect(url_for('first.category'))


# 删除栏目
@bblue.route('/del_type/<int:id>/',methods=['GET'])
@login_required  # 校验登陆
def del_type(id):
    atc_type_res = Atc_type.query.filter(Atc_type.id == id).first()
    atc_type_res.delete()
    return redirect(url_for('first.category'))


# 登陆
@bblue.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':   # 直接get请求访问/login,渲染登陆页面
        # 访问该路由时,若返回get请求参数 exit==exit,执行退出登录操作
        if request.args.get('exit') == 'exit':
            session.pop('user_id')  #  删除session
            return redirect(url_for('first.login')) #退出登陆时,进入该路由地址带有参数, 重定向到/login/

        # 访问该路由时,从装饰器中返回get请求参数 error==error,渲染带有参数的login页面
        if request.args.get('error') == 'error':
            err = '未登录,请先登录!'
            return render_template('back/login.html',err=err)

        return render_template('back/login.html')

    if request.method == 'POST':  # 当有post请求提交到/login时,执行该语句,校验成功后,渲染主页面,结束
        # time.sleep(5)
        username = request.form.get('username')
        password = request.form.get('userpwd')
        user_res = User.query.filter(User.name == username).first() #查询
        if user_res == None:
            error = '账号不存在,请验证后再试!'
            return render_template('back/login.html', err=error)

        # if user_res.pwd != password:
        # 第一个参数写加密过的hash值,第二个写需要和它匹配的参数
        if check_password_hash(user_res.pwd,password) == False: #解密检测,相等返回True
            error = '密码错误,请重新输入!'
            return render_template('back/login.html', err=error)
        # 设置session存储的用户,需开头定义加密方式 app.secret_key = '随便写'
        session['user_id'] = user_res.id  # 将用户id存入session
        return redirect(url_for('first.index'))


# 注册
@bblue.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')
        password2 = request.form.get('userpwd2')
        if username and password and password2: #判断输入数据是否有为空
            user_res = User.query.filter(User.name == username).first()
            if user_res:  # 判断是否注册
                error = '该用户名已注册,请更换!'
                return render_template('back/register.html', err=error) #error需要页面的{{error}}接收
            if password != password2:
                error = '重复密码不一致!'
                return render_template('back/register.html', err=error)
            #保存用户
            user = User()
            user.name = username
            user.pwd = generate_password_hash(password) #加密保存到数据库
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('first.login'))
        return render_template('back/register.html')


# 修改个人信息(密码等,id,name不能修改)
@bblue.route('/info/', methods=['GET','POST'])
@login_required  # 校验登陆
def info():
    if request.method == 'GET':
        pass
    if request.method == 'POST':    # 通过ajax post请求传值
        old_password = request.form.get('old_pwd')
        new_password = request.form.get('new_pwd')
        new_password2 = request.form.get('new_pwd2')
        if check_password_hash(request.user.pwd, old_password ) == False:  # request:装饰器里绑定了user
            return jsonify({'res':0})
        if new_password != new_password2:
            return jsonify({'res':-1})
        # 保存修改
        request.user.pwd = generate_password_hash(new_password)
        request.user.save_update()
        return jsonify({'res':1})



@bblue.route('/create/',methods=['GET'])
def create_db():
    # 在数据库中生成表
    # 将模型映射成数据库的表(对第一次使用有用)
    db.create_all()
    return '创建表成功'

@bblue.route('/drop/',methods=['GET'])
def drop_db():
    # 删除数据库中所有的表
    db.drop_all()
    return '删除表成功'

