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
    path_url = "null"
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

    if access_granted:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT pathURL FROM users WHERE userID={user_id};")
        dbResult = cur.fetchone()
        cur.close()
        if dbResult:
            path_url = dbResult[0]

    response = { "response": access_granted, "userID": user_id, "pathURL": path_url }
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
    cur.execute(f"INSERT INTO users(userID, fname, lname, pathUrl, bday) VALUES('{id}', '{fname}', '{lname}', '{pathUrl}', '{bday}');")
    mysql.connection.commit()
    cur.close()
    return {"response": True}


def create_post(mysql, user_id, message, attachment):
    post_id = None
    cur = mysql.connection.cursor()
    query = "INSERT INTO messages(author, date, message"
    if attachment != "null":
        query += ", attachment"

    query += f") VALUES({user_id}, NOW(), '{message}'"
    if attachment != "null":
        query += f", '{attachment}'"
    
    query += ");"

    cur.execute(query)
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
        cur.execute(f"SELECT m.* FROM messages m INNER JOIN posts p ON m.post_id=p.post_id WHERE author={user_id} ORDER BY date DESC LIMIT {amount};")
    else:
        cur.execute(f"SELECT m.* FROM messages m INNER JOIN posts p ON m.post_id=p.post_id ORDER BY date DESC LIMIT {amount};")

    for message in cur.fetchall():
        response.append({
            "postID": message[0],
            "author": message[1],
            "timestamp": int(message[2].timestamp()),
            "message": message[3],
            "attachment": message[4] if message[4] else "null"
        })

    cur.close()
    return response


def comment(mysql, parent_post_id, user_id, message):
    response = {"response": False}
    #comment_id = create_post(mysql, user_id, message)["postID"]
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO messages(author, date, message) VALUES({user_id}, NOW(), {message});")
    comment_id = mysql.connection.insert_id()
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
            "message": comment[3],
            "attachment": "null"
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


