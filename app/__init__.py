from flask import Flask
from configfile import ConfigClass

app = Flask(__name__)

# Load configuration from the object class.
app.config.from_object(ConfigClass)

from app import routes
