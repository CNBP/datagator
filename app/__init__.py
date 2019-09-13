from flask import Flask
from configfile import ConfigClass
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Load configuration from the object class.
app.config.from_object(ConfigClass)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models
