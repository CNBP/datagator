from flask_restplus import Api
from flask import Blueprint
from .users import api_user
from .entries import api_entry

bp = Blueprint("api_user", __name__)
api_interface = Api(
    bp,
    title="DataGator API",
    version="1.0",
    description="A MVP API for DataGator implementing RestPlus+",
    doc="/doc/",
)
api_interface.add_namespace(api_user, path="/users")
api_interface.add_namespace(api_entry, path="/entrys")
