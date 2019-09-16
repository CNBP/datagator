from flask_wtf import FlaskForm
from wtforms import (
    StringField,  # regular string.
    PasswordField,  # password, hidden from view etc
    BooleanField,  #  Boolean f
    SubmitField,  # HTML button element type
)
from wtforms.validators import (
    DataRequired,  # Require data to be in that filed.
    ValidationError,  # Raise Validation error if things go bad.
    Email,  # Require data to be considered email.
    EqualTo,  # Require the data to equal to another field.
)


from app.models import User

# LoginForm class which the front end html document anticipates
class LoginForm(FlaskForm):
    """
    Login form class, used during login proces sonly. 
    """

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """
    Registration form class, for registration when no credential exist yet. 
    """

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    # Automaticly validate username field. valid_<field_name>
    def validate_username(self, username):
        """
        Check the username provided against the User name from the app.model, in the database.
        :param username:
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        """
        Check the email provided against the Email from the app.model, in the database.
        :param email:
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address")
