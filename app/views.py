from flask import render_template, abort, request, flash, redirect, session, url_for
from .database import db_session

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/article/<int:article_id>')
def show_article(article_id):
    from jinja2 import Markup
    from .models import Article, User
    from .forms import PostSubmitForm
    article = Article.query.filter(Article.id == article_id).first()
    form = PostSubmitForm()
    form.article_id = article_id
    if article:
        comments = []
        for comment in article.comments:
            username = User.query.filter(User.id == comment.user_id).first().username
            content = comment.content
            datetime = comment.datetime
            comments.append({'username':username, 'content':content, 'datetime':datetime})
        return render_template("article.html", articleName=article.name,
                               content=Markup(article.content),
                               form=form,
                               comments=comments,
                               comments_number = len(comments))
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


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    from .forms import AvatarSettingsForm, PasswordOrEmailForm, ChangeUserNameForm
    avatar_form = AvatarSettingsForm()
    email_password_form = PasswordOrEmailForm()
    username_form = ChangeUserNameForm()
    if not session.get("username"):
        return abort(404)
    username_form.new_username.data = session["username"]
    return render_template("settings.html", avatarForm=avatar_form, emailOrPasswordForm=email_password_form, usernameform = username_form)

def crop_image(img):
    import math
    from PIL import Image
    width = img.width
    height = img.height
    if width != height != 256:
        aspect_ratio = height / width
        vertical_crop = 0
        horizontal_crop = 0
        if height > width:
            aspect_ratio = height / width
            img = img.resize((256, math.trunc(256 * aspect_ratio)), Image.BILINEAR)
            vertical_crop = (img.height - 256) / 2
        else:
            img = img.resize((math.trunc(256 / aspect_ratio), 256), Image.BILINEAR)
            horizontal_crop = (img.width - 256) / 2
        return img.crop((horizontal_crop, vertical_crop, 256 + horizontal_crop, 256 + vertical_crop))
    return img


@app.route('/settings/avatar', methods=['GET', 'POST'])
def change_avatar():
    from pathlib import Path
    from .forms import AvatarSettingsForm
    from PIL import Image
    if not session.get("username"):
        return abort(404)
    form = AvatarSettingsForm(request.form)
    if request.method == 'POST' and form.validate():
        image_data = request.files[form.newAvatar.name]
        img = Image.open(image_data)
        if img.width > 2048 or img.height > 2048:
            flash("The image size is too big! Maximum: 1024x1024")
        cropped_image = crop_image(img)
        img.save(Path(__file__).parent.joinpath('static').joinpath(session['username']+'.jpg'))
        return redirect('/settings')



@app.route('/comment', methods=['GET', 'POST'])
def submit_post():
    from .models import User, Comment, Article
    from .forms import PostSubmitForm
    import datetime
    from .database import db_session
    form = PostSubmitForm(request.form)
    if request.method == 'POST' and form.validate():
        if not session.get("username"):
            print('no user session')
            return redirect("/", code=404)
        user = User.query.filter(User.username == session["username"]).first()
        article_id = form.article_id.data
        article = Article.query.filter(Article.id == article_id).first()
        if not user or not article:
            print("user is", user)
            print("article_id is", article_id)
            return redirect("/", code=404)
        comment = Comment(datetime.datetime.now(), form.content.data, user.id)
        article.comments.append(comment)
        db_session.commit()
        return redirect("/article/{0}#comments".format(article_id))
    return redirect("/", code=404)
