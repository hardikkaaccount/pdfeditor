
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

    return app