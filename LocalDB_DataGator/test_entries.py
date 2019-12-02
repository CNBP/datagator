import unittest


class UT_LocalDB_DataGator_Entries(unittest.TestCase):
    def test_prepare_entries(self):
        from LocalDB_DataGator.entries import get_entries_CNBPID, jsonify_entry

        # Get Entries.
        a = get_entries_CNBPID("VXF12345")

        # Jsonify the entry for upload.
        jsonify_entry(a)

        return True
