from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 20 characters')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20),my_length_check])
    firstname = StringField('First Name',
                            validators=[DataRequired(),my_length_check])
    lastname = StringField('Last Name')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    rego = StringField('Car',validators=[DataRequired()])
    pickup = DateField('PickUp Date', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    dropoff = DateField('Drop Off Date', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    submit = SubmitField('bookedcar')
