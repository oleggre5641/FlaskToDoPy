from flask import redirect, url_for, request
from flask_login import LoginManager

from sweater import create_app
from sweater.models import User

app = create_app()
manager = LoginManager(app)
manager.login_view = "route.login"
manager.login_message = "Сначала авторизуйтесь, для доступа к остальным страницам"


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
