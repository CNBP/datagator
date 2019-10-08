from datetime import date, datetime, timedelta

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

choics_diagnoses = [
    ("d0", "No Diagnoses, Healthy."),
    ("d1", "ABO incompatibility"),
    ("d2", "Anemia"),
    ("d3", "Apnea"),
    ("d4", "Asphxia"),
    ("d5", "Aspiration"),
    ("d6", "Bradycardia"),
    ("d7", "Breathing problesm"),
    ("d8", "Bronchopulmonary dysplastia"),
    ("d9", "Cerebral palsy"),
    ("d10", "Coarctation of the aorta"),
    ("d11", "Cyanosis"),
    ("d12", "Desaturation"),
    ("d13", "Feeding difficutlies"),
    ("d14", "Gastrostomy tube"),
    ("d15", "Heart failure"),
    ("d16", "Heart murmur"),
    ("d17", "Heart valve abnormalities"),
    ("d18", "Hernia/Hydrocele"),
    ("d19", "Hypoglycemia"),
    ("d20", "Hypotension"),
    ("d21", "Hypothermia"),
    ("d22", "Hypertension"),
    ("d23", "Intrauterine growth retardation "),
    ("d24", "Intraventricular hemorrhage"),
    ("d25", "Jaundice"),
    ("d26", "Laryngomalacia"),
    ("d27", "Necrotizing enterocolitis"),
    ("d28", "Patent ductus arteriosus"),
    ("d29", "Periodic breathing"),
    ("d30", "Periventricular leukomalacia"),
    ("d31", "Persistent pulmonary hypertehsion of the newborn"),
    ("d32", "Pneumonia"),
    ("d33", "Pneumothorax"),
    ("d34", "Polycythemia"),
    ("d35", "Reflux"),
    ("d36", "Repiratory distress syndrome"),
    ("d37", "Retinopathy of prematurity"),
    ("d38", "Retraction"),
    ("d39", "Rh incompatibility"),
    ("d40", "Seizures"),
    ("d41", "Sepsis"),
    ("d42", "Septal defect"),
    ("d43", "Tetralogy of Fallot"),
    ("d44", "Transposition of the great arteries"),
]


class RequestEntryForm(FlaskForm):
    """
    This is used to request a particular entry.
    """

    id = IntegerField("Entry ID:", validators=[DataRequired()])

    submit = SubmitField("Load Entry")

    def __init__(self, current_username, *args, **kwargs):
        # At the time of initialization
        super(RequestEntryForm, self).__init__(*args, **kwargs)

        # Store the input into class variable.
        self.username = current_username

    def validate_id(self, id):
        """
        Validation function to ensure such entries exist.
        :param username:
        :return:
        """
        entries_desired = Entry.query.filter_by(id=id.data)

        # check the database to see if such user name already exist
        entry = entries_desired.scalar() is not None
        # Entry does not exist!
        if not entry:
            raise ValidationError(
                "No loadable records were found. Maybe it did not exist OR you do not have permission to view it?"
            )

        # Check the current user name ID, validate it against the creation ID.
        user_current = User.query.filter_by(username=self.username).first_or_500()
        # Check if they are the same
        if entries_desired.first().user_id != user_current.id:
            raise ValidationError(
                "No loadable records were found! Maybe it did not exist OR you do not have permission to view it."
            )


class NeonatalDataFormMixins(FlaskForm):
    """
    This is the main form where bulk of the data for the clinical inforamtion are entered
    """

    MRN = IntegerField(
        "MRN*", validators=[DataRequired("Medical Record number is mandatory!")]
    )
    CNBPID = StringField("CNBPID")
    birth_weight = FloatField(
        "Birth Weight* (lb)", validators=[DataRequired("Birth weight is mandatory.")]
    )

    birth_date = DateField(
        "Birth Date* (YYYY-MM-DD)",
        validators=[DataRequired("Birth date is mandatory.")],
        format="%Y-%m-%d",
        default=date.today(),
    )

    birth_time = TimeField("Birth Time(HH:MM) in 24h format.")

    mri_date = DateField(
        "MRI Date* (YYYY-MM-DD)",
        validators=[DataRequired("MRI scan date is mandatory.")],
        format="%Y-%m-%d",
        default=date.today(),
    )

    mri_reason = SelectMultipleField(
        "Reason for MRI* \n (Ctrl = multi-select, Shift = batch-select) ",
        validators=[DataRequired("A reason must be specified.")],
        choices=choics_diagnoses,
    )

    mri_age = FloatField("Gestation Age (weeks)")

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
        if birth_weight.data > 30:
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
            * 24  # 75 years, 52 weeks each, 7 days per week 24 hours per day.
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
