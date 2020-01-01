from flask import render_template, abort, request, flash, redirect, session, url_for
from .database import db_session

from app import app


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/articles')
def articles():
    return articles_page(1)


@app.route('/articles/<int:page>')
def articles_page(page):
    from jinja2 import Markup
    from .models import Article, User
    from markdown import markdown
    if not page:
        page = 1
    page -= 1
    all_articles = Article.query.all()
    selected_articles = all_articles[page*5:page*5+5]
    if len(selected_articles) == 0:
        return abort(404)
    articles = list()
    for article in selected_articles:
        preview = r"https://cdn.pixabay.com/photo/2015/01/11/07/02/moe-595954_960_720.png"
        content_preview = '\n'.join(article.content.splitlines()[:3])  # First 3 lines of article
        if len(content_preview) > 200:
            content_preview = content_preview[:200]+'...'
        content_preview = markdown(content_preview)
        user = User.query.filter(User.id == article.author_id).first()
        articles.append({'date':article.datetime,'author':user.username,'name':article.name,'preview_image':preview, 'preview_content':Markup(content_preview), 'id':article.id, 'comments_count':len(article.comments)})
    return render_template("articles.html", articles=articles)


@app.route('/article/<int:article_id>')
def view_article(article_id):
    from markdown import markdown
    from jinja2 import Markup
    from .models import Article, User
    from .forms import CommentAddForm
    article = Article.query.filter(Article.id == article_id).first()
    form = CommentAddForm()
    form.article_id = article_id
    if article:
        comments = []
        for comment in article.comments:
            username = User.query.filter(User.id == comment.user_id).first().username
            content = comment.content
            datetime = comment.datetime
            comment_id = comment.id
            comments.append({'username':username, 'content':content, 'datetime':datetime, 'id':comment_id})
        content = markdown(article.content, extensions=['extra', 'nl2br', 'sane_lists'])
        author = dict()
        author['username'] = User.query.filter(User.id == article.author_id).first().username

        return render_template("article.html", articleName=article.name,
                               content=Markup(content),
                               form=form,
                               comments=comments,
                               comments_number=len(comments),
                               author=author,
                               post_date=article.datetime,
                               article_id=article_id)
    else:
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from .models import User
    from .forms import LoginForm
    import hashlib
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.password == hashlib.sha256(form.password.data.encode()).hexdigest():
            session["username"] = form.username.data
            flash("Signed In Successfully!", 'success')
            return redirect("/")
        else:
            flash("Invalid username or password.", 'error')
    return render_template("signin.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    from .models import User
    from .forms import RegisterForm
    import hashlib
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, hashlib.sha256(form.password.data.encode()).hexdigest())
        db_session.add(user)
        db_session.commit()
        session['username'] = user.username
        flash("Singed Up Successfully", 'success')
        return redirect("/")
    return render_template("signup.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    del session["username"]
    flash("Signed Out Successfully!", 'success')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
def personal_settings():
    from .forms import ChangeAvatarForm, ChangePasswordOrEmailForm, ChangeUserNameForm
    avatar_form = ChangeAvatarForm()
    email_password_form = ChangePasswordOrEmailForm()
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
    from .forms import ChangeAvatarForm
    from PIL import Image
    if not session.get("username"):
        return abort(404)
    form = ChangeAvatarForm(request.form)
    if request.method == 'POST' and form.validate():
        image_data = request.files[form.newAvatar.name]
        img = Image.open(image_data)
        if img.width > 2048 or img.height > 2048:
            flash("The image size is too big! Maximum: 1024x1024", 'error')
        cropped_image = crop_image(img)
        img.save(Path(__file__).parent.joinpath('static').joinpath(session['username']+'.jpg'))
        flash("Avatar Changed Successfully!", 'success')
        return redirect('/settings')


@app.route('/settings/user', methods=['GET', 'POST'])
def change_email_or_password():
    from .forms import ChangePasswordOrEmailForm
    from .models import User
    from .database import db_session
    from hashlib import sha256
    if not session.get("username"):
        return abort(404)
    form = ChangePasswordOrEmailForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == session['username']).first()
        if not user.password == sha256(form.oldPassword.data.encode()).hexdigest():
            flash("Password Incorrect", 'error')
            redirect('/settings')
        if form.password.data:
            user.password = sha256(form.password.data.encode()).hexdigest()
            db_session.commit()
            flash("Password Changed Successfully!", 'success')
        if form.newEmail.data:
            user.email = form.newEmail.data
            db_session.commit()
            flash("Email Changed Successfully!", 'success')
    if not form.newEmail.data and not form.password.data:
        flash("No Data Specified To Change", 'error')
    return redirect('/settings')


