"""
更新用户信息
"""

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from web.extensions import db, make_json_response, token_return, login_check
from web.model import User

auth_update_bp = Blueprint('update', __name__, url_prefix='/auth')


@auth_update_bp.put('/')
@login_check
def update_user_information(mailbox):
    password     = request.form.get("password", "&*")  # 不为None
    new_password = request.form.get("new_password")
    name         = request.form.get("user_name")
    education    = request.form.get("education")
    user = User(mailbox=mailbox, password=password)
    if user.check_user_identify():
        user = User.query.get(mailbox)
        if new_password is not None:
            user.password = generate_password_hash(new_password)
        if name is not None:
            user.name = name
        if education is not None:
            user.education = education
        db.session.add(user)
        db.session.commit()
        return make_json_response(
            status=1,
            message="Succeed",
            data={}
        )
    else:
        return make_json_response(
            status=0,
            message="WrongPassword",
            data={}
        )
