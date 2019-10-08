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
    ResetPasswordRequestForm,  # the form that can REQUEST the reset the password
    ResetPasswordForm,  # the form that is actually resetting the password
)
from app.forms_entries import (
    NeonatalDataForm_Submit,
    NeonatalDataForm_Update,
    RequestEntryForm,
)

from flask_login import (  # flask_login module is a module to help manage module
    current_user,  # get the active logged in user.
    login_user,  # login the user action.
    logout_user,  # used to logout user
    login_required,  # used to @login_required decorator to indicate a route MUST be logged in before showing.
)
from app.models import (
    User,
    Post,
    Entry,
)  # import data base model for User and Post construct.
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email
import json

"""
This file is responsible for ROUTING the VIEW functions. What happens when you look at a page etc?

Any view needs to be defined here. 

"""

import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

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

    # Get the page argumetn from the URL entered. Default to 1?
    page = request.args.get("page", 1, type=int)

    # Use the paginate function from SQLAlchemy to get the posts.
    posts = current_user.followed_posts().paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    # Next URL if they exist.
    next_url = url_for("index", page=posts.next_num) if posts.has_next else None

    # Previous URL if they exist
    prev_url = url_for("index", page=posts.prev_num) if posts.has_prev else None

    # Return rendered template with the variables set.
    # Post > Redirect > Get pattern.
    return render_template(
        "index.html",
        title="Home, Sweet Home!",
        form=form,
        posts=posts.items,  # must use ITEMS if using pagination
        next_url=next_url,
        prev_url=prev_url,
    )


@app.route("/user/<username>")
@login_required
def user(username):
    """
    This shows the information for the relevant username.
    :param username:
    :return:
    """
    # set user
    user = User.query.filter_by(username=username).first_or_404()

    # set current pagination limit
    page = request.args.get("page", 1, type=int)

    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )

    next_url = (
        url_for("user", username=user.username, page=posts.next_num)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for("user", username=user.username, page=posts.prev_num)
        if posts.has_prev
        else None
    )

    # Post > Redirect > Get pattern.
    return render_template(
        "user.html", user=user, posts=posts.items, next_url=next_url, prev_url=prev_url
    )


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
    This allows editing of the profile.
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
    # Default page argumet is 1. Otherwise, based
    page = request.args.get("page", 1, type=int)

    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    next_url = url_for("explore", page=posts.next_num) if posts.has_next else None
    prev_url = url_for("explore", page=posts.prev_num) if posts.has_prev else None

    return render_template(
        "index.html",
        title="Explore",
        posts=posts.items,  # this must include ITEMS when using pagination
        prev_url=prev_url,
        next_url=next_url,
    )


@app.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    """
    Page where user can request the reset of the password
    :return:
    """
    # if logged in, return to index.
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    # Instantiate the form object.
    form = ResetPasswordRequestForm()

    # if form validate successfully,
    if form.validate_on_submit():

        # Get user by email.
        user = User.query.filter_by(email=form.email.data).first()

        # if user EXIST, send email.
        if user:
            send_password_reset_email(user)

        # Display to inform user.
        flash("Check your email for the instruction to reset your password")

        # Redirect to login.
        return redirect(url_for("login"))

    return render_template(
        "reset_password_request.html", title="Reset Password", form=form
    )


@login_required
@app.route("/data_entry/", methods=["GET", "POST"])
def data_entry():
    """
    View function where the editing of the actual functions happen.
    :return:
    """
    # Instantiate the form
    form = NeonatalDataForm_Submit()
    # If past validation, during submission,
    if form.validate_on_submit():

        # Retrieve from database the row that contain the user name.
        user_current = User.query.filter_by(
            username=current_user.username
        ).first_or_404()

        # Create the ENTRY model data
        entry = Entry(
            MRN=form.MRN.data,
            CNBPID=form.CNBPID.data,
            birth_weight=form.birth_weight.data,
            birth_date=form.birth_date.data,
            birth_time=form.birth_time.data,
            mri_date=form.mri_date.data,
            mri_reason=json.dumps(form.mri_reason.data),
            mri_age=form.mri_age.data,
            user_id=user_current.id,
        )
        db.session.add(entry)
        db.session.commit()

        # Notify the issue.
        flash("Your data entry has been successfully written to the database.")
        # return redirect(url_for("index"))

    return render_template("data_entry.html", title="Add a Data Entry", form=form)


