from flask import Flask

from sweater.models import db, migrate
from sweater.routes import app_route


def create_app():
    app = Flask(__name__)
    app.secret_key = "asus912"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    app.register_blueprint(app_route)

    return app
