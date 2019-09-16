from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

# Main root rout.
@app.route("/")


# index page rout.
@app.route("/")  # this indicate which endpoint these actions will be carried out.
@app.route("/index")  # this indicate which endpoint these actions will be carried out.
@login_required  # this marks the page as login required.
def index():

    # The main function that was executed.
    user = {"username": "Data Structure"}

    posts = [
        {"author": {"username": "John"}, "body": "Nice!"},
        {"author": {"username": "Susan"}, "body": "Averages!"},
    ]

    # Return rendered template with the variables set.
    return render_template("index.html", title="Home", posts=posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    View function for the registration page.
    :return:
    """
    # Redirect to index if the user is already logged in.
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    # First, ensure the information contained in the form pass the validation phase.
    if form.validate_on_submit():

        # Create the user based on the data provided.
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        # Commit the information to the database.
        db.session.add(user)
        db.session.commit()
        # Inform the user.
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Instantiate form data object.
    form = LoginForm()

    # Deal with when visiting index when already authenticated.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()

    if form.validate_on_submit():

        # query User table from the database using the user name.
        # Will return NONE if it doesn't exist.
        user = User.query.filter_by(username=form.username.data).first()

        # Reject if no user or wrong password.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            # Redirect to login to retry again.
            return redirect(url_for("login"))

        # Login the actual user.
        login_user(user, remember=form.remember_me.data)

        # Flash warning required.
        flash(
            f"Welcome, User {form.username.data}, you have asked to rememebr you? {form.remember_me.data}"
        )

        # If the login URL includes a next argument that is set to a relative path (or in other words, a URL without the domain portion), then the user is redirected to that URL.
        next_page = request.args.get("next")

        # If the login URL does not have a next argument, then the user is redirected to the index page.
        if not next_page:
            next_page = url_for("index")

        # If the login URL includes a next argument that is set to a full URL that includes a domain name, then the user is redirected to the index page.
        if url_parse(next_page).netloc != "":
            next_page = url_for("index")

        # Redirect to a page should the form pass validation.
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)
