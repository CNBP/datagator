from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask("DataGatorSQLAlchemyAccessor")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getenv("datagator_database")
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

    def __repr__(self):
        return f"<DICOMTransitConfig {self.id} by {self.user_id} on {self.timestamp}>"
