"""Forms for notes app."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for new user registration"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=30)])

    password = PasswordField("Password", validators=[InputRequired()])

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)])

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


class AddNoteForm(FlaskForm):
    """Form for adding note"""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)] )

    content = TextAreaField("Content", validators=[InputRequired()])

class EditNoteForm(AddNoteForm):
    """Form for editing a note"""

# class EditNoteForm(FlaskForm): 
#     """Form for editing a note"""

#     title = StringField("Title", validators=[InputRequired(), Length(max=100)] )

#     content = TextAreaField("Content", validators=[InputRequired()])