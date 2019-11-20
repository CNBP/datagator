from app import (
    create_app,
    db,
)  #  a Python script at the top-level that defines the Flask application

# instantiate the Flask app using the create app method there with the default parameter.
app = create_app()
from app.models import User, Post


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}
