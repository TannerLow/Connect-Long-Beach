import mysql.connector
import json
import random
import datetime

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


#helper function
def create_unique_id():
    unique_id = ""
    for _ in range(10):
        x = random.randint(0,35)
        if x < 10:
            unique_id += str(x)
        else:
            unique_id += chr(x + ord('a') - 10)

    return unique_id


def generate_unique_id(mysql):
    uid = create_unique_id()
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT pathUrl FROM users u WHERE u.pathUrl='{uid}';")
    while cur.fetchone():
        uid = create_unique_id()
        cur.execute(f"SELECT pathUrl FROM users u WHERE u.pathUrl='{uid}';")
    cur.close()
    return uid


def monthToInt(month):
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    return months.index(month) + 1


def register(mysql, email, password, fname, lname, gender, month, day, year):
    # Fail if email already in use
    if is_email_in_use(mysql, email)["response"]:
        return {"response": False}

    monthInt = monthToInt(month)
    bday = datetime.datetime(int(year), monthInt, int(day)).strftime('%Y-%m-%d %H:%M:%S')
    pathUrl = generate_unique_id(mysql)
    
    # create entry in accounts
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO accounts(email, password) VALUES('{email}', '{password}');")
    mysql.connection.commit()
    cur.close()

    # create entry in users
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT ID FROM accounts WHERE email='{email}';")
    id = cur.fetchone()[0]
    print(id)
    cur.execute(f"INSERT INTO users(userID, fname, lname, gender, pathUrl, bday) VALUES('{id}', '{fname}', '{lname}', '{gender}', '{pathUrl}', '{bday}');")
    mysql.connection.commit()
    cur.close()
    return {"response": True}


def create_post(mysql, user_id, message):
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO messages(author, date, message) values({user_id}, NOW(), '{message}');")
    mysql.connection.commit()
    cur.close()
    

if __name__ == "__main__":
    #insert test driver code
    create_post("", 0, "hello")


def test(mysql):
    create_post(mysql, 22, "This is a test message. Working on posts.")
