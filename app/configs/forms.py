from datetime import date, datetime, timedelta
import sys
from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    FloatField,
    DateField,
    TimeField,
    SelectMultipleField,
    SubmitField,
    ValidationError,
    BooleanField,
)
from wtforms.validators import DataRequired
from app.models import Entry, User


class DTConfigForm(FlaskForm):
    """
    This is the main form where bulk of the data for the clinical inforamtion are entered
    """

    LORISurl = StringField("LORIS URL")
    LORISusername = StringField(
        "LORIS Username for your location",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    LORISpassword = StringField(
        "LORIS Password of the Username",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    timepoint_prefix = StringField(
        "Prefix for the Timepoint",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    institutionID = StringField(
        "ID of the institution", validators=[DataRequired("Birth weight is mandatory.")]
    )
    institutionName = StringField("Name of the institution")
    projectID_dic = StringField("Dictionary of list of PrrojectIDs")
    LocalDatabasePath = StringField(
        "Path to the Local Database",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    LogPath = StringField(
        "Path to Log", validators=[DataRequired("Birth weight is mandatory.")]
    )
    ZipPath = StringField(
        "Path to Zip files temporary storage. ",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    DevOrthancIP = StringField("IP address of the Development Orthanc")
    DevOrthancUser = StringField("User name of the Development Orthanc")
    DevOrthancPassword = StringField("Password of of the Development Orthanc")
    ProdOrthancIP = StringField(
        "IP of of the Production Orthanc",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    ProdOrthancUser = StringField(
        "User name of the Lpregjycrb Orthanc",
        validators=[DataRequired("Birth weight is mandatory.")],
    )
    ProdOrthancPassword = StringField(
        "Password of the Production Orthanc",
        validators=[DataRequired("Birth weight is mandatory.")],
    )

    """
    Make sure to update the validator fields below should you change or rename anything here! 
    Note that these while similar but are not the same thing as the database fileds. 
    """

    def validate_MRN(self, MRN):
        """
        Validate the MRN field to ensure it is not too big or negative.
        :param MRN:
        """
        if MRN.data > 9999999:
            raise ValidationError("MRN number must be 7 digits")
        elif MRN.data < 0:
            raise ValidationError("MRN number cannot be negative")

    def validate_birth_weight(self, birth_weight):
        """
        Validate birth weight to ensure it is not TOO high or negative.
        :param birth_weight:
        :return:
        """
        if birth_weight.data > 2500:
            raise ValidationError("Birth weight too high (>30LB?!)")
        elif birth_weight.data < 0:
            raise ValidationError("Birth weight cannot be negative")

    def validate_mri_age(self, mri_age):
        """
        Validate the MRI age to ensure it is not too old and not too young
        :param mri_age:
        :return:
        """

        if mri_age.data < 20:
            raise ValidationError(
                "Gestational age is less than 20 weeks old? Are you sure? "
            )
        elif mri_age.data > 5 * 52:
            raise ValidationError(
                "Gestational age is more than 5 YEARS old? Are you sure? "
            )

    def validate_birth_date(self, birth_date):
        """
        Validate the birth date to ensure that it is not in the future not too recent and not too far in the past.
        :param birth_date:
        :return:
        """

        # assum
        birthday = birth_date.data

        # Youngest preemie is at least 23 weeks old. You cannot be younger than that and expect to be scanned?
        birth_date_latest_possible = datetime.now() - timedelta(
            hours=23 * 7 * 24  # 23 weeks each, 7 days per week 24 hours per day.
        )

        birth_date_earliest_possible = datetime.now() - timedelta(
            hours=75
            * 52
            * 7
            * 24  # 75 years, 52 weeks each, 7 da12ys per week 24 hours per day.
        )

        if birthday >= datetime.now().date():
            raise ValidationError("Birth is in the future? Are you sure? ")
        elif birthday < birth_date_earliest_possible.date():
            raise ValidationError(
                "Based on Birthday, the age is more than 75 YEARS old? Are you sure? "
            )
        elif birthday > birth_date_latest_possible.date():
            raise ValidationError(
                "Based on Birthday, the age is younger than 23 weeks old? Are you sure? "
            )

    def validate_mri_date(self, birth_date):
        """
        Check the MRI date to ensure it is not too far
        :param birth_date:
        :param mri_date:
        :return:
        """
        mri_date_iso = self.mri_date.data
        age = mri_date_iso - birth_date.data
        weeks = age.days / 7

        if mri_date_iso > datetime.now().date():
            raise ValidationError(
                "You will scan this subject is in the future? Are you sure? "
            )
        elif weeks < -36:
            raise ValidationError("MRI age is less than 20 weeks old? Are you sure? ")
        elif weeks > 52 * 25:
            raise ValidationError("MRI age is more than 25 YEARS old? Are you sure? ")


class NeonatalDataForm_Submit(NeonatalDataFormMixins):
    """
    This is an extended class of the base form. This is for the submission purpsoe.
    """

    submit_entry = SubmitField("Submit")


class NeonatalDataForm_Update(NeonatalDataFormMixins):
    """
    This is an extended class of the base form. This is for the update and deletion purpsoe.
    """

    update_entry = SubmitField("Update")

    confirm_delete = BooleanField("Confirm Delete?")
    confirm_double_delete = BooleanField("Really, I double confirm Delete?")
    delete_entry = SubmitField("!!!Delete!!!")
