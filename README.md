# datagator

A simple Flask app that will collect data for LORIS

This is an internal facing app for the clinicians to enter additional data which are sent to CNBP loris to be centrally aggregated and validated. 

This happens pre-anonymization so post submission, a schedule anonymization and synchronization task against the main local database before submitting the data to the LORIS instrument data collector. 

### Credit: 
Most of the architecture of the module was designed based on the Mega Flask Tutorial by Miguel Grinberg. 
