from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, Regexp, Length, EqualTo, ValidationError
import email_validator
import re
from contacts_app.models import User


class ContactForm(FlaskForm):
    name = StringField('Name :', validators=[InputRequired()])
    email = StringField('Email id :', validators=[InputRequired(), Email(message='Invalid email')])

    reg = re.compile("^[0-9]{10}$")
    mob = StringField('Mobile no.:', validators=[InputRequired(), Regexp(reg, message='Invalid number')])

    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    username = StringField('Username :', validators=[InputRequired()])

    email = StringField('Email id :', validators=[InputRequired(), Email(message='Invalid email')])

    password = PasswordField('New password: ', validators=[InputRequired(), Length(min=8, message='Password should be at least 8 characters long')])

    retype_password = PasswordField('Confirm password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

    submit = SubmitField('Create new account')

    # custom validations
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account is already registered with this email.')


class LoginForm(FlaskForm):
    username = StringField('Username :', validators=[InputRequired()])

    password = PasswordField('Password: ', validators=[InputRequired(), Length(min=8, message='Password should be at least 8 characters long')])

    submit = SubmitField('Login')
