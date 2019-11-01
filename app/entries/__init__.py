from flask import Blueprint

bp = Blueprint("entries", __name__)

from app.entries import routes
