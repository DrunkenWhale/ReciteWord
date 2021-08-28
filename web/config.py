import os


class Config(object):

    FLASK_APP = "web"

    SECRET_KEY = "SegmentTree"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(
    #     os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data.db'))

    MAIL_USE_SSL = True
    MAIL_USE_TLS = False  # 禁用tls 顺带一提 25端口日常被ban
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
