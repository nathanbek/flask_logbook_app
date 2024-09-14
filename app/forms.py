# forms.py

# app/forms.py

from flask_wtf import FlaskForm
from models import User
from wtforms import PasswordField, SelectField, StringField, SubmitField

# Define your form classes here
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('driver', 'Driver'), ('admin', 'Administrator')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.lower()).first()
        if user:
            raise ValidationError('Username already exists.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class RouteEntryForm(FlaskForm):
    date = DateField('Date', default=date.today(), validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    finish_time = TimeField('Finish Time', validators=[DataRequired()])
    start_mileage = IntegerField('Start Mileage', validators=[DataRequired()])
    end_mileage = IntegerField('End Mileage', validators=[DataRequired()])
    container_number = StringField('Container Number', validators=[DataRequired(), Length(max=20)])
    chassis_number = StringField('Chassis Number', validators=[DataRequired(), Length(max=20)])
    route_from = StringField('From', validators=[DataRequired(), Length(max=100)])
    route_to = StringField('To', validators=[DataRequired(), Length(max=100)])
    load_status = SelectField('Load Status', choices=[('Loaded', 'Loaded'), ('Empty', 'Empty')])
    standby_time_in = TimeField('Standby Time In', validators=[])
    standby_time_out = TimeField('Standby Time Out', validators=[])
    # Inspection Fields
    lights = BooleanField('Lights')
    tires = BooleanField('Tires')
    brakes = BooleanField('Brakes')
    # Add additional inspection fields as necessary
    remarks = TextAreaField('Remarks')
    submit = SubmitField('Submit')

    def validate_end_mileage(self, end_mileage):
        if end_mileage.data < self.start_mileage.data:
            raise ValidationError('End mileage cannot be less than start mileage.')

    def validate_finish_time(self, finish_time):
        if finish_time.data <= self.start_time.data:
            raise ValidationError('Finish time must be after start time.')
