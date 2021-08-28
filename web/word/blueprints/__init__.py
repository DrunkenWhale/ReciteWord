from web.word.blueprints.record import word_update_bp


def word_register_blueprints(app):
    app.register_blueprint(word_update_bp)
