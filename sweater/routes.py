from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from sweater.models import Notes, User, db
from werkzeug.security import check_password_hash, generate_password_hash

app_route = Blueprint("route", __name__)


@app_route.route("/main")
@app_route.route("/")
def main():
    return render_template("index.html")


@app_route.route("/posts")
@login_required
def posts():
    uid = current_user.get_id()
    note = Notes.query.order_by(Notes.date.desc()).filter(Notes.uid == uid).all()
    return render_template("posts.html", note=note)


@app_route.route("/posts/<int:id>")
@login_required
def post_detail(id):
    note = Notes.query.get(id)
    return render_template("post_detail.html", note=note)


@app_route.route("/posts/<int:id>/delete")
@login_required
def post_delete(id):
    note = Notes.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect("/posts")
    except Exception:
        return "При удалении заметки произошла ошибка :("


@app_route.route("/posts/<int:id>/update", methods=["POST", "GET"])
@login_required
def post_update(id):
    note = Notes.query.get(id)
    if request.method == "POST":
        note.title = request.form["title"]
        note.text_uno = request.form["text_uno"]
        note.text_dos = request.form["text_dos"]
        try:
            db.session.commit()
            return redirect("/posts")
        except Exception:
            return "При редактировании заметки произошла ошибка :("
    else:
        return render_template("post_update.html", note=note)


@app_route.route("/create", methods=["POST", "GET"])
@login_required
def create_text():
    if request.method == "POST":
        title = request.form["title"]
        text_uno = request.form["text_uno"]
        text_dos = request.form["text_dos"]
        uid = current_user.get_id()
        note = Notes(title=title, text_uno=text_uno, text_dos=text_dos, uid=uid)
        try:
            db.session.add(note)
            db.session.commit()
            return redirect("/posts")
        except Exception:
            return "При добавлении заметки произошла ошибка :("
    else:
        return render_template("crtext.html")


@app_route.route("/faq")
def faq():
    return render_template("faq.html")


@app_route.route("/about")
def about():
    return render_template("about.html")


@app_route.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("route.main"))
    login = request.form.get("login")
    password = request.form.get("password")
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next = request.args.get("next")
            return redirect(next)
        else:
            flash("Ошибка авторизации")
    else:
        flash("Заполните поля логина и пароля")
    return render_template("login.html")


@app_route.route("/register", methods=["POST", "GET"])
def register():
    login = request.form.get("login")
    password = request.form.get("password")
    password2 = request.form.get("password2")
    if request.method == "POST":
        if not (login or password or password2):
            flash("Для завершения заполните все поля")
        elif password != password2:
            flash("Ваши пароли не соответствуют")
        else:
            hash = generate_password_hash(password)
            new_user = User(login=login, password=hash)
            db.session.add(new_user)
            db.session.commit()
            return render_template("login.html")
    return render_template("register.html")


@app_route.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("route.main"))


# @app_route.route("/admin")
# @login_required
# def user_index():
#     return f"""<p><a href="{url_for("route.logout")}">Выйти из аккаунта<a>
#                 <p>user info: {current_user.get_id()}"""


@app_route.after_request
def redirect_to_signin(respone):
    if respone.status_code == 401:
        return redirect(url_for("login") + "?next" + request.url)
    return respone
