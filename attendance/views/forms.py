from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from attendance.models import User


class GuestForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError(
                'That name is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_mobile(self, mobile):
        enter_mobile = mobile.data.replace(" ", "")
        if enter_mobile.isnumeric() == False:
            raise ValidationError(
                'Please enter the right format of mobile number.')
        format_mobile = enter_mobile[:-6] + " " + \
            enter_mobile[-6:-3] + " " + enter_mobile[-3:]
        user = User.query.filter_by(mobile=format_mobile).first()
        if user:
            raise ValidationError(
                'That mobile number is taken. Please choose a different one.')


class MemberForm(FlaskForm):
    member_names = SelectField(
        'Choose your name...', validators=[DataRequired()],)
    submit = SubmitField('Submit')


class ReturnGuestForm(FlaskForm):
    guest_names = SelectField(
        'Choose your name...', validators=[DataRequired()],)
    submit = SubmitField('Submit')


class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
