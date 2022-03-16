# Import Modules
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Length
from wtforms.widgets import TextArea


# FORMS
class AddRecipeForm(FlaskForm):
    name = StringField("Recipe Name")
    desc = StringField("Description", widget=TextArea(), validators=[Length(max=1500)])
    ingredients = StringField("Ingredients", widget=TextArea(), validators=[Length(max=1500)])
    method = StringField("Method", widget=TextArea(), validators=[Length(max=1500)])
    image = StringField("Image URL")
    submit = SubmitField("Submit")


class AdminLogin(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField("Full Name")
    email = StringField("Email")
    message = StringField("Message", widget=TextArea(), validators=[Length(max=1500)])
    submit = SubmitField("Submit")
