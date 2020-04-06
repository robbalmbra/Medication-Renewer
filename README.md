# Medication-Renewer

## Info

Python script to renew medication from https://systmonline.tpp-uk.com, effectively can be used headlessly through a cronjob. Logs into webservice and tries to renew medication, returns if something went wrong.

## Usage

python ./Medication.py [USERNAME] [PASSWORD]

## Notes

Needs phantomjs to be installed and within the PATH variable to function correctly, use https://phantomjs.org/download.html to obtain the binary and supporting files.
