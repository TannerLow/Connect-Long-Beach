from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL 
import databases
from profile_data import ProfileData

app = Flask(__name__)
databases.initialize(app)
mysql = MySQL(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    # databases.test(mysql)
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    pass_hash = data['password']
    return databases.login(mysql, email, pass_hash)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    pass_hash = data['password']
    fname = data["firstName"]
    lname = data["lastName"]
    gender = data["gender"]
    month = data["month"]
    day = data["day"]
    year = data["year"]
    return databases.register(mysql, email, pass_hash, fname, lname, gender, month, day, year)


@app.route('/api/emailCheck/<email>')
def check_email(email):
    return databases.is_email_in_use(mysql, email)


@app.route('/api/post', methods=['POST'])
def post():
    data = request.get_json()
    message = data["message"]
    user_id = data["userID"]
    attachment = data["attachment"]
    return databases.create_post(mysql, user_id, message, attachment)


@app.route('/api/getPosts/<amount>', defaults={'user_id': -1})
@app.route('/api/getPosts/<amount>/<user_id>')
def get_posts(amount, user_id):
    return jsonify(databases.get_posts(mysql, int(amount), int(user_id)))


@app.route('/api/comment', methods=['POST'])
def comment():
    data = request.get_json()
    message = data["message"]
    user_id = data["userID"]
    post_id = data["postID"]
    return databases.comment(mysql, post_id, user_id, message)


@app.route('/api/getComments/<post_id>')
def get_comments(post_id):
    return jsonify(databases.get_comments(mysql, int(post_id)))

@app.route('/api/about', methods=['POST'])
def set_about():
    data = request.get_json()
    user_id = data["userID"]
    message = data["aboutMe"]
    return databases.create_about(mysql,int(user_id), message)

@app.route('/api/like', methods=['POST'])
def like_unlike_post():
    data = request.get_json()
    user_id = data['userID']
    post_id = data["postID"]
    return databases.like_unlike_post(mysql, int(user_id), int(post_id))

@app.route('/api/getLikes/<post_id>')
def get_likes(post_id):
    return jsonify(databases.get_likes(mysql, int(post_id)))

@app.route('/api/getImage/<path>')
def get_image(path):
    return databases.get_image(mysql, path)


@app.route('/api/storeImage', methods=['POST'])
def store_image():
    data = request.get_json()
    image = data["image"]
    path = data["path"]
    return databases.store_image(mysql, image, path)

@app.route('/api/updateProfile', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = data["userID"]
    path_url = data["pathURL"]
    profile = ProfileData()
    profile.set_first_name(data["fname"])
    profile.set_last_name(data["lname"])
    profile.set_major(data["major"])
    profile.set_year(data["year"])
    profile.set_gender(data["gender"])
    profile.set_profile_pic(data["profilePic"])
    profile.set_background_pic(data["backgroundPic"])
    profile.set_interests(data["interests"])
    profile.set_courses(data["courses"])
    return databases.update_profile(mysql, user_id, path_url, profile)


@app.route('/api/createProfile/<path_url>')
def create_profile(path_url):
    return databases.create_profile(mysql, path_url)


@app.route('/api/getProfile/<user_id>/<path_url>')
def get_profile(user_id, path_url):
    return databases.get_profile(mysql, int(user_id), path_url)


@app.route('/api/getPathURL/<user_id>')
def get_path_url(user_id):
    return databases.get_path_url(mysql, int(user_id))


@app.route('/api/getInterests')
def get_interests():
    return jsonify(databases.get_interests(mysql))


@app.route('/api/getCourses')
def get_courses():
    return jsonify(databases.get_courses(mysql))


@app.route('/api/getName/<user_id>')
def get_name(user_id):
    return databases.get_name(mysql, int(user_id))


@app.route('/api/getProfilePic/<user_id>')
def get_profile_pic(user_id):
    return databases.get_profile_pic(mysql, int(user_id))


app.run()