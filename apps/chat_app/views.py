# encoding:utf-8
# __author__ = 'wukeke'
# __time__ = 2019/1/26 10:46
import shortuuid
from flask import Blueprint, render_template, request, redirect, url_for, session
import config
from exct import db
from utils.image import CreatImage
from .functions import get_all_messages
from flask_socketio import emit
from .form import Login_Register_Form
from utils import restful, upload_message
from .models import UserModel
from .decorators import login_required

bp = Blueprint('chat', __name__)

logined_userid = []
user_dict = {}


@bp.route('/')
@login_required
def index():
    user_id = session.get(config.FRONT_USER_ID)
    user_se = UserModel.query.get(user_id)
    if user_id not in logined_userid:
        # user_dict[user_id] = user_id
        logined_userid.append(user_id)

    logined_users = (UserModel.query.get(user_id) for user_id in logined_userid)
    messsages = get_all_messages()

    context = {
        'logined_users': logined_users,
        'messsages': messsages,
        'username': user_se.username
    }
    return render_template('index.html', **context)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('mylogin.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_pwd(password):
            session[config.FRONT_USER_ID] = user.id
            return restful.success(data={'username': user.username, 'imgname': user.imgname})
        else:
            return restful.params_error(message='账户或密码错误，请重试~')


@bp.route('/logout/', methods=['POST'])
def logout():
    user_id = request.form.get('user_id')
    user_id_session = session.get(config.FRONT_USER_ID)
    if user_id == user_id_session:
        del session[config.FRONT_USER_ID]
        logined_userid.remove(user_id)
        return restful.success()
    else:
        return redirect(url_for('chat.login'))


@bp.route('/regist/', methods=['POST'])
def regiser():
    form = Login_Register_Form(request.form)
    if form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return restful.params_error(message='该用户已经注册，换一个试试吧~')
        if not password or len(password) < 6:
            return restful.params_error(message='密码至少6个字符')

        if len(username) == 0:
            username = '无'
        # todo 生成头像
        msg = username[0:1]
        imag_name = shortuuid.uuid() + '.png'

        image = CreatImage()
        image.image(msg, imag_name)

        new_user = UserModel(username=username, password=password, imgname=imag_name)
        db.session.add(new_user)
        db.session.commit()

        return restful.success()
    else:
        if form.errors.get('username'):
            return restful.params_error(message=form.errors.get('username')[0])
        if form.errors.get('password'):
            return restful.params_error(message=form.errors.get('password')[0])
