from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from web.extensions import db, make_json_response, token_return
from web.model import User

auth_login_bp = Blueprint('login', __name__, url_prefix='/auth')


@auth_login_bp.post('/')
def login():
    mailbox  = request.form.get("mailbox")
    password = request.form.get("password")
    if mailbox is None or password is None:
        return make_json_response(status=0, message='InvalidArgument', data={})
    else:
        user = User(mailbox=mailbox, password=password)
        if user.check_user_identify():
            token = token_return(user.mailbox)
            response = jsonify({
                'status': 1,
                'message': "Succeed",
                'data': {},
                "token": str(token)[2:-1],
            })
            return response
        else:
            return make_json_response(status=0, message='PasswordWrong', data={})

