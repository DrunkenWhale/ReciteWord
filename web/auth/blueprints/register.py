from flask import Blueprint, request, jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from web.extensions import db, make_json_response, token_return, mail
from web.model import User
from random import randint
from time import time

auth_register_bp = Blueprint('register', __name__, url_prefix='/auth')

identify_code_dic = {}


@auth_register_bp.post('/register')
def register():
    mailbox = request.form.get("mailbox", None)
    user_name = request.form.get("user_name", None)
    password = request.form.get("password", None)
    education = request.form.get("education", 0)
    identify_code = request.form.get("identify_code", 0)

    if int(education) > 3:
        return make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    # 判断验证码是否存在以及是否正确
    if mailbox not in identify_code_dic.keys() or int(identify_code_dic[mailbox]["code"]) != int(identify_code):
        return make_json_response(
            status=0,
            message="WrongIdentifyCode",
            data={}
        )

    # 判断验证码是否在时限内
    if time() - identify_code_dic[mailbox]["time"] >= 5 * 60:
        return make_json_response(
            status=0,
            message="ExceedTimeLimit",
            data={}
        )
    # 将验证码键值对清除
    identify_code_dic.pop(mailbox)

    # 判断参数是否有空缺
    if mailbox is None \
            or user_name is None \
            or password is None:
        return make_json_response(status=0, message="InvalidArgument", data={})
    user = User(mailbox=mailbox, name=user_name, password=password, education=education)
    if not user.check_user_exist():
        user.register_user_identify()
        response = jsonify({
            'status': 1,
            'message': "Succeed",
            'data': {},
        })
        return response
    else:
        return make_json_response(status=0, message='UserExist', data={})


@auth_register_bp.post('/identify')
async def send_mail():
    user_mailbox = request.form.get("mailbox", None)
    if user_mailbox is None:
        return make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    # 判断验证码是否发送过于频繁

    if user_mailbox in identify_code_dic and time() - identify_code_dic[user_mailbox]["time"] <= 60:
        return make_json_response(
            status=0,
            message="FrequentSubmission",
            data={}
        )

    msg = Message("注册验证", sender="reciteword@163.com", recipients=[user_mailbox])
    temp_code: int = randint(100000, 999999)
    msg.body = "您正在注册 ReciteWord App, 您的验证码是" + str(temp_code) + " ,请在五分钟内使用该验证码完成注册(*╹▽╹*)"
    mail.send(msg)
    identify_code_dic[user_mailbox] = {"code": temp_code, "time": time()}
    return make_json_response(
        status=1,
        message="Succeed",
        data={}
    )
