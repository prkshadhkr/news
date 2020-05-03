from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

COUNTRIES = ["","ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn",
            "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu",
            "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", 
            "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", 
            "rs", "ru", "sa", "se", "sg", "si", "sk", "th","tr", "tw", 
            "ua", "us", "ve", "za"]


class SignupForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    country = SelectField('Country', choices=[(country, country) for country in COUNTRIES])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
