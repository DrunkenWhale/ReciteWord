from web.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    mailbox = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(80), index=True)
    password = db.Column(db.String(128))
    education = db.Column(db.Integer, index=True)  # 学习等级
    recent_book = db.Column(db.String(64))  # 最新添加的书 话说这个功能真觉的木大
    # 外键
    learned_records = db.relationship("Record")
    learned_books   = db.relationship("Book")

    def __init__(self, mailbox, password, education=0, name=None):
        self.mailbox = mailbox
        self.name = name
        self.password = password
        self.education = education

    '''
    这里的education代表教育经历这样的 
    小学 0
    初中 1
    高中 2
    大学 3
    '''

    '''
    用于判断用户是否存在
    存在返回 True
    不存在返回False
    '''

    def check_user_exist(self) -> bool:
        if User.query.get(self.mailbox) is None:
            return False
        else:
            return True

    '''
     用于检查用户用户名与密码是否匹配
    '''

    def check_user_identify(self) -> bool:
        user = User.query.get(self.mailbox)
        if user is None:
            return False
        real_password = user.password

        if check_password_hash(real_password, self.password):
            # 如果mailbox不存在 也会报错
            return True
        else:
            return False

    '''
        将当前对象写入数据库中
        若mailbox冲突  返回False
        若成功写入 返回True
    '''

    def register_user_identify(self) -> bool:
        if User.query.get(self.mailbox) is None:
            # 未注册
            self.password = generate_password_hash(self.password)
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    # def change_user_password(self) -> bool:
    #


class Record(db.Model):  # 书名$用户邮箱为主键
    id = db.Column(db.String(70), primary_key=True)
    size = db.Column(db.Integer)  # 前辈那里学单词一定要按顺序来着哒 那就用size来记录学到哪里啦
    user_mailbox = db.Column(db.ForeignKey("user.mailbox"), index=True, nullable=False)

    def __init__(self, id, user_mailbox, size):
        self.id = id
        self.user_mailbox = user_mailbox
        self.size = size

    def submit(self):
        db.session.add(self)
        db.session.commit()  # 这玩意好像线程安全啊


class Book(db.Model):  # 记录每个用户拥有哪些单词书

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 这里直接放空
    name = db.Column(db.String(30), nullable=True)

    user_mailbox = db.Column(db.ForeignKey("user.mailbox"), index=True, nullable=False)

    def __init__(self, name, user_mailbox):
        self.name = name
        self.user_mailbox = user_mailbox

    def submit(self):
        db.session.add(self)
        db.session.commit()

# class Word(db.Model):   # 这个表中的数据通过SQL文件导入 表名为单词本名 不和任何表单相连 独立的 作为资源存在 寄了 顶不住
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
#     chinese = db.Column(db.String(30), nullable=false, index=True)
#     english = db.Column(db.String(30), nullable=false, index=True)
#     phonetic = db.Column(db.String(50))
#     phrase = db.Column(db.String(300))
#     conjugate = db.Column(db.String(300))
#     remember_method = db.Column(db.String(50))
#     sentence = db.Column(db.String(300))
#
#     def __init__(self, id,
#                  chinese,
#                  english,
#                  phonetic,
#                  phrase,
#                  conjugate,
#                  remember_method,
#                  sentence,
#                  ):
#         self.id = id
#         self.chinese = chinese
#         self.english = english
#         self.phonetic = phonetic
#         self.phrase = phrase
#         self.conjugate = conjugate
#         self.remember_method = remember_method
#         self.sentence = sentence
