import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

path_DataGator = Path(os.path.abspath(os.path.dirname(__file__)))
path_DICOMTransit = path_DataGator.parent


def get_DataGator_DataBaseURI():
    """
    A dedicated way to get database URI regardless if Travis or not.
    :return:
    """
    if "TRAVIS" in os.environ:
        URI = "sqlite:///" + os.path.join(path_DataGator, "app.db")
    else:  # not on travis and not standalone, hence should defer to DICOMTransit .env settings.
        # Load .env from DICOMTransit path.
        load_dotenv(path_DICOMTransit / ".env")
        if "datagator_database" in os.environ:
            # Get the path of the database URL from the environment.
            SQLALCHEMY_DATABASE_URI = f"sqlite:///" + os.environ.get(
                "datagator_database"
            )
        else:
            SQLALCHEMY_DATABASE_URI = f"sqlite:///" + os.path.join(
                path_DataGator, "app.db"
            )

        # Get the path of the database URL from the environment.
        # URI = "sqlite:///" + os.environ.get("datagator_database")
    return SQLALCHEMY_DATABASE_URI


class Config(object):
    """
    This class stores the configurations loaded from the environment. 
    """

    load_dotenv(find_dotenv())

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    SQLALCHEMY_DATABASE_URI = get_DataGator_DataBaseURI()

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["it@cnbp.ca"]
    POSTS_PER_PAGE = 5
    LANGUAGE = ["en-CA", "fr-CA"]
    LOG_TO_STDOUT = True
