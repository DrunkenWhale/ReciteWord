"""
    获取用户最近添加一本单词书
"""

import os
import json
from flask import Blueprint, request
from web.extensions import login_check, make_json_response,data_cleaning
from web.model import User
from web.book.mapping import rank_mapping, name_mapping

book_recent_bp = Blueprint("recent", __name__, url_prefix="/book")


@book_recent_bp.get("/recent")
@login_check
def get_recent_book(mailbox):
    return make_json_response(
        status=1,
        message="Success",
        data=name_mapping[User.query.get(mailbox).recent_book]
    )