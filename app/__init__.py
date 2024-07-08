# app/__init__.py

from flask import Flask
from .config import config
from .routes import main
from .db import close_db

def create_app(config_name='alphatesting'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize any extensions (e.g., SQLAlchemy)

    # Import and register blueprints or routes here
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.teardown_appcontext(close_db)

    return app
