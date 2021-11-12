from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL 
import databases

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
    return databases.create_post(mysql, user_id, message)


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


app.run()