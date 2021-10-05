import mysql.connector
import json

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

dbCredentialsFile.close() #close file

# Connect to remote database
db = mysql.connector.connect(
	host = dbHost,
	user = dbUsername,
	passwd = dbPassword,
	database = dbDatabase
)


def fetchTables():
    # Cursor is used to interact with the database
    cur = db.cursor()
    cur.execute("SHOW TABLES;")
    dbResult = cur.fetchall() 
    cur.close()

    # data format: [("Table1",), ("Table2",)]
    tables = { "tables": []}
    for table in dbResult:
        tables["tables"].append(table[0]) # add table name to dictionary

    return json.loads(json.dumps(tables)) # dump and load removes double quotes

if __name__ == "__main__":
    print(fetchTables())