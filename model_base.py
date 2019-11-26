from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
from config import get_DataGator_DataBaseURI
import os

load_dotenv()
app = Flask("DataGatorSQLAlchemyAccessor")

app.config["SQLALCHEMY_DATABASE_URI"] = get_DataGator_DataBaseURI()

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
datagator_db = SQLAlchemy(app)


class DICOMTransitConfig(datagator_db.Model):
    """
    This is used to model the configuration entry from the user regarding DICOMTransit Operation.
    """

    # Inspired from: https://stackoverflow.com/questions/49560609/sqlalchemy-encrypt-a-column-without-automatically-decrypting-upon-retrieval
    id = datagator_db.Column(datagator_db.Integer, primary_key=True)  # hidden
    LORISurl = datagator_db.Column(datagator_db.String)
    LORISusername = datagator_db.Column(datagator_db.String)
    LORISpassword = datagator_db.Column(datagator_db.String)

    timepoint_prefix = datagator_db.Column(datagator_db.String)
    institutionID = datagator_db.Column(datagator_db.String)
    institutionName = datagator_db.Column(datagator_db.String)
    projectID_dic = datagator_db.Column(datagator_db.String)
    LocalDatabasePath = datagator_db.Column(datagator_db.String)
    LogPath = datagator_db.Column(datagator_db.String)
    ZipPath = datagator_db.Column(datagator_db.String)
    DevOrthancIP = datagator_db.Column(datagator_db.String)

    DevOrthancUser = datagator_db.Column(datagator_db.String)
    DevOrthancPassword = datagator_db.Column(datagator_db.String)

    ProdOrthancIP = datagator_db.Column(datagator_db.String)
    ProdOrthancUser = datagator_db.Column(datagator_db.String)
    ProdOrthancPassword = datagator_db.Column(datagator_db.String)

    timestamp = datagator_db.Column(
        datagator_db.DateTime, index=True, default=datetime.utcnow
    )  # hidden

    user_id = datagator_db.Column(
        datagator_db.Integer, datagator_db.ForeignKey("user.id")
    )  # used to associate who entered this entry. # hidden


class Entry(datagator_db.Model):
    """
    This is used to model the data entry from the user regarding the scans.
    """

    id = datagator_db.Column(datagator_db.Integer, primary_key=True)
    MRN = datagator_db.Column(datagator_db.Integer)
    CNBPID = datagator_db.Column(datagator_db.String(10))
    birth_weight = datagator_db.Column(datagator_db.String(140))
    birth_date = datagator_db.Column(datagator_db.Date)
    birth_time = datagator_db.Column(datagator_db.Time)
    mri_date = datagator_db.Column(datagator_db.Date)
    mri_reason = datagator_db.Column(datagator_db.String)
    # Many more fields to add here.
    mri_dx = datagator_db.Column(datagator_db.String)  # JSON string
    dicharge_diagoses = datagator_db.Column(datagator_db.String)
    mri_age = datagator_db.Column(datagator_db.String)
    timestamp = datagator_db.Column(
        datagator_db.DateTime, index=True, default=datetime.utcnow
    )
    user_id = datagator_db.Column(
        datagator_db.Integer, datagator_db.ForeignKey("user.id")
    )  # used to associate who entered this entry.
