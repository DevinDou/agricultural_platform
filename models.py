from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserModel(db.Model, UserMixin):
    __tablename__ = "user"  # テーブル名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)  # ユーザー名
    password = db.Column(db.String(255), nullable=False)  # パスワード（長さを255に調整）
    email = db.Column(db.String(100), nullable=False, unique=True)  # 電子メール
    address = db.Column(db.String(255)) #住所
    join_time = db.Column(db.DateTime, default=datetime.now)  # 登録時間
    avatar_url = db.Column(db.String(255))  # 新增字段，存储头像 URL

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'  # テーブル名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)  # 電子メール
    captcha = db.Column(db.String(100), nullable=False)  # キャプチャ
    used = db.Column(db.Boolean, default=False)  # 使用済みかどうか
    join_time = db.Column(db.DateTime, default=datetime.now)  # 登録時間

class QuestionModel(db.Model):
    __tablename__ = 'question'  # テーブル名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)  # タイトル
    content = db.Column(db.Text, nullable=False)  # 内容
    create_time = db.Column(db.DateTime, default=datetime.now)  # 作成時間

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作成者ID
    author = db.relationship(UserModel, backref='questions')  # 作成者との関係
    selected_months = db.Column(db.String(255))  # 実際に関わる月
    selected_crops = db.Column(db.String(255))  # 農産物の種類

class AnswerModel(db.Model):
    __tablename__ = 'answer'  # テーブル名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)  # 内容
    create_time = db.Column(db.DateTime, default=datetime.now)  # 作成時間

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 作成者ID
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))  # 質問ID

    author = db.relationship(UserModel, backref='answers')  # 作成者との関係
    question = db.relationship(QuestionModel, backref=db.backref('answers', order_by=create_time.desc()))  # 質問との関係