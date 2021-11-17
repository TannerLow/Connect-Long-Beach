from flask import Flask, render_template, request
from flask_mysqldb import MySQL 
import databases
from profile_data import ProfileData

app = Flask(__name__)
databases.initialize(app)
mysql = MySQL(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    databases.test(mysql)
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


@app.route('/api/updateProfile', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = data["userID"]
    profile = ProfileData()
    profile.set_first_name(data["firstName"])
    profile.set_last_name(data["lastName"])
    profile.set_major(data["major"])
    profile.set_year(data["year"])
    profile.set_gender(data["gender"])
    profile.set_interests(data["interests"])
    profile.set_courses(data["courses"])
    return databases.update_profile(mysql, user_id, profile)


@app.route('/api/getProfile/<path_url>')
def get_profile(path_url):
    return databases.get_profile(mysql, path_url)


app.run()