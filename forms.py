from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length
from constants import COUNTRIES, CATEGORIES



class UserEditForm(FlaskForm):
    """Form for editing users."""
	
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    country = SelectField('Country', choices=COUNTRIES)

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class AddForm(FlaskForm):
    """Form for adding/editing boards and feeds"""

    name = StringField('name', validators=[DataRequired()])

class CountryForm(FlaskForm):
    """Form for selecting country."""

    country = SelectField('Country', choices=COUNTRIES)

class CategoryByCountry(FlaskForm):
    """Form for selecting category by country"""

    country = SelectField('Country', choices=COUNTRIES)
    category = SelectField('Category', choices=CATEGORIES)