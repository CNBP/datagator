# from app.api import api_interface
from app.models import User
from flask import jsonify
from flask_restplus import Resource


# @api_interface.route("/users/<int:id>")
class User(Resource):
    def get(self, id):
        return jsonify(User.query.get_or_404(id).to_dict())

    def post(self):
        # todo: finish PAI
        pass


# @api_interface.route("/users/")
class HelloWorld(Resource):
    def get_users(self):
        return {"hello": "world"}
