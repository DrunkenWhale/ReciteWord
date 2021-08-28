"""
    用户的学习情况
    :post 提交新的学习记录
    :get
        all 参数为1时
"""

from flask import Blueprint, request
from web.extensions import login_check, make_json_response
from web.model import User, Record, db
from web.book.mapping import name_mapping

word_update_bp = Blueprint("record", __name__, url_prefix="/word")


@word_update_bp.post("/")
@login_check
def update_user_word_record(mailbox):
    book_name = request.form.get("book", None)
    size = request.form.get("size", None)

    if book_name is None or size is None:
        return make_json_response(
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

    book_name = book

    record = Record.query.get(book_name + "$" + mailbox)

    if record is None:
        db.session.add(Record(
            id=book_name + "$" + mailbox,
            user_mailbox=mailbox,
            size=size,
        ))
        db.session.commit()
        return make_json_response(
            status=1,
            message="Succeed",
            data={}
        )

    if record.size > size:  # 总不可能越学越少吧
        return make_json_response(
            status=0,
            message="InvalidArgument",
            data={}
        )

    #
    # if record is not None:
    #     # 该用户之前已经有过这个单词本的记录了
    #     # record.record_list = ",".join(set(record.record_list.split(",") + size.split(","))) 老版本 功能好像不好实现诶
    #     record.size = size
    #     record.submit()
    # else:
    # 该用户第一次出现这个单词本的记录
    # record = Record(id=book_name + "$" + mailbox, user_mailbox=mailbox,
    #                 record_list=",".join(set(size.split(","))))
    record.size = size
    record.submit()

    return make_json_response(
        status=1,
        message="Succeed",
        data={},
    )


@word_update_bp.get("/")
@login_check
def get_user_word_record(mailbox):
    params = request.args.get("all", 0)
    if params == 0:  # 获取特定的单词书学习记录
        book_name = request.args.get("book", None)

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

        book_name = book

        record = Record.query.get(book_name + "$" + mailbox)

        if record is not None:
            # re = record.record_list.split(",")
            return make_json_response(
                status=1,
                message="Succeed",
                data=record.size
            )
        else:  # 没有学习记录
            return make_json_response(
                status=1,
                message="Succeed",
                data=0,
            )
    else:
        re = {}
        all_words_number = 0
        user = User.query.get(mailbox)
        for i in user.learned_records:
            re[name_mapping[i.id.split("$")[0]]] = i.size
            all_words_number += i.size
        # for i in user.learned_records:
        #     temp = {
        #         i.id.split("$")[0]:
        #             [int(id) if id is not None else id for id in i.record_list.split(",")]
        #     }
        #     re.append(temp)
        return make_json_response(
            status=1,
            message="Succeed",
            data={
                "record": re,
                "sum": all_words_number,
            }
        )
