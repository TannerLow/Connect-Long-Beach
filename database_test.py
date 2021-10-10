import mysql.connector

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

# Cursor is used to interact with the database
cur = db.cursor()

# Show all tables in database
cur.execute("SHOW TABLES;")
print(cur.fetchall())

# Create posts table if it doesn't already exist
cur.execute(
    "CREATE TABLE IF NOT EXISTS posts ("
    "post_id INT AUTO_INCREMENT PRIMARY KEY,"
    "message VARCHAR(255) NOT NULL);"
)

# Create comments table if it doesn't already exist, references posts
cur.execute(
    "CREATE TABLE IF NOT EXISTS comments ("
    "comment_id INT AUTO_INCREMENT PRIMARY KEY,"
    "post_id INT,"
    "message VARCHAR(255) NOT NULL,"
    "FOREIGN KEY (post_id) "
    "   REFERENCES posts (post_id) "
    "   ON DELETE CASCADE);"
)

# Lets the user enter strings to be inserted in the DB as "posts"
print("\nENTER done TO MOVE ON.\n")
while True:
    post = input("Enter a message to simulate writing a post to the database: ")
    if post == "done":
        break
    cur.execute("\nINSERT INTO posts (message) VALUES (%s);", (post,))

db.commit() #DB commit

# Display contents of posts table in the DB
cur.execute("SELECT * FROM posts;")
for post in cur.fetchall():
    print(post)

# Lets the user enter strings to be inserted in the DB as "comments"
print("\nENTER done TO MOVE ON\n")
while True:
    postID = input("Enter a post id you would like to comment on: ")
    if postID == "done":
        break
    comment = input("Enter a message to comment on the post: ")
    cur.execute("INSERT INTO comments (message, post_id) VALUES (%s, %s);", (comment, int(postID)))

db.commit() #DB commit

# Display contents of comments table in the DB
cur.execute("SELECT * FROM comments;")
for comment in cur.fetchall():
    print(comment)