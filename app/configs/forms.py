from datetime import date, datetime, timedelta
import sys
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    FloatField,
    DateField,
    TimeField,
    SelectMultipleField,
    SubmitField,
    ValidationError,
    BooleanField,
    Field,
)
from wtforms.validators import (
    DataRequired,  # Require data to be in that filed.
    ValidationError,  # Raise Validation error if things go bad.
    Email,  # Require data to be considered email.
    EqualTo,  # Require the data to equal to another field.
    Length,
)
from app.models import Entry, User
from pathlib import Path


def path_exist_check(form, field):
    if not Path(field.data).exists():
        raise ValidationError(
            f"Path provided: {field.data} does not exist or does not have permission to access!"
        )


class DTConfigForm(FlaskForm):
    """
    This is the main form where bulk of the data for the clinical inforamtion are entered
    """

    LORISurl = StringField("LORIS URL")
    LORISusername = StringField(
        "LORIS Username for your location",
        validators=[DataRequired("LORIS Username obtained from CNBP")],
    )
    LORISpassword = StringField(
        "LORIS Password of the Username",
        validators=[
            DataRequired("LORIS Password you set for your CNBP LORIS password.")
        ],
    )
    timepoint_prefix = StringField(
        "Prefix for the Timepoint",
        validators=[
            DataRequired("Timepoint prefix used to distinguish the various."),
            Length(min=1, max=1),
        ],
    )
    institutionID = StringField(
        "ID of the institution",
        validators=[
            DataRequired("Three Letter string represent the local institintion."),
            Length(min=3, max=3),
        ],
    )
    institutionName = StringField("Full name of the institution")
    projectID_dic = StringField("Dictionary of list of ProjectIDs")
    LocalDatabasePath = StringField(
        "Path to the Local Database",
        validators=[DataRequired("Path to the local database."), path_exist_check],
    )
    LogPath = StringField(
        "Path to Log",
        validators=[DataRequired("Path to the log folder."), path_exist_check],
    )
    ZipPath = StringField(
        "Path to Zip files temporary storage. ",
        validators=[
            DataRequired("Path to the zip folder where files are unzipped"),
            path_exist_check,
        ],
    )
    DevOrthancIP = StringField("IP address of the Development Orthanc")
    DevOrthancUser = StringField("User name of the Development Orthanc")
    DevOrthancPassword = StringField("Password of of the Development Orthanc")
    ProdOrthancIP = StringField(
        "IP of of the Production Orthanc",
        validators=[DataRequired("Accessing the production Orthanc IP address")],
    )
    ProdOrthancUser = StringField(
        "User name of the Lpregjycrb Orthanc",
        validators=[DataRequired("User name of the production Orthanc deployed.")],
    )
    ProdOrthancPassword = StringField(
        "Password of the Production Orthanc",
        validators=[DataRequired("Password of the production orthanc deloyed.")],
    )

    """
    Make sure to update the validator fields below should you change or rename anything here! 
    Note that these while similar but are not the same thing as the database fileds. 
    """

    def validate_path(self, path_input: Field):

        if Path(path_input.data).exists():
            return True
        else:
            return False


class NeonatalDataForm_Submit(DTConfigForm):
    """
    This is an extended class of the base form. This is for the submission purpsoe.
    """

    submit_entry = SubmitField("Submit")


class NeonatalDataForm_Update(DTConfigForm):
    """
    This is an extended class of the base form. This is for the update and deletion purpsoe.
    """

    update_entry = SubmitField("Update")

    confirm_delete = BooleanField("Confirm Delete?")
    confirm_double_delete = BooleanField("Really, I double confirm Delete?")
    delete_entry = SubmitField("!!!Delete!!!")
