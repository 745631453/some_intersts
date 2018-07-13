from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect

db = SQLAlchemy()


def creat_a(app):
    db.init_app(app=app)


def creat_data(DATABASE):
    user = DATABASE.get('user')
    password = DATABASE.get('password')
    host = DATABASE.get('host')
    port = DATABASE.get('port')
    dbd = DATABASE.get('db')
    driver = DATABASE.get('driver')
    name = DATABASE.get('name')

    return '{}+{}://{}:{}@{}:{}/{}'.format(dbd, driver,
                                           user, password,
                                           host, port, name)


import functools


def is_login(view_fun):
    @functools.wraps(view_fun)
    def decorator():
        try:
            # 验证用户是否登录
            if 'user_id' in session:
                return view_fun()
            else:
                return redirect('/user/login/')
        except:
            return redirect('/user/login/')

    return decorator
