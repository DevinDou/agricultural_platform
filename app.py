from flask import Flask, render_template, request, redirect, url_for, g, session
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import text
#from flask_wtf import CSRFProtect
import config
from exts import db
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
from flask_login import LoginManager

import speech_recognition as sr

app = Flask(__name__)

app.config.from_object(config)
app.config['SECRET_KEY'] = 'your_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        g.user = db.session.get(UserModel, user_id)
    else:
        g.user = None

@login_manager.user_loader
def load_user(user_id):
    # データベースからユーザーを取得
    return UserModel.query.get(int(user_id))


'''
#テストだけ
with app.app_context():
    with db.engine.connect() as conn:
        rs = conn.execute(text("select 1"))
        print(rs.fetchone())
'''
'''
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #  varchar
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
'''

#with app.app_context():
#   db.create_all()

'''
csrf = CSRFProtect(app)

app.config.from_object(config)

db.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)
'''


#recognizerの初期化
'''r = sr.Recognizer()

with sr.Microphone() as source:
    #マイクから音声データを読み込み
    audio_data = r.record(source, duration=5)
    print("Recognizing...")
    text = r.recogize_google(audio_data, language="ja")
    print(text)
'''

'''
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<コメント {self.id} 作者 {self.author}>'

@app.route('/post_comment/<int:article_id>', methods=['POST'])
def post_comment(article_id):
    author = request.form.get('author')
    content = request.form.get('content')
    comment = Comment(author=author, content=content, article_id=article_id)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('articles'))
'''

'''
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='article', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article> {self.id} {self.title}'

@app.route('/articles')
def articles():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('articles.html', articles=articles)

@app.route('/submit-article', methods=['GET', 'POST'])
def submit_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        article = Article(title=title, content=content)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('articles'))
    return render_template('submit_article.html')

'''

if __name__ == '__main__':
   # with app.app_context():
       # db.create_all()
    app.run(debug=True, port=5004)