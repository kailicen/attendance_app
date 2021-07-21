from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from attendance.models import User


class GuestForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile Phone')
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


class MemberForm(FlaskForm):
    member_names = SelectField(
        'Choose your name...', validators=[DataRequired()],)
    submit = SubmitField('Submit')


class AdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
