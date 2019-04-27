from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)
    pwd = db.Column(db.String(255))
    isdelete = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    atcs = db.relationship('Article', backref='u')
    __tablename__ = 'user'  #定义表名,可不写,默认为模型名的小写user

    def save_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Atc_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tname = db.Column(db.String(100))
    keyword = db.Column(db.String(100))
    desc = db.Column(db.String(255))
    atcs = db.relationship('Article', backref='tp')
    __tablename__ = 'atc_type'

    def save_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(150))
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    type = db.Column(db.Integer, db.ForeignKey('atc_type.id'), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __tablename__ = 'article'

    def save_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



