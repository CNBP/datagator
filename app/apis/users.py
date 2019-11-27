from app.models import User
from flask import jsonify
from flask_restplus import Namespace, Resource, fields

api_user = Namespace("Users", description="Users related operations")

user = api_user.model(
    "User",
    {
        "id": fields.String(required=True, description="The user identifier"),
        "name": fields.String(required=True, description="The user name"),
    },
)


@api_user.route("/")
class CatList(Resource):
    @api_user.doc("list_users")
    @api_user.marshal_list_with(user)
    def get(self):
        return jsonify(User.query.get_or_404(id).to_dict())


@api_user.route("/<id_user>")
@api_user.param("id_user", "The user identifier")
@api_user.response(404, "Cat not found")
class Cat(Resource):
    @api_user.doc("get_user")
    @api_user.marshal_with(user)
    def get(self, id_user):
        """Fetch a user given its identifier"""
        for user in User.query.get_or_404(id_user).to_dict():
            if user["id_user"] == id_user:
                return user
        api_user.abort(404)
