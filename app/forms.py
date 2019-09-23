from flask_wtf import FlaskForm
from wtforms import (
    StringField,  # regular string.
    PasswordField,  # password, hidden from view etc
    BooleanField,  #  Boolean f
    SubmitField,  # HTML button element type
    IntegerField,
    DateField,
    TimeField,
    TextAreaField,
    MultipleFileField,
    DateTimeField,
)
from wtforms.validators import (
    DataRequired,  # Require data to be in that filed.
    ValidationError,  # Raise Validation error if things go bad.
    Email,  # Require data to be considered email.
    EqualTo,  # Require the data to equal to another field.
    Length,
)


from app.models import User

"""
This contains classes which represent a great variety of forms which collects or allow edit of a great variety of information.  
"""


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


class EditProfileForm(FlaskForm):
    """
    Specific form which allow people to submit the profile specific information. 
    """

    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """
        A custom validation method to check if the name already exist in the database.
        :param username:
        :return:
        """
        # If the entered username is not the same as the current one,
        if username.data != self.original_username:
            # check the database to see if such user name already exist
            user = User.query.filter_by(username=self.username.data).first()
            # If any exist, raise error.
            if user is not None:
                raise ValidationError("Please use a different username.")


class DataEntryForm(FlaskForm):
    """
    This is the main form where bulk of hte data for the clinical inforamtion are entered
    """

    MRN = IntegerField("MRN*", validators=[DataRequired()])

    CNBPID = StringField("CNBPID")
    birth_weight = IntegerField("Birth Weight*", validators=[DataRequired()])
    birth_date = DateField("Birth Date*", validators=[DataRequired()])
    birth_time = TimeField("Birth Time")
    mri_date = DateField("MRI Date*", validators=[DataRequired()])
    mri_reason = StringField("Reason for MRI")
    mri_age = IntegerField("Gestation Age (weeks)")


class PostForm(FlaskForm):
    """
    This form is about Blog Posts
    """

    post = TextAreaField(
        "Say something nice!", validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField("Submit")
