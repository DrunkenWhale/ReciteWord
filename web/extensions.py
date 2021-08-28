from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask import jsonify, request
from flask_mail import Mail
import jwt
import sqlite3

db = SQLAlchemy()
mail = Mail()
conn = sqlite3.connect("../data.db")


def make_json_response(
        status=200,
        message=None,
        data=None
):
    response = jsonify({
        "status": status,
        "message": message,
        "data": data,
    })
    response.headers.add('Access-Control-Allow-Origin', "*")
    response.headers.add('Access-Control-Allow-Methods', "GET, POST, OPTIONS")
    response.headers.add('Access-Control-Allow-Headers', "*")
    return response


def login_check(func):  # token放在请求头中
    def wrapper(*args, **kwargs):
        token = (request.headers.get('Authorization', "Bearer heap")).split("Bearer ")[1]
        try:
            login_msg = jwt.decode(token, key="SegmentTree", algorithms="HS256")
            login_status = bool(login_msg.get('login_status', None))  # 传入bool值
            login_user_mailbox = str(login_msg.get('login_user_mailbox'))  # 登录用户邮箱账号
            issue = bool(str(login_msg.get("iss", "Pigeon")) == "Pigeon377")
        except:
            return make_json_response(status=0, message="NoLogin", data={})
        if login_status is True and login_user_mailbox is not None and issue:
            return func(login_user_mailbox, *args, **kwargs)  # 返回函数返回的值
        else:
            return make_json_response(status=0, message="NoLogin", data={})

    wrapper.__name__ = func.__name__  # 装饰器联用会导致名称冲突 函数名都变为wrapper 会报overwrite的错误 需要手动修改函数名
    return wrapper


def token_return(mailbox):
    payload = {
        "exp": datetime.utcnow() + timedelta(days=17),
        "iss": "Pigeon377",
        "login_user_mailbox": mailbox,
        "login_status": True,  # jwt的那几个标准键值对还要再看看
    }
    msg = jwt.encode(payload=payload, key="SegmentTree", algorithm="HS256")
    return msg


def data_cleaning(dic: dict):
    dic.pop("bookId")
    temp = dic["content"]["word"]["content"]  # 引用
    try:
        temp.pop("realExamSentence")
    except:
        pass
    try:
        temp.pop("star")
    except:
        pass
    try:
        temp.pop("ukspeech")
        temp.pop("ukphone")
    except:
        pass
    try:
        temp.pop("usspeech")
        temp.pop("usphone")
    except:
        pass
    try:
        temp.pop("syno")
    except:
        pass
    try:
        temp.pop("speech")
    except:
        pass
    try:
        temp["remMethod"]["reVal"] = temp["remMethod"]["val"]
        temp["remMethod"].pop("val")
    except:
        pass
    temp = dic["content"]["word"]["content"]
    word_id = dic["content"]["word"]["wordId"]
    dic.pop("content")
    dic["content"] = temp
    dic["wordId"] = word_id
    return dic