def get_profile_pic(mysql, user_id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT profilePic FROM users u INNER JOIN profile p ON u.pathURL=p.pathURL WHERE u.userID={user_id};")
    data = cur.fetchone()
    cur.close()
    if data:
        return {"name": data[0]}
    else:
        print("Error getting profile pic path. get_profile_pic()")
        return {"name": "null"}


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
    
    cur.execute(f"SELECT * FROM userLikes WHERE post_id={post_id} AND user_id={user_id};")
    data = cur.fetchone()
    
    #Checks to see if it exists or not within the database
    if data:
        #Since it exists, we are going to "Unlike" the post
        cur.execute(f"DELETE FROM userLikes WHERE post_id={post_id} AND user_id={user_id};")
        response["response"] = False
    else:
        #Post hasn't been liked by user, so we create an entry into the database for it
        cur.execute(f"INSERT INTO userLikes(user_id,post_id) VALUES({user_id},{post_id});")
        response["response"] = True

    mysql.connection.commit()
    
    cur.close()
    return response

def get_likes(mysql,post_id):
    response = {"likes": 0}
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT COUNT(*) FROM userLikes WHERE post_id = {post_id};")
    for likes in cur.fetchone():
        response["likes"] = likes

    cur.close()
    return response


def create_profile(mysql, path_url):
    cur = mysql.connection.cursor()
    cur.execute(f"INSERT INTO profile(pathURL) values('{path_url}');")
    mysql.connection.commit()
    cur.close()
    return {"response": True}


def get_profile(mysql, user_id, path_url):
    response = {}

    # get user's general profile information
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM profile WHERE pathURL='{path_url}';")
    data = cur.fetchone()
    cur.close()
    if data:
        response["pathURL"] = path_url
        response["grade"] = data[1]      if data[1] else -1
        response["gender"] = data[2]     if data[2] else "null"
        response["about"] = data[3]      if data[3] else ""
        response["profilePic"] = data[4] if data[4] else "/static/assets/anonymous.png"
        response["coverPic"] = data[5]   if data[5] else "/static/assets/Walter_Pyramid.jpg"
    else:
        print("Error in get_profile: no profile found. Creating a new one.")
        create_profile(mysql, path_url)
        return get_profile(mysql, user_id, path_url)

    # get user's first and last name
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM users WHERE userID={user_id};")
    data = cur.fetchone()
    cur.close()
    if data:
        response["firstName"] = data[0]
        response["lastName"] = data[1]
    else:
        print("Error in get_profile: user_id invalid.")
        return response

    # get user's major (singular for now)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT majorName FROM userMajors u INNER JOIN majors m ON u.major_id=m.course_id WHERE u.user_id={user_id};")
    major = cur.fetchone()
    cur.close()
    if major:
        response["major"] = major[0]
    else:
        print("Error get_profile: no major found")
        response["major"] = ""

    # get user's courses
    response["courses"] = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT dept,courseNum FROM userCourses u INNER JOIN courses c ON u.course_id=c.course_id WHERE u.user_id={user_id};")
    courses = cur.fetchall()
    cur.close()
    if courses:
        for course in courses:
            response["courses"].append(course[0] + ' ' + str(course[1]))
    else:
        print("Error get_profile: no courses found")

    # get user's interests
    response["interests"] = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT interest FROM userInterests WHERE userID={user_id};")
    interests = cur.fetchall()
    cur.close()
    if interests:
        for interest in interests:
            response["interests"].append(interest[0])
        return response
    else:
        print("Error get_profile: no interests found")
        return response



def get_path_url(mysql, user_id):
    response = {"pathURL": "null"}
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT pathURL FROM users WHERE userID={user_id};")
    data = cur.fetchone()
    cur.close()
    if data:
        response["pathURL"] = data[0]
    
    return response


def get_name(mysql, user_id):
    name = ""
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT fname, lname FROM users WHERE userID={user_id};")
    data = cur.fetchone()
    cur.close()
    if data:
        name += data[0] + ' ' + data[1]
    return {"name": name}

def insert_major(mysql, major):
    response = {"response": False}
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM majors WHERE majorName='{major}';")
    if not cur.fetchone():
        cur.execute(f"INSERT INTO majors(majorName) VALUES('{major}');")
        mysql.connection.commit()
        response["response"] = True

    cur.close()
    return response


def get_courses(mysql):
    response = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT dept, courseNum FROM courses;")
    courses = cur.fetchall()
    cur.close()
    if courses:
        for course in courses:
            response.append(course[0] + ' ' + str(course[1]))

    return response


def get_interests(mysql):
    response = []
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT interest FROM interests;")
    interests = cur.fetchall()
    cur.close()
    if interests:
        for interest in interests:
            response.append(interest[0])

    return response


def set_user_interests(mysql, user_id, interests):
    cur = mysql.connection.cursor()
    for interest in interests:
        cur.execute(f"INSERT IGNORE INTO userInterests(interest, userID) VALUES('{interest}', {user_id});")
    mysql.connection.commit()
    cur.close()


def get_course_ids(mysql):
    lookup = dict()
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT course_id, dept, courseNum FROM courses;")
    courses = cur.fetchall()
    cur.close()
    if courses:
        for course in courses:
            lookup[course[1] + ' ' + str(course[2])] = course[0]
    
    return lookup


def set_user_courses(mysql, user_id, courses):
    lookup = get_course_ids(mysql)
    cur = mysql.connection.cursor()
    for course in courses:
        cur.execute(f"INSERT IGNORE INTO userCourses(course_id, user_id) VALUES({lookup[course]}, {user_id});")
    mysql.connection.commit()
    cur.close()


def set_user_major(mysql, user_id, major):
    insert_major(mysql, major)
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT course_id FROM majors WHERE majorName='{major}';")
    major_id = cur.fetchone()[0]
    cur.execute(f"INSERT INTO userMajors(user_id, major_id) VALUES({user_id}, {major_id}) ON DUPLICATE KEY UPDATE major_id={major_id};")
    mysql.connection.commit()
    cur.close()
    return {"response": True}


# helper function for update_profile to reach into users table 
def update_name(mysql, user_id, fname, lname):
    query_head = "UPDATE users SET "
    query_tail = f"WHERE userID={user_id};"
    columns = []
    if fname:
        columns.append(f"fname='{fname}' ")
    if lname:
        columns.append(f"lname='{lname}' ")

    if len(columns) > 0:
        query = ','.join(columns)
        cur = mysql.connection.cursor()
        cur.execute(query_head + query + query_tail)
        mysql.connection.commit()
        cur.close()
        return True
    else:
        return False


def update_major(mysql, user_id, major):
    if len(major) < 1: 
        return False

    insert_major(mysql, major)
    set_user_major(mysql, user_id, major)
    return True


# needs profile database table to be made before use
# will need to be updated 
def update_profile(mysql, user_id, path_url, profile):
    query_head = "UPDATE profile SET "
    query_tail = f"WHERE pathURL='{path_url}';"
    columns = []

    # some fields have to be handled seperately since they house data in a different table
    print(update_name(mysql, user_id, profile.fname, profile.lname))
    print(update_major(mysql, user_id, profile.major))
    print(set_user_interests(mysql, user_id, profile.interests))
    print(set_user_courses(mysql, user_id, profile.courses))

    # build up query
    if profile.year:
        columns.append(f"grade={profile.year} ")
    if profile.gender:
        columns.append(f"gender='{profile.gender}' ")
    if profile.profile_pic:
        columns.append(f"profilePic='{profile.profile_pic}'")
    if profile.background_pic:
        columns.append(f"coverPic='{profile.background_pic}'")

    # combine parts into whole query
    query = query_head
    query += ','.join(columns)
    query += query_tail

    # only insert into db if new information was given
    if len(columns) > 0:
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        cur.close()
        return {"response": True}
    else:
        return {"response": False}


if __name__ == "__main__":
    #insert test driver code
    get_image("", "test")
    profile = ProfileData()
    profile.set_first_name("Mike")
    profile.set_interests("Skateboarding")
    update_profile("", 9, profile)


def test(mysql):
    pass
