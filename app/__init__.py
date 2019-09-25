from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)

logger = logging.getLogger()

# Load configuration from the object class.
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
# Instnatiate the LoginManager for this current app.
login = LoginManager(app)

# The page to direct people to login if they are required.
login.login_view = "login"

from app import routes, models, errors

if not app.debug:

    if app.config["MAIL_SERVER"]:
        logger.debug(
            "App is currently in production mode and a mail server has been set!"
        )
        auth = None
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSSWORD"])
            logger.debug("obtained credential!")
        secure = None
        if app.config["MAIL_USE_TLS"]:
            secure = ()
            logger.debug("using TLS!")
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-replay@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"],
            subject="Microblog Failure",
            credentials=auth,
            secure=secure,
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        logger.debug("Handler added!")

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/microblog.log", maxBytes=1024000, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Microblog is starting up!")


else:
    logger.debug("App is currently in debug mode and no email has been sent")
