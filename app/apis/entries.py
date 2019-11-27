from app.models import Entry, User
from flask import jsonify
from flask_login import current_user
from flask_restplus import Namespace, Resource, fields


api_entry = Namespace("Entries", description="Medical entries related operations")

entry = api_entry.model(
    "Entry",
    {
        "MRN": fields.Integer(required=True, description="The MRN number"),
        "CNBPID": fields.String(required=True, description="The CNBPID"),
        "birth_weight": fields.Float(description="The weight at birth"),
        "birth_date": fields.Date(description="The date of birth"),
        "birth_time": fields.String(description="The time of birth"),
        "mri_date": fields.Date(required=True, description="The date of MRI"),
        "mri_reason": fields.String(description="The reason of MRI"),
        "mri_dx": fields.String(description="The diagnoses of MRI"),
        "discharge_diagnoses": fields.String(description="Diagnoses at discharge time"),
        "mri_age": fields.Float(required=True, description="The age of MRI"),
        "timestamp": fields.DateTime(
            required=True, description="The time stamp of the entry"
        ),
        "user_id": fields.Integer(required=True, description="The ID of the user"),
    },
)


@api_entry.route("/")
class APIEntriesList(Resource):
    @api_entry.doc("list_entries")
    @api_entry.marshal_list_with(entry)
    def get(self):
        """
        Get all the currently known entries and marshal them into a list.
        :return:
        """
        Entry.query.all()

        return


@api_entry.route("/<entry_id>")
@api_entry.param("entry_id", "The entry identifier")
@api_entry.response(404, "Entry ID not found")
class APIEntry(Resource):
    @api_entry.doc("get_entry")
    @api_entry.marshal_with(entry)
    def get(self, entry_id):
        """
        Fetch a specific entry using the provided ID
        :param entry_id:
        :return:
        """
        return Entry.query.filter_by(id=int(entry_id)).first_or_404()
