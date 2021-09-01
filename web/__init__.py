from flask import Flask, request
from web.config import Config
from web.extensions import db, mail, redis, logging_format
from flask_cors import CORS
from web.auth.blueprints import auth_register_blueprints
from web.book.blueprints import book_register_blueprints
from web.word.blueprints import word_register_blueprints
import logging

index: int = 1


def create_app(name=__name__):
    app = Flask(name)
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    CORS(app, origins='*')
    return app


def register_blueprints(app: Flask):
    auth_register_blueprints(app)
    book_register_blueprints(app)
    word_register_blueprints(app)


def register_extensions(app: Flask):
    mail.init_app(app)
    redis.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # 定义一个钩子 储存日志
    # 搬砖呐 明天再说啦
    pipe = redis.pipeline()

    @app.before_request
    def logger():
        global index
        pipe.set(index, logging_format(
            request.full_path,
            request.remote_addr,
            request.method,
            request.form))
        index += 1
        pipe.execute()
