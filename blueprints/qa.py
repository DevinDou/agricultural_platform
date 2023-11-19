from flask import Blueprint, render_template, g, redirect, url_for, request
from models import QuestionModel, AnswerModel
from exts import db
from flask_login import current_user, login_required

bp = Blueprint("qa", __name__, url_prefix="/")

@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)

@bp.route("/qa/public_qa", methods=["GET", "POST"])
def public_qa():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            # 如果用户未登录，重定向到登录页面
            return redirect(url_for('auth.login'))

        title = request.form.get('title')
        content = request.form.get('body')
        selected_months = request.form.getlist('months')  #月
        selected_crops = request.form.getlist('crops')  #農産物

        selected_months_str = ','.join(selected_months)
        selected_crops_str = ','.join(selected_crops)

        # 确保用户已登录
        user_id = current_user.id

        new_question = QuestionModel(
            title=title,
            content=content,
            author_id=user_id,
            selected_months=selected_months_str,
            selected_crops=selected_crops_str
        )
        db.session.add(new_question)
        db.session.commit()

        return redirect(url_for('qa.qa_detail', qa_id=new_question.id))

    return render_template('public_qa.html')

@bp.route("/qa/detail/<int:qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get_or_404(qa_id)
    return render_template("detail.html", question=question)

@bp.route("/answer/public", methods=["POST"])
@login_required
def answer_public():
    print("Current user:", current_user)
    print("Authenticated:", current_user.is_authenticated)
    content = request.form.get('content')
    question_id = request.form.get('question_id')

    # 使用 Flask-Login 的 current_user 获取当前登录用户的ID
    user_id = current_user.id

    new_answer = AnswerModel(content=content, question_id=question_id, author_id=user_id)
    db.session.add(new_answer)
    db.session.commit()

    return redirect(url_for('qa.qa_detail', qa_id=question_id))

@bp.route("/search")
def search():
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html", questions=questions)