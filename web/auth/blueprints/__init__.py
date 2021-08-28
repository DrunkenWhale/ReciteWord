from web.auth.blueprints.register import auth_register_bp
from web.auth.blueprints.login import auth_login_bp
from web.auth.blueprints.information import auth_information_bp
from web.auth.blueprints.update import auth_update_bp


def auth_register_blueprints(app):
    app.register_blueprint(auth_register_bp)
    app.register_blueprint(auth_login_bp)
    app.register_blueprint(auth_information_bp)
    app.register_blueprint(auth_update_bp)
