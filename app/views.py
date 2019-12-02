from flask import render_template, abort
from jinja2 import Markup

from app import app

content = Markup('''<address>email@server.com</address>
        <h1>Article Name</h1>
        <h2>Contents</h2>
        <nav class="contents">
            <ol>
                <li><a href="#firstsection">First Section</a></li>
                <li><a href="#secondsection">Second Section</a></li>
            </ol>
        </nav>
        <h2 id="firstsection">First Section</h2>
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mi tempus imperdiet nulla malesuada. Eu feugiat pretium nibh ipsum. Nulla facilisi nullam vehicula ipsum a arcu cursus. Urna nec tincidunt praesent semper. Ac feugiat sed lectus vestibulum mattis ullamcorper. Dictum sit amet justo donec enim diam vulputate ut pharetra. Lacinia at quis risus sed vulputate. Tincidunt arcu non sodales neque sodales ut etiam sit. Elementum pulvinar etiam non quam. Urna nec tincidunt praesent semper feugiat nibh sed pulvinar proin.
        </p>
        <figure>
            <img src="https://cdn.pixabay.com/photo/2015/01/11/07/03/moe-595955_960_720.png">
            <figcaption>Random Anime Character</figcaption>
        </figure>
        <p>
            Nisi lacus sed viverra tellus in hac habitasse platea dictumst. Nunc mattis enim ut tellus elementum. Vitae auctor eu augue ut lectus. Nulla facilisi cras fermentum odio eu feugiat pretium. Velit scelerisque in dictum non consectetur a erat nam at. Suspendisse ultrices gravida dictum fusce ut placerat. Vel facilisis volutpat est velit egestas dui id ornare arcu. Commodo elit at imperdiet dui. Molestie nunc non blandit massa enim nec dui. Enim diam vulputate ut pharetra sit.
        </p>
        <p>
            Cras tincidunt lobortis feugiat vivamus at augue eget arcu dictum. Tortor at risus viverra adipiscing at in tellus. Et egestas quis ipsum suspendisse ultrices gravida dictum. Posuere morbi leo urna molestie. Orci nulla pellentesque dignissim enim sit amet venenatis urna cursus. Mauris sit amet massa vitae tortor. Sed sed risus pretium quam vulputate dignissim. In hendrerit gravida rutrum quisque non tellus orci ac. Nisi lacus sed viverra tellus in hac habitasse platea dictumst. Risus in hendrerit gravida rutrum quisque non. Pellentesque id nibh tortor id aliquet lectus proin nibh. Vulputate dignissim suspendisse in est ante in nibh mauris. Eget dolor morbi non arcu risus quis varius. Eget felis eget nunc lobortis mattis aliquam faucibus purus in. Volutpat est velit egestas dui.
        </p>
        <figure>
            <img src="https://cdn.pixabay.com/photo/2018/09/11/14/49/moe-3669736_960_720.png">
            <figcaption>Random Anime Character 2</figcaption>
        </figure>
        <h2 id="secondsection">Second Section</h2>
        <p>
            Fusce ut placerat orci nulla pellentesque dignissim enim sit amet. Ipsum dolor sit amet consectetur adipiscing elit duis. Nulla aliquet porttitor lacus luctus accumsan tortor. Id velit ut tortor pretium viverra. Proin libero nunc consequat interdum varius sit. Nec nam aliquam sem et tortor consequat id porta nibh. Tristique sollicitudin nibh sit amet commodo nulla. Nunc non blandit massa enim nec dui nunc mattis enim. Arcu bibendum at varius vel. Habitant morbi tristique senectus et netus et malesuada fames ac. Viverra nibh cras pulvinar mattis nunc sed blandit libero. Donec adipiscing tristique risus nec feugiat in fermentum. Dui vivamus arcu felis bibendum ut. Potenti nullam ac tortor vitae purus faucibus ornare. Nec ullamcorper sit amet risus nullam eget felis. Aliquam sem et tortor consequat. Sagittis aliquam malesuada bibendum arcu. Enim diam vulputate ut pharetra sit amet aliquam id.
        </p>
        <p>
            Id diam maecenas ultricies mi eget. Tempus imperdiet nulla malesuada pellentesque elit eget gravida cum. Nisl vel pretium lectus quam id. Rhoncus dolor purus non enim praesent elementum facilisis. Mollis aliquam ut porttitor leo a diam sollicitudin tempor. Purus ut faucibus pulvinar elementum integer enim. Consequat id porta nibh venenatis cras. Fermentum leo vel orci porta non pulvinar neque laoreet. A arcu cursus vitae congue mauris rhoncus. Risus quis varius quam quisque id diam vel quam elementum. Laoreet non curabitur gravida arcu ac tortor dignissim. Id eu nisl nunc mi ipsum. Faucibus nisl tincidunt eget nullam non nisi est sit. Enim diam vulputate ut pharetra sit amet aliquam. Lobortis scelerisque fermentum dui faucibus in ornare quam. Fermentum odio eu feugiat pretium nibh ipsum consequat nisl vel. Egestas fringilla phasellus faucibus scelerisque eleifend.
        </p>
        <figure>
            <img src="https://cdn.pixabay.com/photo/2017/04/02/18/49/manga-2196570_960_720.jpg">
            <figcaption>Random Anime Character 3</figcaption>
        </figure>''')
name = "Article Name"
blog = "Blog Name"

@app.route('/article_dummy')
def article():
    return render_template("article.html", articleName=name, blogName=blog, content=content)

@app.route('/')
def hello_world():
    return 'Dummy'

@app.route('/article/<int:article_id>')
def show_article(article_id):
    from jinja2 import Markup
    from .models import Article
    article = Article.query.filter(Article.id == article_id).first()
    if article:
        return render_template("article.html", articleName=article.name, blogName='Dummy Var', content=Markup(article.content))
    else:
        abort(404)

from .forms import SignUpForm
@app.route('/signin')
def signIn():
    return render_template("signin.html")

from flask import request, flash,redirect
from .database import db_session
from .models import User
@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    import hashlib
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data, hashlib.sha256(form.password.data.encode()).hexdigest())
        db_session.add(user)
        db_session.commit()
        flash("User record has been created!")
        return redirect("/")
    return render_template("signup.html", form=form)
