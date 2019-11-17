from flask import Blueprint

bp = Blueprint("configs", __name__)

from app.configs import routes
