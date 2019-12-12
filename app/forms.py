from wtforms import Form, TextAreaField, PasswordField, validators, IntegerField, StringField, HiddenField, FileField


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
    content = TextAreaField("Post", [validators.length(min=3, max=1024)])
    article_id = HiddenField("Article ID")


class AvatarSettingsForm(Form):
    newAvatar = FileField("New Avatar")


class PasswordOrEmailForm(Form):
    oldPassword = PasswordField('Old Password', [
        validators.DataRequired(),
    ])
    password = PasswordField('New  Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat New Password')
    newEmail = StringField(64)

class ChangeUserNameForm(Form):
    new_username = StringField('Username', [validators.Length(min=4, max=25)])

