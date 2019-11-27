from flask_restplus import Api
from flask import Blueprint
from .users import api as ns1

bp = Blueprint("api", __name__)
api_interface = Api(
    bp,
    title="DataGator API",
    version="1.0",
    description="A MVP API for DataGator implementing RestPlus+",
    doc="/doc/",
)
api_interface.add_namespace(ns1, path="/users")
