from web.book.blueprints.dir import book_dir_bp
from web.book.blueprints.word import book_word_bp
from web.book.blueprints.book import book_book_bp
from web.book.blueprints.recent import book_recent_bp


def book_register_blueprints(app):
    app.register_blueprint(book_dir_bp)
    app.register_blueprint(book_word_bp)
    app.register_blueprint(book_book_bp)
    app.register_blueprint(book_recent_bp)
