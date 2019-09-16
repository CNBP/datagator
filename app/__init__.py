from flask import Flask
from configfile import ConfigClass
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Load configuration from the object class.
app.config.from_object(ConfigClass)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Instnatiate the LoginManager for this current app.
login = LoginManager(app)

# The page to direct people to login if they are required.
login.login_view = "login"

from app import routes, models
