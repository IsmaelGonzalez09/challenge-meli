
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

Create the BD named "mysql_db_1":
```sql
CREATE DATABASE mysql_db_1;
```

Select the DB:
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

## Create MySQL BD to save the results

Create the BD named "persistent_data_db":
```sql
CREATE DATABASE persistent_data_db;
```

Select the DB:
 ```sql
USE persistent_data_db;
```

Create the Tables:
```sql
CREATE TABLE IF NOT EXISTS classification (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  result JSON DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS connections (
  id VARCHAR(36) NOT NULL PRIMARY KEY,
  host VARCHAR(255) NOT NULL,
  port INT NOT NULL,
  user VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  data_base VARCHAR(255) NOT NULL
);
```

# API Documentation

Run this command line to start the app with your endpoints:
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

## Persistence Endpoint

This Endpoint request the conexion data for the DB to scan (mysql_db_1). Then, this data is saved in our DB "persistent_data_db", encrypting the password, saving this data in our table "connections" and responding with status code 201:

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/0e58e4b6-d419-4b21-a349-6432ee743209)

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/ae04216b-8479-441f-8847-7e3966b3967d)


![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/b87182fb-327f-4c02-99b4-4f096b44baad)

## Post Scan Endpoint

This Endpoint request the ID generated in the previous response and classificate the data according to this dictionary using Regex:
```
{
    "username": "USERNAME",
    "mail": "EMAIL_ADDRESS",
    "credit": "CREDIT_CARD_NUMBER"
}
```
Then, this endpoint save the results in the table "classification" in our DB "persistent_data_db":

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/cda2679e-c658-4e1e-8e82-5396ec710664)

## Get Scan Endpoint

The results can be seen with this endpoint. In this case, I add one table more named "Shipments" with additional information for to be classificated:

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/781bfbda-0918-4ace-b8e0-9cb5a7045091)
![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/db054b9e-c055-4f07-92f1-c880ae0c828f)

In case that some ID not to be found, the API send the error message according to code error:

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/173e5839-779c-4174-a95b-975ea0582d13)

## Get HTML Endpoint

Finally, this endpoint for show the tables classificated with HTML format:

![image](https://github.com/IsmaelGonzalez09/challenge-meli/assets/46968561/85922be1-65cd-4bc2-82cc-a86b7123eae0)

