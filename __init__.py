from flask import Flask, render_template
import databases

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    return render_template('index.html')

@app.route('/api/showTables')
def test():
    return databases.fetchTables()

app.run()