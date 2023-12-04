
# Challenge Meli - BD Classification

Objective.

Develop a REST API in Python or Golang that allows classification as indicated more
below, in principle, any MySQL database.
The classification of a relational database can be done based on the name of the database.
tables and/or columns, and/or by scanning a sample of the information contained in the
tables with a DLP.

This challenge was developed with the next tools:
- Windows Subsystem for Linux - Ubuntu
- MySQL
- Python 3.10
- FastAPI

The main file initializing the Endpoints developed in this practice:
- persistence: Endpoint for save the data connection of the BD to be scan. The passwords are saves encrypted.
- post_scan: Enpoint for search BD in MySQL, scan this BD and save in other BD in MySQL.
- get_scan: Get the data from scan of BD in the Endpoint "post_scan".
- get_html: Get in HTML.

## Create MySQL BD
