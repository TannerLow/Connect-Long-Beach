from flask import Flask, render_template
import databases

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/api/showTables')
def test():
    print(databases.fetchTables())
    return databases.fetchTables()

app.run()