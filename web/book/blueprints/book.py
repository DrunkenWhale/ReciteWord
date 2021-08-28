"""
 用户
 :添加书籍
 :获取已添加的书籍
"""

import os
import json
from flask import Blueprint, request
from web.extensions import login_check, make_json_response, data_cleaning, db
from web.model import User, Book
from web.book.mapping import name_mapping

book_book_bp = Blueprint("book", __name__, url_prefix="/book")

"""
    get方法获取用户已添加的单词本
    post方法给用户添加单词本
"""


@book_book_bp.get("/")
@login_check
def get_book_list(mailbox):
    user = User.query.get(mailbox)
    book_list = [book.name for book in user.learned_books]
    return make_json_response(
        status=0,
        message="Succeed",
        data=book_list
    )


@book_book_bp.post("/")
@login_check
def post_book_list(mailbox):
    book_name = request.form.get("book", None)
    if book_name is None:
        make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    book = None

    for book_english, book_chinese in name_mapping.items():
        if book_chinese == book_name:
            book = book_english
            break

    if book is None:
        return make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    if Book.query.filter_by(name=book, user_mailbox=mailbox).first() is not None:
        user = User.query.get(mailbox)
        user.recent_book = book
        db.session.add(user)
        db.session.commit()
        return make_json_response(
            status=0,
            message="BookExist",
            data={}
        )

    Book(book, mailbox).submit()
    user = User.query.get(mailbox)
    user.recent_book = book
    db.session.add(user)
    db.session.commit()

    return make_json_response(
        status=1,
        message="Succeed",
        data={},
    )
