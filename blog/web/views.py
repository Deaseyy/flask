import math

from flask import Blueprint, request, render_template,redirect,\
    url_for
from flask.json import jsonify
from sqlalchemy import or_,and_,not_

from back.models import Article, Atc_type

# 第一步: 生成蓝图对象
# 蓝图用于管理路由
wblue = Blueprint('web', __name__)



# 默认渲染分页第一页
def default_page():
    atcs_all = Article.query.filter().all()
    pages = list(range(math.ceil(len(atcs_all) / 5)))  # 计算应该显示的页数
    # 默认显示第一页的数据
    atcs = Article.query.order_by(-Article.create_time).offset(0).limit(5).all()
    res = [atcs_all, pages, atcs]
    return res

# ajax分页
def ajax_page(atcs):
    atcss = []
    for atc in atcs:
        atc_dict = {}
        atc_dict['id'] = atc.id
        atc_dict['title'] = atc.title
        atc_dict['desc'] = atc.desc
        atc_dict['content'] = atc.content
        atc_dict['create_time'] = atc.create_time.strftime('%Y-%m-%d %X')
        atc_dict['type'] = atc.type  # type保存的时类型的id
        atc_dict['uid'] = atc.uid
        atc_dict['tname'] = atc.tp.tname  # 获取类型名
        atcss.append(atc_dict)
    # return jsonify({'status':200})
    return jsonify({'atcss': atcss})



# 网站主页
@wblue.route('/home/',methods=['GET'])
def home():
    # 显示左侧栏目分类
    types = Atc_type.query.filter().all()
    res = default_page()
    return render_template('web/home.html', types=types, pages=res[1], atcs=res[2])


# 相册
@wblue.route('/photo/',methods=['GET'])
def photo():

    return render_template('web/photo.html')


# 文章分享主页
@wblue.route('/share/',methods=['GET','POST'])
def share():
    if request.method == 'GET':
        # 显示左侧文章分类
        types = Atc_type.query.filter().all()
        # 最近更新
        recent_atcs = Article.query.order_by(-Article.create_time).offset(0).limit(8).all()
        # 默认显示第一页文章数据
        res = default_page()
        return render_template('web/share.html', types=types, pages=res[1], atcs=res[2],recent_atcs=recent_atcs)

    if request.method == 'POST':
        page = int(request.form.get('page'))
        atcs = Article.query.order_by(-Article.create_time).offset((page - 1) * 5).limit(5).all()
        return ajax_page(atcs)


# 所选栏目的所有文章界面
@wblue.route('/share/<string:tname>/',methods=['GET', 'POST'])
def category(tname):
    if request.method == 'GET':
        # 显示左侧栏目分类
        types = Atc_type.query.filter().all()
        # 显示该类所有文章
        type = Atc_type.query.filter(Atc_type.tname == tname).first() #查找到指定类的对象
        pages = list(range(math.ceil(len(type.atcs) / 5)))  # 计算应该显示的页数
        # 默认显示第一页的数据
        atcs = Article.query.filter(Article.type==type.id).order_by(-Article.create_time).offset(0).limit(5).all()
        # 最近更新
        recent_atcs = Article.query.order_by(-Article.create_time).offset(0).limit(8).all()
        return render_template('web/share.html', atcs=atcs, types=types, pages=pages, recent_atcs=recent_atcs)  #类型对象.关联关系(atcs) 得到所有该类文章
    if request.method == 'POST':
        page = int(request.form.get('page'))
        type = Atc_type.query.filter(Atc_type.tname == tname).first()  # 查找到指定类的对象
        atcs = Article.query.filter(Article.type==type.id).order_by(-Article.create_time).offset((page - 1) * 5).limit(5).all()
        return ajax_page(atcs)


# 显示选定文章的内容界面
@wblue.route('/share/show_atc/<int:id>/',methods=['GET'])
def show_atc(id):
    # 显示左侧栏目分类
    types = Atc_type.query.filter().all()
    # 显示文章内容
    atc = Article.query.filter(Article.id == id).first()
    # 最近更新
    recent_atcs = Article.query.order_by(-Article.create_time).offset(0).limit(8).all()
    return render_template('web/share.html', atc=atc, types=types, recent_atcs=recent_atcs)


# 关于我
@wblue.route('/about/',methods=['GET'])
def about():
        return render_template('web/about.html')


@wblue.route('/info/',methods=['GET'])
def info():
        return render_template('web/info.html')

