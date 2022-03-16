# Import Modules
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.widgets import TextArea


# FORMS
class AddRecipeForm(FlaskForm):
    name = StringField("Recipe Name")
    desc = StringField("Description", widget=TextArea())
    ingredients = StringField("Ingredients", widget=TextArea())
    method = StringField("Method", widget=TextArea())
    image = StringField("Image URL")
    submit = SubmitField("Submit")


class AdminLogin(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")


class ContactForm(FlaskForm):
    name = StringField("Full Name")
    email = StringField("Email")
    message = StringField("Message", widget=TextArea())
    submit = SubmitField("Submit")
