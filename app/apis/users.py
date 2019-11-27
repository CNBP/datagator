from app.models import User
from flask import jsonify
from flask_restplus import Namespace, Resource, fields

api = Namespace("Users", description="Users related operations")

user = api.model(
    "User",
    {
        "id": fields.String(required=True, description="The user identifier"),
        "name": fields.String(required=True, description="The user name"),
    },
)


@api.route("/")
class CatList(Resource):
    @api.doc("list_users")
    @api.marshal_list_with(user)
    def get(self):
        return jsonify(User.query.get_or_404(id).to_dict())


@api.route("/<id>")
@api.param("id", "The user identifier")
@api.response(404, "Cat not found")
class Cat(Resource):
    @api.doc("get_user")
    @api.marshal_with(user)
    def get(self, id):
        """Fetch a user given its identifier"""
        for user in User.query.get_or_404(id).to_dict():
            if user["id"] == id:
                return user
        api.abort(404)
