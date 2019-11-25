import os
from dotenv import load_dotenv
from pathlib import Path

path_DataGator = Path(os.path.abspath(os.path.dirname(__file__)))
path_DICOMTransit = path_DataGator.parent


class Config(object):
    """
    This class stores the configurations loaded from the environment. 
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    if "TRAVIS" in os.environ:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(path_DataGator, "app.db")
    else:  # not on travis and not standalone, hence should defer to DICOMTransit .env settings.

        # Load .env from DICOMTransit path.
        load_dotenv(path_DICOMTransit / ".env")

        # Get the path of the database URL from the environment.
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.environ.get("datagator_database")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["it@cnbp.ca"]
    POSTS_PER_PAGE = 5
    LANGUAGE = ["en-CA", "fr-CA"]
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
