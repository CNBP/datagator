import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel

from config import Config

app = Flask(__name__)

logger = logging.getLogger()

# Load configuration from the object class.
app.config.from_object(Config)

# Initialize the VARIOUS INSTANCES of PLUGINS by passing the app context to them
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
# The page to direct people to login if they are required.
login = LoginManager(app)  # Instnatiate the LoginManager for this current app.
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."

bootstrap = Bootstrap(app)

moment = Moment(app)
babel = Babel(app)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as erros_bp
    from app.auth import bp as auth_bp
    from app.entries import bp as entries_bp
    from app.main import bp as main_bp

    # Register blueprint
    app.register_blueprint(erros_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")  # extra name spacing.
    app.register_blueprint(entries_bp)  # extra name spacing.
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:

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

    return app


"""
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])
"""
from app import models
