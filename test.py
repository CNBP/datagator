from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask("DataGatorSQLAlchemyAccessor")


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///C:\\GitHub\\DICOMTransit\\LocalDB\\datagator.sqlite"
datagator_database = SQLAlchemy(app)


class DICOMTransitConfig(datagator_database.Model):
    """
    This is used to model the configuration entry from the user regarding DICOMTransit Operation.
    """

    # Inspired from: https://stackoverflow.com/questions/49560609/sqlalchemy-encrypt-a-column-without-automatically-decrypting-upon-retrieval
    id = datagator_database.Column(
        datagator_database.Integer, primary_key=True
    )  # hidden
    LORISurl = datagator_database.Column(datagator_database.String)
    LORISusername = datagator_database.Column(datagator_database.String)
    LORISpassword = datagator_database.Column(datagator_database.String)

    timepoint_prefix = datagator_database.Column(datagator_database.String)
    institutionID = datagator_database.Column(datagator_database.String)
    institutionName = datagator_database.Column(datagator_database.String)
    projectID_dic = datagator_database.Column(datagator_database.String)
    LocalDatabasePath = datagator_database.Column(datagator_database.String)
    LogPath = datagator_database.Column(datagator_database.String)
    ZipPath = datagator_database.Column(datagator_database.String)
    DevOrthancIP = datagator_database.Column(datagator_database.String)

    DevOrthancUser = datagator_database.Column(datagator_database.String)
    DevOrthancPassword = datagator_database.Column(datagator_database.String)

    ProdOrthancIP = datagator_database.Column(datagator_database.String)
    ProdOrthancUser = datagator_database.Column(datagator_database.String)
    ProdOrthancPassword = datagator_database.Column(datagator_database.String)

    timestamp = datagator_database.Column(
        datagator_database.DateTime, index=True, default=datetime.utcnow
    )  # hidden

    user_id = datagator_database.Column(
        datagator_database.Integer, datagator_database.ForeignKey("user.id")
    )  # used to associate who entered this entry. # hidden

    def __repr__(self):
        return f"<DICOMTransitConfig {self.id} by {self.user_id} on {self.timestamp}>"
