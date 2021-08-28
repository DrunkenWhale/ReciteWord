'''

获取用户信息

'''

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from web.extensions import db, make_json_response, token_return, login_check
from web.model import User

auth_information_bp = Blueprint('information', __name__, url_prefix='/auth')


@auth_information_bp.get('/')
@login_check
def get_user_information(id):
    user = User.query.get(id)
    if user is not None:
        re = {
            "id": user.mailbox,
            "name": user.name,
            "education": user.education,
        }
        return make_json_response(
            status=1,
            message="Succeed",
            data=re
        )
    else:
        return make_json_response(
            status=0,
            message="NoLogin",
            data={}
        )
