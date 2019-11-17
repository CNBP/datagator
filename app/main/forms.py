from flask_wtf import FlaskForm
from wtforms import (
    StringField,  # regular string.
    SubmitField,  # HTML button element type
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,  # Require data to be in that filed.
    ValidationError,  # Raise Validation error if things go bad.
    Length,
)

from app.models import User

"""
This contains classes which represent a great variety of forms which collects or allow edit of a great variety of information.  
"""


class EditProfileForm(FlaskForm):
    """
    Specific form which allow people to submit the profile specific information. 
    """

    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def __init__(self, original_username, *args, **kwargs):

        # At the time of initialization
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # Store the self.original_username varaible with the initialized username variable.
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


class PostForm(FlaskForm):
    """
    This form is about Blog Posts
    """

    post = TextAreaField(
        "Say something nice!", validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField("Submit")
