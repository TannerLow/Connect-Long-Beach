from flask import Flask, render_template, request
from flask_mysqldb import MySQL 
import databases

app = Flask(__name__)
databases.initialize(app)
mysql = MySQL(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    return render_template('index.html')


@app.route('/api/showTables')
def test():
    return databases.fetchTables(mysql)


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
    return databases.register(mysql, email, pass_hash)

app.run()