from flask_wtf import FlaskForm
<<<<<<< HEAD
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 20 characters')

class GreaterThan(object):
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data < other.data:
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('DropOff must be greater than %(other_name)s.')

            raise ValidationError(message % d)


=======
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateTimeField, SelectField, FloatField
>>>>>>> fd63c84b2f1db35ae162d4cf1927034dadfb6ac3
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
<<<<<<< HEAD
    email = StringField('Email',validators=[DataRequired()])
    rego = StringField('Car',validators=[DataRequired()])
    pickup = DateField('PickUp Date', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired()])
    dropoff = DateField('Drop Off Date', format='%Y-%m-%d %H:%M:%S',validators=[DataRequired(),GreaterThan('pickup')])
    submit = SubmitField('bookedcar')


=======
    
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
>>>>>>> fd63c84b2f1db35ae162d4cf1927034dadfb6ac3
