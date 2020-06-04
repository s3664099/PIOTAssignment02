"""
.. module:: forms

"""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.core import SelectField

def my_length_check(form, field):
    """
    Length check for validation

    """
    if len(field.data) > 20:
        raise ValidationError('Field must be less than 20 characters')

def my_password_check(form, field):
    """
    Password check for validation

    """
    if len(field.data) < 8:
        raise ValidationError('Password must be at least 8 characters')
    if re.search('[0-9]', field.data) is None:
        raise ValidationError("Make sure your password has a number in it")
    elif re.search('[A-Z]', field.data) is None: 
       raise ValidationError("Make sure your password has a capital letter in it")


class RegistrationForm(FlaskForm):
    """
    Registration flask form

    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=6, max=20),my_length_check])
    firstname = StringField('First Name',
                            validators=[DataRequired(),my_length_check])
    lastname = StringField('Last Name')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), my_password_check], description="Minimum 8 Characters, 1 Capital, 1 number")
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """
    Login flask form

    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices = [('Admin'),('Manager'),('Engineer')], validators = [DataRequired()])
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    """
    Booking flask form

    """
    email = StringField('Email',validators=[DataRequired()])
    rego = StringField('Car',validators=[DataRequired()])
    pickup = DateField('PickUp Date', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    dropoff = DateField('Drop Off Date', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    submit = SubmitField('bookedcar')
