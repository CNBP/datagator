from flask import Blueprint

bp = Blueprint("api", __name__)

# avoid circular dependencies
from app.api import users, errors, tokens
from app import api_interface