@app.route('/settings/username', methods=['GET', 'POST'])
def change_username():
    from .forms import ChangeUserNameForm
    from .models import User
    from .database import db_session
    from pathlib import Path
    import os
    if not session.get("username"):
        return abort(404)
    form = ChangeUserNameForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter(User.username == session['username']).first()
        user.username = form.new_username.data
        db_session.commit()
        path_to_avatars = Path(__file__).parent.joinpath('static')
        old_avatar = path_to_avatars.joinpath(session['username'] + '.jpg')
        if old_avatar.exists():
            os.rename(old_avatar, path_to_avatars.joinpath(user.username + '.jpg'))
        session['username'] = user.username
        flash("Username Changed Successfully!", 'success')
    return redirect('/settings')


@app.route('/comment/add', methods=['GET', 'POST'])
def add_comment():
    from .models import User, Comment, Article
    from .forms import CommentAddForm
    import datetime
    from .database import db_session
    form = CommentAddForm(request.form)
    if request.method == 'POST' and form.validate():
        if not session.get("username"):
            return redirect("/", code=404)
        user = User.query.filter(User.username == session["username"]).first()
        article_id = form.article_id.data
        article = Article.query.filter(Article.id == article_id).first()
        if not user or not article:
            return redirect("/", code=404)
        comment = Comment(datetime.datetime.now(), form.content.data, user.id)
        article.comments.append(comment)
        db_session.commit()
        flash("Comment Submitted Successfully!", 'success')
        return redirect("/article/{0}#comments".format(article_id))
    return redirect("/", code=404)


@app.route('/comment/delete/<int:comment_id>', methods=['GET', 'POST'])
def del_comment(comment_id):
    from .models import User, Comment
    from .database import db_session
    comment = Comment.query.filter(Comment.id == comment_id).first()
    if not comment:
        abort(404)
    article_id = comment.article_id
    if not comment:
        abort(404)
    user = User.query.filter(User.username == session['username']).first()
    if not user:
        abort(402)
    if user.id == comment.user_id:
        db_session.delete(comment)
        db_session.commit()
    return redirect(url_for("view_article", article_id=article_id))



@app.route('/submit', methods=['GET', 'POST'])
def add_article():
    from .models import User, Article
    from .forms import AddArticleForm
    import datetime
    from .database import db_session
    form = AddArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        if not session.get("username"):
            flash("Unauthorized publication attempt.")
            return redirect("")
        user = User.query.filter(User.username == session["username"]).first()
        if not user:
            flash("Invalid cookies. Please, login again.")
            return redirect("/signout")
        article = Article(form.name.data, datetime.datetime.now(), form.content.data, user.id)
        db_session.add(article)
        db_session.commit()
        flash("Article Created Successfully!", "success")
        return redirect('/article/{0}'.format(article.id))
    return render_template('submit.html', form=form)

@app.route('/delete/<int:article_id>', methods=['GET', 'POST'])
def delete_article(article_id):
    from .models import User, Article
    from .forms import DeleteArticleForm
    from .database import db_session
    form = DeleteArticleForm(request.form)
    article = Article.query.filter(Article.id == article_id).first()
    user = User.query.filter(User.username == session['username']).first()
    author = User.query.filter(User.id == article.author_id).first()
    if not article or not user or not author:
        return abort(404) # DB Failure or incorrect form data
    if user != author:
        return abort(403) # Unauthorized delete attempt
    if request.method == 'POST' and form.validate():
        for comment in article.comments:
            db_session.delete(comment)
        db_session.delete(article)
        db_session.commit()
        flash("Deletion successful.", category="success")
        return redirect('/')
    else:
        form.article_id = article_id
        return render_template('delete.html', form=form)

@app.route('/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    from .models import User, Article
    from .forms import EditArticleForm
    from .database import db_session
    form = EditArticleForm(request.form)
    article = Article.query.filter(Article.id == article_id).first()
    user = User.query.filter(User.username == session['username']).first()
    author = User.query.filter(User.id == article.author_id).first()
    if not article or not user or not author:
        return abort(404) # DB Failure or incorrect form data
    if user != author:
        return abort(403) # Unauthorized edit attempt
    if request.method == 'POST' and form.validate():
        article.content = form.content.data
        article.name = form.name.data
        db_session.commit()
        return redirect('/article/{0}'.format(article_id))
    else:
        form.content.data = article.content
        form.name.data = article.name
        return render_template('edit.html', form=form, article_id=article_id)