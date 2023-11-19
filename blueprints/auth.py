from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import check_password_hash, generate_password_hash
from models import UserModel
from exts import db
from flask_login import login_user

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = UserModel.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session['user_id'] = user.id
            g.user = user
            flash("ログイン成功")
            return redirect(url_for("qa.index"))
        else:
            flash("ユーザー名またはパスワードが正しくありません")

    return render_template("login.html")



@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        address = request.form.get("address")

        # 检查用户是否已经存在
        user = UserModel.query.filter_by(username=username).first()
        if user:
            flash("ユーザー名はすでに登録しましたので、他のユーザー名を利用してください。")
            return redirect(url_for("auth.register"))

        # 检查电子邮箱是否已被注册
        user = UserModel.query.filter_by(email=email).first()
        if user:
            flash("メールアドレスを登録しましたので、他のメールアドレスを利用してください。")
            return redirect(url_for("auth.register"))

        # ユーザーの作成
        new_user = UserModel(
            username=username,
            password=generate_password_hash(password),
            email=email,
            address = address
        )

        # データベースに入れる。
        db.session.add(new_user)
        db.session.commit()

        flash("登録成功！")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('ログアウトしました。')
    return redirect(url_for('auth.login'))