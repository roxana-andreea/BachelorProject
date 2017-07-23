from wtforms import Form, BooleanField, DateTimeField, PasswordField
from wtforms import TextAreaField, StringField
from wtforms.validators import Length, DataRequired, Email, InputRequired, EqualTo
from wtforms.fields.html5 import EmailField
from werkzeug.datastructures import ImmutableMultiDict as multidict

class UserForm(Form):

    name = StringField('Name', validators=[
        InputRequired('Please enter your name.'),
        Length(max=255)
    ])
    email = EmailField('Email',  validators=[
        InputRequired('Please enter your email address.'),
        Email('Please enter your email address.'),
        Length(max=255)
    ])
    password = PasswordField('New Password', validators=[
        DataRequired('Please enter your password'),
        EqualTo('confirm', message='Passwords must match')])

    confirm = PasswordField('Repeat Password')

if __name__ == '__main__':
    # form = UserForm()
    # print('Here is how a form field displays:')
    # print(form.name.label)
    # print(form.name)

    data = multidict([
        ('name', 'Lupu Cristian'),
        ('email','cristianlupu@gmail.com'),
        ('password','secret'),
        ('confirm','secret')
    ])
    form = UserForm(data)
    print('Here is validation...')
    print('Does it validate: {}'.format(form.validate()))
    print('There is an error attached to the field...')
    print('form.errors: {}'.format(form.errors))