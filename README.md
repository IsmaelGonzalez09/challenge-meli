
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
- Some libraries (added in requirements.txt)

Before to start, must to create a .env file to save the next environment variables:
```
PERSISTENT_DB_HOST=localhost
PERSISTENT_DB_PORT=3306
PERSISTENT_DB_USER=usermeli
PERSISTENT_DB_PASS=Test2023
PERSISTENT_DB_NAME=persistent_data_db
SECRET_KEY=kpje21xu4WpTYW0Mk9mB6-5nIh6sYP_i0KwT7L65er4=
```
This variables are to connect to the MySQL DB where will be save the results of scans.

## Create MySQL BD to be Scanned

To create the BD to be Scanned, after of config the MySQL in localhost, run the next queries:

- Create the BD named "mysql_db_1":
```sql
CREATE DATABASE mysql_db_1;
```

- Select the DB:
 ```sql
USE mysql_db_1;
```

Create the Table named USERS:
```sql
CREATE TABLE USERS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(255) NOT NULL,
    EMAIL_ADDRESS VARCHAR(255) NOT NULL,
    CREDIT_CARD_NUMBER VARCHAR(19) NOT NULL,
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Documentation

Run this command line to run the app with your endpoints:
```
uvicorn app.main:app --reload
```

Now, we can to try the connection with the app calling the first endpoint:

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/5ffc9cbd-095c-4455-afeb-073304dc121f)

To solve the challenge, the API has the next endopints, that were config in the main file:
- persistence: Endpoint for save the data connection of the BD to be scan. The passwords are saves encrypted.
- post_scan: Enpoint for search BD in MySQL, scan this BD and save in other BD in MySQL.
- get_scan: Get the data from scan of BD in the Endpoint "post_scan".
- get_html: Get in HTML.
