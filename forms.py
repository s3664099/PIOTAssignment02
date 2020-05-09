from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectField, FloatField
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('First Name',
                            validators=[DataRequired()])
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
    
    cars = car.cur.fetchall()
    car_list = []
    #car.rego, car.make + car.model
    for car in cars:
        car_make_model = car.make + " " + car.model
        car_list.append((car.rego,car_make_model ))

    rego = SelectField('Cars',choices=car_list, validators=[DataRequired()])
    
    pickuptime = DateTimeField('Start Date/Time', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    dropofftime = DateTimeField('End Date/Time', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    totalcost = FloatField('Total Cost', validators=[DataRequired()])