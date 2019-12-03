from wtforms import Form, StringField, PasswordField, validators


class SignUpForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class SignUpForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])