"""
    获取书名列表
    只能获取难度等级当前用户等级相同的
"""

import os
from flask import Blueprint
from web.extensions import login_check, make_json_response
from web.model import User
from web.book.mapping import rank_mapping, name_mapping

book_dir_bp = Blueprint("dir", __name__, url_prefix="/book")


@book_dir_bp.get("/dir")
@login_check
def get_book_dir(mailbox):
    user = User.query.get(mailbox)
    user_rank = user.education
    re = [name_mapping[i] for i in rank_mapping[user_rank]]
    return make_json_response(
        status=1,
        message="Succeed",
        data=re
    )
