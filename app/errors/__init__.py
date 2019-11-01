# Erros blueprint

from flask import Blueprint

# Name of the blueprint, name of the base module
bp = Blueprint("errors", __name__)

from app.errors import handlers
