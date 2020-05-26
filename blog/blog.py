from flask import Flask ,render_template, request, redirect, session, Flask, send_from_directory,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy import and_
import pymysql
import os, json
import time
import sys

pymysql.install_as_MySQLdb()

app = Flask(__name__)

# 设置连接数据
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1:3306/blog'

# 设置每次请求结束后会自动提交数据库中的改动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 设置成 True，SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# 实例化SQLAlchemy对象
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "123456789"


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)


class Article(db.Model):

    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
    brief = db.Column(db.Text, nullable=True)


@app.route('/')
def login():

    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login_check', methods=['POST'])
def login_check():
    email = request.form['email']
    password = request.form['password']
    print(password)
    print(email)
    # user = db.session.query(User).filter(and_(User.email == email, User.password == password)).first()
    # print(user)
    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if user is not None:
        print("ok!!!")
        session['name'] = user.name
        return redirect('/index')
    return render_template("login.html")


@app.route('/register_check', methods=['POST'])
def register_check():
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("login.html")


@app.route('/index')
def index():
    name = session.get('name')
    res = {}
    print(name)
    if name is None:
        return render_template("login.html")
    res['name'] = name
    articles = Article.query.all()
    tmp = []
    for article in articles:
        temp_data = {}
        temp_data['title'] = article.title
        temp_data['id'] = article.id
        temp_data['brief'] = article.brief
        tmp.append(temp_data)

    res['data'] = tmp
    return render_template("index.html", res = res)


@app.route('/detail', methods=['GET'])
def detail():
    name = session.get('name')
    res = {}
    res['name'] = name
    if name is None:
        return render_template("login.html")
    id = request.args.get('id')
    article = Article.query.get(int(id))
    res['title'] = article.title
    res['content'] = article.content
    res['brief'] = article.brief

    return render_template('info.html', res=res)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
