import mysql.connector
import json
import random
import datetime
from sendEmail import emailTo
from profile_data import ProfileData

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
    user_id = -1
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT ID,password FROM accounts a WHERE a.email = '{email}';")
    dbResult = cur.fetchone()
    cur.close()

    # verify password hashes match
    access_granted = False
    if dbResult != None and dbResult[1] == password:
        access_granted = True
        user_id = dbResult[0]

    response = { "response": access_granted, "userID": user_id }
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

    #method from the sendEmail file is called to send a link to the user, who is signing up into the website
    # print(email)
    # emailTo(email, fname, lname)

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
    post_id = None
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO messages(author, date, message) VALUES({user_id}, NOW(), '{message}');")
    post_id = mysql.connection.insert_id()
    cur.execute(f"INSERT INTO posts(post_id, group_id) VALUES({post_id}, 1);") # use default group for general posts
    mysql.connection.commit()
    cur.close()
    return {
        "postID": post_id
    }


def get_posts(mysql, amount, user_id=-1):
    response = []
    cur = mysql.connection.cursor()
    if user_id != -1: # -1 indicates no user specified
        cur.execute(f"SELECT * FROM messages WHERE author={user_id} ORDER BY date DESC LIMIT {amount};")
    else:
        cur.execute(f"SELECT * FROM messages ORDER BY date DESC LIMIT {amount};")

    for message in cur.fetchall():
        response.append({
            "postID": message[0],
            "author": message[1],
            "timestamp": int(message[2].timestamp()),
            "message": message[3]
        })

    cur.close()
    return response


def comment(mysql, parent_post_id, user_id, message):
    response = {"response": False}
    comment_id = create_post(mysql, user_id, message)["postID"]
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO comments(post_id, parent_host) VALUES({comment_id}, {parent_post_id});")
    mysql.connection.commit()
    response["response"] = True
    cur.close()
    return response


def get_comments(mysql, post_id):
    response = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM messages m WHERE m.post_id IN (SELECT post_id FROM comments c WHERE c.parent_host={post_id});")
    for comment in cur.fetchall():
        response.append({
            "postID": comment[0],
            "author": comment[1],
            "timestamp": int(comment[2].timestamp()),
            "message": comment[3]
        })

    cur.close()
    return response


def get_image(mysql, path):
    response = {"retrieved": False, "image": "null"}
    with open("images/" + path, "r") as file:
        image_data = file.read()
        response["image"] = image_data
        response["retrieved"] = True
        
    return response


def generate_image_path():
    return create_unique_id()

def store_image(mysql, image, path):
    response = {"response": False, "path": "null"}

    if path == "null":
        path = generate_image_path()
        response["path"] = path

    with open("images/" + path, "w") as file:
        file.write(image)
        response["response"] = True
        response["path"] = path

    return response

def get_about_me(mysql,user_id):
    response = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT p.about FROM users u INNER JOIN profile p ON u.pathURL = p.pathURL WHERE u.userID = {user_id};")
    for aboutMe in cur.fetchall():
        response.append({
            "about": aboutMe[0]
        })

    cur.close()
    return response

def create_about(mysql,user_id,message):
    response = {"response": False}
    
    # get users path url
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT pathURL FROM users WHERE userID={user_id};")
    data = cur.fetchone()
    # if path url was found
    if data:
        path_url = data[0] #extract path_url from raw data
        cur.execute(f"SELECT * FROM profile WHERE pathURL='{path_url}';")
        # udpate if exists, insert otherwise
        if cur.fetchone():
            cur.execute(f"UPDATE profile SET about='{message}' WHERE pathURL='{path_url}';")
        else:
            cur.execute(f"INSERT INTO profile(pathURL, about) VALUES('{path_url}', '{message}');")

        mysql.connection.commit()
        response["response"] = True
    
    cur.close()
    return response

def like_unlike_post(mysql, user_id, post_id):
    response = {"response": False}

    cur = mysql.connection.cursor()
    
    cur.execute(f"SELECT * FROM posts WHERE post_id={post_id};")
    data = cur.fetchone()
    
    #Checks to see if it exists or not within the database
    if data:
        #Since it exists, we are going to "Unlike" the post
        cur.execute(f"DELETE FROM userLikes WHERE post_id = {post_id} AND user_id = {user_id};")
        response["response"] = True
    else:
        #Post hasn't been liked by user, so we create an entry into the database for it
        cur.execute(f"INSERT INTO userLikes(user_id,post_id) VALUES ({user_id},{post_id});")
        response["response"] = True

    mysql.connection.commit()
    
    cur.close()
    return response

def get_likes(mysql,post_id):
    response = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) FROM userLikes WHERE post_id = {post_id};")
    for likes in cur.fetchall():
        response.append({
            "likes": likes[0]
        })

    cur.close()
    return response


# needs profile database table to be made before use
# will need to be updated 
def update_profile(mysql, user_id, profile):
    query_head = "UPDATE profiles SET "
    query_tail = f"WHERE userID={user_id};"
    columns = []
    if profile.fname:
        columns.append(f"fname='{profile.fname}' ")
    if profile.lname:
        columns.append(f"lname='{profile.lname}' ")
    if profile.major:
        columns.append(f"major='{profile.major}' ")
    if profile.year:
        columns.append(f"year={profile.year} ")
    if profile.gender:
        columns.append(f"gender='{profile.gender}' ")
    if profile.interests:
        columns.append(f"interests='{profile.interests}' ")

    query = query_head
    for column in columns:
        query += column
    query += query_tail
    print(query)

    if len(columns) != 0:
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return {"response": True}
    else:
        return {"response": False}


def get_profile(mysql, path_url):
    response = {}
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM profile WHERE pathURL='{path_url}';")
    data = cur.fetchone()
    cur.close()
    if data:
        response["pathURL"] = path_url
        response["grade"] = data[1]
        response["gender"] = data[2]
        response["about"] = data[3]
        response["profilePic"] = data[4]
        response["coverPic"] = data[5]
        return response
    else:
        print("Error in get_profile: no profile found")


if __name__ == "__main__":
    #insert test driver code
    get_image("", "test")
    profile = ProfileData()
    profile.set_first_name("Mike")
    profile.set_interests("Skateboarding")
    update_profile("", 9, profile)


def test(mysql):
    pass
