import mysql.connector

dbCredentialsFile = open("credentials.txt","r")
dbHost = None
dbUsername = None
dbPassword = None
dbDatabase = None
for line in dbCredentialsFile.readlines():
    line = line.split("=")
    for i in range(0, len(line)):
        line[i] = line[i].strip()
        
    if line[0] == "host":
        dbHost = line[1]
    elif line[0] == "user":
        dbUsername = line[1]
    elif line[0] == "passwd":
        dbPassword = line[1]
    elif line[0] == "database":
        dbDatabase = line[1]

dbCredentialsFile.close()

db = mysql.connector.connect(
	host = dbHost,
	user = dbUsername,
	passwd = dbPassword,
	database = dbDatabase
)

cur = db.cursor()
cur.execute("SHOW TABLES")
print(cur.fetchall())
input()