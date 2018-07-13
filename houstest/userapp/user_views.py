import re

import os
from flask import Blueprint, render_template, request, jsonify, session, redirect

from utlis import status_code
from utlis.settings import UPLOAD_DIR
from utlis.status_code import USER_REGISTER_PARAMS_ERROR, USER_REGISTER_MOBILE_ERROR, USER_REGISTER_MOBILE_IS_EXSITS
from utlis.funcktions import is_login
from userapp.models import User, db

user = Blueprint('user', __name__)


@user.route('/')
def hello():
    db.create_all()

    return '成功'


# 注册页面
@user.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        re_dict = request.form
        moble = re_dict.get('mobile')
        password = re_dict.get('password')
        password2 = re_dict.get('password2')
        # all(列表)如果有空字符串返回False
        if not all([moble, password, password2]):
            return jsonify(USER_REGISTER_PARAMS_ERROR)

        if not re.match(r'^1[34578]\d{9}$', moble):
            return jsonify(USER_REGISTER_MOBILE_ERROR)

        if User.query.filter(User.phone == moble).count():
            return jsonify(USER_REGISTER_MOBILE_IS_EXSITS)
        if password != password2:
            return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

        users = User()
        users.phone = moble
        users.name = moble
        users.password = password
        try:
            users.add_update()
            return jsonify(status_code.SUCCESS)
        except:
            return jsonify(status_code.DATABASE_ERROR)


# 登录页面
@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        user_dict = request.form
        mobile = user_dict.get('mobile')
        password = user_dict.get('password')
        # 验证是否为空
        if not all([mobile, password]):
            return jsonify(status_code.PARAMS_ERROR)
        if not re.match(r'^1[34578]\d{9}$', mobile):
            return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
        my_user = User.query.filter(User.phone == mobile).first()

        if my_user:
            # 校验密码
            if my_user.check_pwd(password):
                # 存入redis
                session['user_id'] = my_user.id
                return jsonify(status_code.SUCCESS)
            else:
                return jsonify(status_code.USER_LOGIN_PASSWORD_IS_ERROR)
        else:
            return jsonify(status_code.USER_LOGIN_IS_NOT_EXSIST)


# 我的页面
@user.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 我的页面展示头像
@user.route('/user/', methods=['GET'])
@is_login
def get_user():
    user_id = session['user_id']
    users = User.query.get(user_id)
    return jsonify(user=users.to_basic_dict(), code='200')


# 修改信息
@user.route('/profile/', methods=['GET'])
@is_login
def user_profile():
    return render_template('profile.html')


# 修改头像和用户名
@user.route('/mprofile/', methods=['PUT'])
@is_login
def user_mprofile():
    user_dict = request.form
    file_dict = request.files
    if 'avatar' in file_dict:
        f1 = file_dict['avatar']
        # 判断类型
        if not re.match(r'^image/.*$', f1.mimetype):
            return jsonify(status_code.USER_PROFILE_IMG_ERRO)

        url = os.path.join(UPLOAD_DIR, f1.filename)
        f1.save(url)
        uu = User.query.filter(User.id == session['user_id']).first()

        image_url = os.path.join('/static/upload/', f1.filename)
        uu.avatar = image_url
        try:
            uu.add_update()
            return jsonify(code=status_code.OK, url=image_url)
        except:
            return jsonify(status_code.DATABASE_ERROR)

    elif 'name' in user_dict:
        my_user = user_dict.get('name')
        if User.query.filter(User.name == my_user).count():
            return jsonify(status_code.USER_UPDATE_USERNAME_IS_EXSITS)
        else:
            uu = User.query.get(session['user_id'])
            uu.name = my_user
            try:
                uu.add_update()
                return jsonify(status_code.SUCCESS)
            except Exception as e:
                return jsonify(status_code.DATABASE_ERROR)
    else:
        return jsonify(status_code.PARAMS_ERROR)


# 实名认证
@user.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


@user.route('/auths/', methods=['GET'])
@is_login
def get_user_auth():
    userq = User.query.get(session['user_id'])
    if all([userq.id_card, userq.id_name]):
        return jsonify(code=status_code.OK,
                       id_name=userq.id_name,
                       id_card=userq.id_card)


# 实际工作中只这样写页面跳转传递给前端
@user.route('/auths/', methods=['PUT'])
@is_login
def user_auth():
    user_div = request.form
    id_name = user_div.get('id_name')
    id_card = user_div.get('id_card')
    if not all([id_card, id_name]):
        return jsonify(status_code.PARAMS_ERROR)
    if not re.match(r'^[1-9]\d{17}$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARE_IS_ERROR)
    try:
        userq = User.query.get(session['user_id'])
        userq.id_card = id_card
        userq.id_name = id_name
        userq.add_update()
        return jsonify(status_code.SUCCESS)
    except:
        return jsonify(status_code.DATABASE_ERROR)


# 退出
@user.route('/logout/')
def logout():
    session.clear()
    return jsonify(status_code.SUCCESS)
