from flask import Flask, render_template, request
import databases

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    return render_template('index.html')

@app.route('/api/showTables')
def test():
    return databases.fetchTables()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    pass_hash = data['password']
    return databases.login(email, pass_hash)

app.run()