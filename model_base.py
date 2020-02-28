from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import URLType, EncryptedType
from datetime import datetime
from dotenv import load_dotenv
from config_datagator import get_DataGator_DataBaseURI

import sqlalchemy as sa

secret_key = "secretkey1234"
#from sqlalchemy_utils.types.encrypted.encrypted_type import FernetEngine

import os

load_dotenv()
app = Flask("DataGatorSQLAlchemyAccessor")

app.config["SQLALCHEMY_DATABASE_URI"] = get_DataGator_DataBaseURI()

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class DICOMTransitConfig(db.Model):
    """
    This is used to model the configuration entry from the user regarding DICOMTransit Operation.
    """

    # Inspired from: https://stackoverflow.com/questions/49560609/sqlalchemy-encrypt-a-column-without-automatically-decrypting-upon-retrieval
    id = db.Column(db.Integer, primary_key=True)  # hidden
    LORISurl = db.Column(URLType)
    LORISusername = db.Column(db.String)
    LORISpassword = db.Column(db.String)

    timepoint_prefix = db.Column(db.String)
    institutionID = db.Column(db.String)
    institutionName = db.Column(db.String)
    projectID_dic = db.Column(db.String)
    LocalDatabasePath = db.Column(db.String)
    LogPath = db.Column(db.String)
    ZipPath = db.Column(db.String)
    DevOrthancIP = db.Column(db.String)

    DevOrthancUser = db.Column(db.String)
    DevOrthancPassword = db.Column(db.String)

    ProdOrthancIP = db.Column(db.String)
    ProdOrthancUser = db.Column(db.String)
    ProdOrthancPassword = db.Column(db.String)

    # RedCap related data control.

    REDCAP_TOKEN_CNN_ADMISSION = db.Column(db.String)
    REDCAP_TOKEN_CNN_BABY = db.Column(db.String)
    REDCAP_TOKEN_CNN_MOTHER = db.Column(db.String)
    REDCAP_TOKEN_CNN_MASTER = db.Column(db.String)
    REDCAP_TOKEN_CNFUN_PATIENT = db.Column(db.String)
    REDCAP_API_URL = db.Column(db.String)

    CNN_CONNECTION_STRING = db.Column(db.String)
    CNFUN_CONNECTION_STRING = db.Column(db.String)

    USE_LOCAL_HOSPITAL_RECORD_NUMBERS_LIST = db.Column(db.Integer)

    NUMBER_OF_RECORDS_PER_BATCH = db.Column(db.Integer)

    # RedCap export related data control
    REDCAP_EXPORT_ENABLED = db.Column(db.Boolean)

    # MySQL
    MYSQL_EXPORT_ENABLED = db.Column(db.Boolean)
    MYSQL_EXPORT_HOST = db.Column(db.String)
    MYSQL_EXPORT_PORT = db.Column(db.Integer)
    MYSQL_EXPORT_DATABASE = db.Column(db.String)
    MYSQL_EXPORT_USER = db.Column(db.String)
    MYSQL_EXPORT_PASSWORD = db.Column(db.String)

    # CouchDB
    COUCHDB_EXPORT_ENABLED = db.Column(db.Boolean)
    COUCHDB_EXPORT_HOST = db.Column(db.String)
    COUCHDB_EXPORT_PORT = db.Column(db.Integer)
    COUCHDB_EXPORT_DATABASE = db.Column(db.String)
    COUCHDB_EXPORT_USER = db.Column(db.String)
    COUCHDB_EXPORT_PASSWORD = db.Column(db.String)

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # hidden

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # used to associate who entered this entry. # hidden


class Entry(db.Model):
    """
    This is used to model the data entry from the user regarding the scans.
    """

    id = db.Column(db.Integer, primary_key=True)
    MRN = db.Column(db.Integer)
    CNBPID = db.Column(db.String(10))
    birth_weight = db.Column(db.String(140))
    birth_date = db.Column(db.Date)
    birth_time = db.Column(db.Time)
    mri_date = db.Column(db.Date)
    mri_reason = db.Column(db.String)
    # Many more fields to add here.
    mri_dx = db.Column(db.String)  # JSON string
    dicharge_diagoses = db.Column(db.String)
    mri_age = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # used to associate who entered this entry.
