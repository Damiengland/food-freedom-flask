# Import Modules
import os
from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_bootstrap import Bootstrap
import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
import smtplib
# Local Files
from config import Config
from forms import AddRecipeForm, AdminLogin, ContactForm


# Initialize files
config = Config()

# SETUP
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_BASE", "sqlite:///food-freedom.db")
# Optional but will silence the deprecation warning in the console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# DATE
date = dt.date.today().year


# SEND EMAIL
def send_email(name, from_addr, message):
    """Sends an email using a forwarding address"""
    send_addr = config.EMAIL_USER
    email_pass = config.EMAIL_PASS

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()  # Secures connection
        connection.login(user=send_addr, password=email_pass)
        connection.sendmail(from_addr=send_addr, to_addrs="karen.england@optusnet.com.au",
                            msg=f"Subject:Contact form: {name}\n\n"
                                f"NAME: {name}\n"
                                f"EMAIL: {from_addr}\n"
                                f"MESSAGE: {message}",
                            )


# BUILD DATABASE STRUCTURE
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(1500), nullable=False)
    ingredients = db.Column(db.String(1500), nullable=False)
    method = db.Column(db.String(1500), nullable=False)
    image = db.Column(db.String(400), nullable=True)

    def __repr__(self):
        return f"<Recipe {self.name}"


# Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))


# Only needs to be executed once.
db.create_all()


# Extra security measure ensuring only the admin has editing permission
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


# ROUTES
@app.route("/")
def home():
    logout_user()
    return render_template("index.html", current_user=current_user, date=date)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(name=form.name.data, from_addr=form.email.data, message=form.message.data)
        flash("Email sent.")
        return redirect(url_for('contact'))
    return render_template("pages/contact.html", form=form, date=date)


@app.route("/about")
def about():
    return render_template("pages/about.html", date=date)


@app.route("/recipes")
def recipes():
    all_recipes = Recipe.query.order_by(Recipe.id).all()
    return render_template("pages/recipes.html", recipes=all_recipes, date=date)


@app.route("/recipe-item")
def recipe_item():
    recipe_id = request.args.get("id")
    recipe = Recipe.query.get(recipe_id)
    return render_template("pages/recipe-item.html", recipe=recipe, date=date)


@app.route("/weight-loss")
def weight_loss():
    return render_template("pages/weight-loss.html", date=date)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Authenticates user input against admin login."""
    form = AdminLogin()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("Username does not exist.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('admin'))

    return render_template("admin/login.html", form=form)


@app.route("/admin", methods=["GET", "POST"])
@login_required
@admin_only
def admin():
    return render_template("admin/admin.html", logged_in=True)


@app.route("/add", methods=["GET", "POST"])
@login_required
@admin_only
def add():
    """Adds database entry on submit from the form data"""
    form = AddRecipeForm()
    if form.validate_on_submit():

        image = form.image.data
        split_url = image.split("/")
        try:
            converted_image = f"https://drive.google.com/uc?export=view&id={split_url[5]}"
        except IndexError:
            converted_image = image

        new_recipe = Recipe(
            name=form.name.data,
            desc=form.desc.data,
            ingredients=form.ingredients.data,
            method=form.method.data,
            image=converted_image
        )
        db.session.add(new_recipe)
        db.session.commit()

        logout_user()

        return redirect(url_for('home'))
    return render_template("admin/add.html", form=form, logged_in=True)


@app.route("/select", methods=["GET", "POST"])
@login_required
@admin_only
def select():
    """Searches database and displays all recipes to select action."""
    all_recipes = Recipe.query.order_by(Recipe.id).all()
    return render_template("admin/select.html", recipes=all_recipes, logged_in=True)


@app.route("/edit", methods=["GET", "POST"])
@login_required
@admin_only
def edit():
    """Finds recipe from URL ID argument. Updates found recipe on submit with field inputs."""
    recipe_id = request.args.get("id")
    recipe = Recipe.query.get(recipe_id)
    form = AddRecipeForm(
        name=recipe.name,
        desc=recipe.desc,
        ingredients=recipe.ingredients,
        method=recipe.method,
        image=recipe.image
    )

    if form.validate_on_submit():

        recipe.name = form.name.data
        recipe.desc = form.desc.data
        recipe.ingredients = form.ingredients.data
        recipe.method = form.method.data
        recipe.image = form.image.data

        db.session.commit()

        logout_user()

        return redirect(url_for('home'))

    return render_template("admin/edit.html", form=form, recipe=recipe, logged_in=True)


@app.route("/delete", methods=["GET", "POST"])
@login_required
@admin_only
def delete():
    """Finds & deletes the recipe from the ID url argument."""
    recipe_id = request.args.get("id")
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()

    logout_user()

    return redirect(url_for('home'))


# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)
