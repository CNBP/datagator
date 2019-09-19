from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404  # return template and error code.


@app.errorhandler(500)  # handel database errors
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500
