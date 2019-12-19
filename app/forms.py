from wtforms import Form, TextAreaField, PasswordField, validators, IntegerField, StringField, HiddenField, FileField


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('E-mail', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])


class CommentAddForm(Form):
    content = TextAreaField("Post", [validators.length(min=3, max=1024)])
    article_id = HiddenField("Article ID")


class ChangeAvatarForm(Form):
    newAvatar = FileField("New Avatar")


class ChangePasswordOrEmailForm(Form):
    oldPassword = PasswordField('Old Password', [
        validators.DataRequired(),
    ])
    password = PasswordField('New  Password', [
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat New Password')
    newEmail = StringField(64)


class ChangeUserNameForm(Form):
    new_username = StringField('Username', [validators.Length(min=4, max=25),
                                            validators.DataRequired()])


class AddArticleForm(Form):
    name = StringField('Article Name', [validators.data_required(),
                                          validators.Length(min=5, max=64)])
    content = TextAreaField('Content', [validators.data_required(),
                                        validators.Length(min=128)])


class EditArticleForm(Form):
    name = StringField('Article Name', [validators.data_required(),
                                          validators.Length(min=5, max=256)])
    content = TextAreaField('Content', [validators.data_required(),
                                        validators.Length(min=5)])

class DeleteCommentForm(Form):
    comment_id = HiddenField('Comment ID')
    article_id = HiddenField('Article ID')
