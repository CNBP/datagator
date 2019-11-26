from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,  # used to hide LORIS and Orthanc password fields from view.
    SubmitField,
    BooleanField,
    IntegerField,
    Field,
)

from wtforms.validators import (
    DataRequired,  # Require data to be in that filed.
    ValidationError,  # Raise Validation error if things go bad.
    Length,
)
from pathlib import Path


def path_exist_check(form, field):
    """
    A generic verification function where the first
    :param form:
    :param field:
    :return:
    """
    try:
        path_exist = Path(field.data).exists()
    except OSError:
        raise ValidationError(
            f"Path provided: {field.data} has incompatible format. Ensure the path actuall exist."
        )
    except:
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
    LORISpassword = PasswordField(
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
    DevOrthancPassword = PasswordField("Password of of the Development Orthanc")
    ProdOrthancIP = StringField(
        "IP of of the Production Orthanc",
        validators=[DataRequired("Accessing the production Orthanc IP address")],
    )
    ProdOrthancUser = StringField(
        "User name of the Production Orthanc",
        validators=[DataRequired("User name of the production Orthanc deployed.")],
    )
    ProdOrthancPassword = PasswordField(
        "Password of the Production Orthanc",
        validators=[DataRequired("Password of the production Orthanc deloyed.")],
    )

    CNFUN_CONNECTION_STRING = StringField(
        "Connection String to connect to the local CNFUN database. In the format of, Driver=;XYZ, DBQ=XYZ;, PWD=XYZ;, CHARSET=XYZ;"
    )
    CNN_CONNECTION_STRING = StringField(
        "Connection String to connect to the local CNN database. In the format of, Driver=XYZ;, DBQ=XYZ;, PWD=XYZ;, CHARSET=XYZ;"
    )

    COUCHDB_EXPORT_ENABLED = BooleanField("")
    COUCHDB_EXPORT_DATABASE = StringField("")
    COUCHDB_EXPORT_HOST = StringField("")
    COUCHDB_EXPORT_PORT = StringField("")
    COUCHDB_EXPORT_USER = StringField("")
    COUCHDB_EXPORT_PASSWORD = PasswordField("")

    MYSQL_EXPORT_ENABLED = BooleanField("")
    MYSQL_EXPORT_DATABASE = StringField("")
    MYSQL_EXPORT_HOST = StringField("")
    MYSQL_EXPORT_PORT = StringField("")
    MYSQL_EXPORT_USER = StringField("")
    MYSQL_EXPORT_PASSWORD = PasswordField("")

    NUMBER_OF_RECORDS_PER_BATCH = StringField("")

    REDCAP_API_URL = StringField("")
    REDCAP_EXPORT_ENABLED = BooleanField("")

    REDCAP_TOKEN_CNFUN_PATIENT = PasswordField("")
    REDCAP_TOKEN_CNN_ADMISSION = PasswordField("")
    REDCAP_TOKEN_CNN_BABY = PasswordField("")
    REDCAP_TOKEN_CNN_MASTER = PasswordField("")
    REDCAP_TOKEN_CNN_MOTHER = PasswordField("")

    USE_LOCAL_HOSPITAL_RECORD_NUMBERS_LIST = BooleanField("")

    """
    Make sure to update the validator fields below should you change or rename anything here! 
    Note that these while similar but are not the same thing as the database fileds. 
    """

    def validate_path(self, path_input: Field):
        return Path(path_input.data).exists()


class DTConfigForm_Submit(DTConfigForm):
    """
    This is an extended class of the base form. This is for the submission purpsoe.
    """

    submit_entry = SubmitField("Submit")


class DTConfigForm_Update(DTConfigForm):
    """
    This is an extended class of the base form. This is for the update and deletion purpsoe.
    """

    update_entry = SubmitField("Update")

    confirm_delete = BooleanField("Confirm Delete?")
    confirm_double_delete = BooleanField("Really, I double confirm Delete?")
    delete_entry = SubmitField("!!!Delete!!!")
