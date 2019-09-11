from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

# Main root rout.
@app.route("/")

# index page rout.
@app.route("/index")
def index():
    # The main function that was executed.
    user = {"username": "Data Structure"}
    posts = [
        {"author": {"username": "John"}, "body": "Nice!"},
        {"author": {"username": "Susan"}, "body": "Averages!"},
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Instantiate form data object.
    form = LoginForm()

    if form.validate_on_submit():

        # Flash warning required.
        flash(
            f"Login requested for user {form.username.data}, rememebr_me={form.remember_me.data}"
        )

        # Redirect to a page should the form pass validation.
        return redirect(url_for("index"))

    return render_template("login.html", title="Sign In", form=form)
