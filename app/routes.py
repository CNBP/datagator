from app import app

# Main root rout.
@app.route("/")

# index page rout.
@app.route("/index")

# The main function that was executed.
def index():
    return "Hello, World!"
