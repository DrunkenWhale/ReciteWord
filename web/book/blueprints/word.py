"""
    获取书名列表
    只能获取难度等级当前用户等级相同的
"""

import os
import json
from flask import Blueprint, request
from web.extensions import login_check, make_json_response,data_cleaning
from web.model import User
from web.book.mapping import rank_mapping, name_mapping

book_word_bp = Blueprint("word", __name__, url_prefix="/book")


@book_word_bp.get("/word")
@login_check
def get_book_words(mailbox):
    book_name = request.args.get("book", None)

    if book_name is None:
        return make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    table_name = None

    for table, book in name_mapping.items():
        if book == book_name:
            table_name = table
            break

    if table_name is None:
        return make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    # 数据库实在是没办法搞定编码
    # 所以直接从文件中查询
    #

    with open(file=os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+os.sep+"resource"+os.sep+table_name+".json", mode="r", encoding="utf-8") as file:
        re = [data_cleaning(json.loads(i)) for i in file.readlines()]

    return make_json_response(
        status=1,
        message="Succeed",
        data=re
    )
