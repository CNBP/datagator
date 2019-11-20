import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()

# we'll add classes here

# creates a create_engine instance at the bottom of the file
engine = create_engine("sqlite:///books-collection.db")

Base.metadata.create_all(engine)
from datetime import datetime


class dicom_transit_config(Base):
    """
    This is used to model the configuration entry from the user regarding DICOMTransit Operation.
    """

    __tablename__ = "dicom_transit_config"
    # Get the encryption key from the env.

    # Inspired from: https://stackoverflow.com/questions/49560609/sqlalchemy-encrypt-a-column-without-automatically-decrypting-upon-retrieval
    id = Column(Integer, primary_key=True)  # hidden
    LORISurl = Column(String)
    LORISusername = Column(String)
    LORISpassword = Column(String)

    timepoint_prefix = Column(String)
    institutionID = Column(String)
    institutionName = Column(String)
    projectID_dic = Column(String)
    LocalDatabasePath = Column(String)
    LogPath = Column(String)
    ZipPath = Column(String)
    DevOrthancIP = Column(String)

    DevOrthancUser = Column(String)
    DevOrthancPassword = Column(String)

    ProdOrthancIP = Column(String)
    ProdOrthancUser = Column(String)
    ProdOrthancPassword = Column(String)

    timestamp = Column(DateTime, index=True, default=datetime.utcnow)  # hidden

    user_id = Column(
        Integer, ForeignKey("user.id")
    )  # used to associate who entered this entry. # hidden

    def __repr__(self):
        return f"<DICOMTransitConfig {self.id} by {self.user_id} on {self.timestamp}>"