@login_required
@app.route("/data_request/", methods=["POST", "GET"])
def data_request():
    """
    The place to place a request to view data ENTRY form. 
    :return:
    """
    form = RequestEntryForm(current_user.username)
    if form.validate_on_submit():
        id_form = int(form.id.data)
        logger.info(id_form)
        logger.info("Reached here!")
        flash(f"Requesting entry data from ID={str(id_form)}.")
        return redirect(url_for("data_view", id_entry=id_form))
    return render_template("data_view.html", title="Load a Data Entry", form=form)


@login_required
@app.route("/data_view/<id_entry>", methods=["GET", "POST"])
def data_view(id_entry):
    """
    View function where the editing of the actual functions happen.
    :return:
    """

    # Instantiate the form with NO default values.
    form = NeonatalDataForm_Update()

    # Instantiate the data object from the SQL records.
    entry_data = Entry.query.filter_by(id=id_entry).first()

    # No data found path:
    # Entry ID based on the parameter passed to the page
    if entry_data is None:
        flash("No suitable data found.")

    # Deletion path: delete the database entry.
    elif form.delete_entry.data:
        # Only delete when all set.
        if (
            form.delete_entry.data
            and form.confirm_delete.data
            and form.confirm_double_delete.data
        ):
            flash(f"Deleting this entry{id_entry}")
            Entry.query.filter_by(id=id_entry).delete()
            db.session.commit()
            flash(f"Entry {id_entry} deleted!")
            return redirect(url_for("data_request"))
        else:
            flash("Deletion aborted due to insufficient confirmation")

    # Update info path:
    # If past validation and submitted, commit to database.
    elif form.validate_on_submit() and form.update_entry.data:
        # Update.ENTRY model data
        entry_data.MRN = form.MRN.data
        entry_data.CNBPID = form.CNBPID.data
        entry_data.birth_weight = form.birth_weight.data
        entry_data.birth_date = form.birth_date.data
        entry_data.birth_time = form.birth_time.data
        entry_data.mri_date = form.mri_date.data
        entry_data.mri_reason = json.dumps(form.mri_reason.data)
        entry_data.mri_age = form.mri_age.data
        db.session.commit()

        # Notify the issue.
        flash(f"Data entry {id_entry} has been successfully updated to the database!")
    # Data found path:
    else:
        form.MRN.data = int(entry_data.MRN)
        form.CNBPID.data = entry_data.CNBPID
        form.birth_weight.data = float(entry_data.birth_weight)
        form.birth_date.data = entry_data.birth_date
        form.birth_time.data = entry_data.birth_time
        form.mri_date.data = entry_data.mri_date
        form.mri_age.data = float(entry_data.mri_age)
        # form.submit.render_kw = {"disabled": "disabled"}
        # form.submit(disabled=True, readonly=True)
        form.mri_reason.data = json.loads(entry_data.mri_reason)

        flash(f"Data entry {id_entry} has been successfully loaded from the database.")

    # Post > Redirect > Get pattern.
    return render_template("data_view.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    View function of actual form to reset the password by setting it on the page.
    :param token:
    :return:
    """
    # Reject when already authenticated.
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    # verify the token to get the username.
    user = User.verify_reset_password_token(token)

    # if None (i.e. bad token) do not proceed.
    if not user:
        return redirect(url_for("index"))

    # Instantiate resetpassword form.
    form = ResetPasswordForm()

    # if the form is valid,
    if form.validate_on_submit():

        # set the password for this user.
        user.set_password(form.password.data)

        # push to data base.
        db.session.commit()

        flash("Your password has been reset.")

        return redirect(url_for("login"))

    return render_template("reset_password.html", form=form)
