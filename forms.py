"""Forms for notes app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length
# TODO: email validator

class RegisterForm(FlaskForm):
    """Form for new user registration"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=30)])

    password = PasswordField("Password", validators=[InputRequired()])

    email = EmailField(
        "Email",
        validators=[InputRequired(), Length(max=50)])

    first_name = StringField(
        "First name",
        validators=[InputRequired(), Length(max=30)])

    last_name = StringField(
        "Last name",
        validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """Form for login"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=30)])

    password = PasswordField("Password", validators=[InputRequired()])


class CSRFProtectForm(FlaskForm):
    """Form for CSRF protection"""

