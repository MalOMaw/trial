from flask import render_template, abort, request, flash, redirect, session, url_for
from .database import db_session

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/article/<int:article_id>')
def show_article(article_id):
    from jinja2 import Markup
    from .models import Article
    article = Article.query.filter(Article.id == article_id).first()
    if article:
        return render_template("article.html", articleName=article.name,
                               blogName='Dummy Var',
                               content=Markup(article.content))
    else:
        abort(404)


@app.route('/signin', methods=['GET', 'POST'])
def signIn():
    from .models import User
    from .forms import SignInForm
    import hashlib
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.password == hashlib.sha256(form.password.data.encode()).hexdigest():
            session["username"] = form.username.data
            return redirect("/")
    return render_template("signin.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    from .models import User
    from .forms import SignUpForm
    import hashlib
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, hashlib.sha256(form.password.data.encode()).hexdigest())
        db_session.add(user)
        db_session.commit()
        flash("User record has been created!")
        return redirect("/")
    return render_template("signup.html", form=form)


@app.route('/signout', methods=['GET', 'POST'])
def signOut():
    del session["username"]
    return redirect(url_for('index'))

@app.route('/post/submit', methods=['GET', 'POST'])
def submit_post():
    from .models import User, Comment, Article
    from .forms import PostSubmitForm
    import datetime
    from .database import db_session
    form = PostSubmitForm(request.form)
    if request.method == 'POST' and form.validate():
        if not session["username"]:
            return redirect("/", code=404)
        user = User.query.filter(User.username == session["username"]).first()
        article_id = form.article_id.data
        article = Article.query.filter(Article.id == article_id).first()
        if not user or not article:
            return redirect("/", code=404)
        comment = Comment(datetime.datetime.now(), form.content.data, user.id)
        article.comments.append(comment)
        db_session.commit()
        return redirect("/article/{0}".format(article_id))
    return redirect("/", code=404)
