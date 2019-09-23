from app import app, db
from flask import (
    render_template,  # flask function to render a HTML template with elements replaced.
    flash,  # show a message overlay.
    redirect,  # redirect to another page.
    url_for,  # used to interpret endpoints.
    request,
)
from app.forms import (
    LoginForm,  # our project customary forms built here to carry out login function.
    RegistrationForm,  # our project customary forms built here to carry out login function.
    EditProfileForm,  # our edit profile form
    PostForm,  # our form about post editing
)

from flask_login import (  # flask_login module is a module to help manage module
    current_user,  # get the active logged in user.
    login_user,  # login the user action.
    logout_user,  # used to logout user
    login_required,  # used to @login_required decorator to indicate a route MUST be logged in before showing.
)
from app.models import User, Post  # import data base model for User and Post construct.
from werkzeug.urls import url_parse
from datetime import datetime


"""
This file is responsible for ROUTING the VIEW functions. What happens when you look at a page etc?

Any view needs to be defined here. 

"""

# index page rout.
@app.route(
    "/", methods=["GET", "POST"]
)  # this indicate which endpoint these actions will be carried out.
@app.route(
    "/index", methods=["GET", "POST"]
)  # this indicate which endpoint these actions will be carried out.
@login_required  # this marks the page as login required.
def index():

    form = PostForm()

    # If form past validation, update the database with the post information and notify user while redirect to current page.
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post is now live!")
        return redirect(url_for("index"))

    posts = current_user.followed_posts().all()

    # Return rendered template with the variables set.
    # Post > Redirect > Get pattern.
    return render_template(
        "index.html", title="Home, Sweet Home!", form=form, posts=posts
    )


@app.route("/user/<username>")
@login_required
def user(username):
    """
    This shows the information for the relevant username.
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    # Post > Redirect > Get pattern.
    return render_template("user.html", user=user, posts=posts)


@app.route("/logout")
def logout():
    """
    End point to log out the user
    :return:
    """
    logout_user()  # from the flask_login module
    return redirect(url_for("index"))


@app.before_request
def before_request():
    """
    This is executed every time before a view request happen, put something that required logging here typically
    :return:
    """
    # If authenticated
    if current_user.is_authenticated:

        # Set the date column value to this.
        current_user.last_seen = datetime.utcnow()

        # Commit the information to the database.
        db.session.commit()


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
        # Set the password field entry.
        user.set_password(form.password.data)

        # Commit the information to the database.
        db.session.add(user)
        db.session.commit()

        # Inform the user.
        flash("Congratulations, you are now a registered user!")
        # Redirect to login.
        return redirect(url_for("login"))

    # if form not valid, redirect to register page.
    return render_template("register.html", title="Register", form=form)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    This allows
    :return:
    """

    # Instantiate the form
    form = EditProfileForm(current_user.username)

    # If past validation, during submission,
    if form.validate_on_submit():

        # assign username, about me info
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))

    # if it is just to get data, load from database.
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    The login endpoint.
    :return:
    """
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


@app.route("/follow/<username>")
@login_required
def follow(username):
    """
    Follow a user provided by the username.
    :param username:
    :return:
    """
    # Check against the database.
    user = User.query.filter_by(username=username).first()

    # If doesn't exist,
    if user is None:
        flash(f"User {username} not found.")
        return redirect(url_for("index"))
    # If it is current user.
    if user == current_user:
        flash("You cannot follow yourself!")
        return redirect(url_for("user", username=username))

    # Commit change to database.
    current_user.follow(user)
    db.session.commit()

    # flash and redirect.
    flash("You are following {username}!")
    return redirect(url_for("user", username=username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    """
    Unfollow a particular user.
    :param username:
    :return:
    """
    # Check against the database.
    user = User.query.filter_by(username=username).first()

    # If it doesn't exist
    if user is None:
        flash(f"User {username} not found.")
        return redirect(url_for("index"))

    # if it is the user,
    if user == current_user:
        flash("You cannot unfollow yourself!")
        return redirect(url_for("user", username=username))

    # unfollow user and commit to database.
    current_user.unfollow(user)
    db.session.commit()
    flash("You are not following {username}")
    return redirect(url_for("user", username=username))


@app.route("/explore")
@login_required
def explore():
    """
    Explore the global posts stream
    :return:
    """
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("index.html", title="Explore", posts=posts)
