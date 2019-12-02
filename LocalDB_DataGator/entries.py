from datagator.app.models import Entry, db
from PythonUtils.PUJson import guarnteed_json_dump


def get_entries_MRN(MRN: int):
    """
    Acquire the Entry based on the MRN provided.
    :param MRN:
    :return:
    """
    entries = Entry.query.filter_by(MRN=MRN).order_by("timestamp").first()
    return entries


def set_entries_CNBPID(CNBPID: str, MRN: int):
    """
    Update LocalDB to forcibly overwrite the CNBPID informaiton as this informaiton is NOT obtained from the user in the first place.
    :param CNBPID:
    :param MRN:
    :return:
    """
    # Update entries of the MRN, to fill their CNBPID fields.
    entries = Entry.query.filter_by(MRN=MRN).update(dict(CNBPID=CNBPID))

    # Commit the action to the database.
    db.session.commit()


def get_entries_CNBPID(CNBPID: str):
    """
    Acquire the Entry based on the MRN provided.
    :param MRN:
    :return:
    """
    entries = Entry.query.filter_by(CNBPID=CNBPID).order_by("timestamp").first()
    return entries


def jsonify_entry(entry: Entry):
    """
    A way to convert the entry into the right format to be jsonified to be returned.

    :param entry:
    :return:
    """
    list_fields = get_entry_fields(entry)
    # Build Meta Dict
    Meta: dict = {
        "Instrument": "LocalMRIQuestionnaire",
        "Visit": "V1",
        "Candidate": 362950,
        "DDE": False,
    }

    # Build LocalMRIQUestionnarie Dict
    LocalMRIQuestionnaire: dict = {}

    # Fill the dictionary.
    for field in list_fields:
        LocalMRIQuestionnaire[field] = getattr(entry, field)

    return guarnteed_json_dump(
        {"Meta": Meta, "LocalMRIQuestionnaire": LocalMRIQuestionnaire}
    )


if __name__ == "__main__":
    a = get_entries_CNBPID("VXF12345")
    print(jsonify_entry(a))
