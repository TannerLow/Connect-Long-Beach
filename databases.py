import mysql.connector
import json

def initialize(app):
    # Read database credentials file to login to the database
    dbCredentialsFile = open("credentials.txt","r")
    dbHost = None
    dbUsername = None
    dbPassword = None
    dbDatabase = None

    # parse credentials file
    for line in dbCredentialsFile.readlines():
        line = line.split("=")
        for i in range(0, len(line)):
            line[i] = line[i].strip()
        
        #set credential variables
        if line[0] == "host":
            dbHost = line[1]
        elif line[0] == "user":
            dbUsername = line[1]
        elif line[0] == "passwd":
            dbPassword = line[1]
        elif line[0] == "database":
            dbDatabase = line[1]

    app.config['MYSQL_HOST'] = dbHost
    app.config['MYSQL_USER'] = dbUsername
    app.config['MYSQL_PASSWORD'] = dbPassword
    app.config['MYSQL_DB'] = dbDatabase
    dbCredentialsFile.close() #close file


def fetchTables(mysql):
    # Cursor is used to interact with the database
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES;")
    dbResult = cur.fetchall() 
    cur.close()

    # data format: [("Table1",), ("Table2",)]
    tables = { "tables": []}
    for table in dbResult:
        tables["tables"].append(table[0]) # add table name to dictionary

    return json.loads(json.dumps(tables)) # dump and load removes double quotes


def login(mysql, email, password):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT password FROM accounts a WHERE a.email = '{email}';")
    dbResult = cur.fetchone()
    cur.close()

    # verify password hashes match
    access_granted = False
    if dbResult != None and dbResult[0] == password:
        access_granted = True

    response = { "response": access_granted }
    return response


def is_email_in_use(mysql, email):
    cur = mysql.connection.cursor()
    email_in_use = False
    cur.execute(f"SELECT id FROM accounts a WHERE a.email = '{email}';")
    if cur.fetchone():
        email_in_use = True

    cur.close()
    return {"response": email_in_use}


def register(mysql, email, password, fname, lname, gender, path_url):
    # Fail if email already in use
    if is_email_in_use(mysql, email)["response"]:
        return {"response": False}

    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO accounts(email, password) VALUES('{email}', '{password}');")
    cur.execute(f"INSERT INTO users(userID, fname, lname, gender, pathUrl) VALUES(1, '{fname}', '{lname}', '{gender}', '{path_url}');")
    mysql.connection.commit()
    cur.close()
    return {"response": True}


def test(mysql):
    print(fetchTables(mysql))
    print(login(mysql, "fake_email@test.gov", "9285ab8def09c863d8a68824c31f4404f1cd004029d2af30e62576149d9a652c"))
    print(register(mysql, "another_fake@flylo.fm", "9285ab8def09c863d8a68824c31f4404f1cd004029d2af30e62576149d9a652d"))
    print(login(mysql, "another_fake@flylo.fm", "9285ab8def09c863d8a68824c31f4404f1cd004029d2af30e62576149d9a652d"))