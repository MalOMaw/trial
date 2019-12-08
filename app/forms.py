from wtforms import Form, StringField, PasswordField, validators, IntegerField


class SignUpForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class SignInForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])

class PostSubmitForm(Form):
    content = StringField("Post", [validators.length(min=3, max=1024)])
    article_id = IntegerField("Article ID")