from flask import Flask, render_template, request, g
import sqlite3
import json
import hashlib

app = Flask (__name__)

######################################################################################################
######################################################################################################
#This block taken from https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/
DATABASE = 'data/datastore.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
######################################################################################################
######################################################################################################

def init_db():
    query_db("CREATE TABLE IF NOT EXISTS students ( name TEXT PRIMARY KEY, grade INTEGER NOT NULL )")

def insertQuery(insertQuery):
    init_db()
    get_db().execute(insertQuery)
    get_db().commit()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    omfgEncodingAreYouSerious = username + '|' +  password

    #Here we check login user names and passwords
    return hashlib.md5(str(omfgEncodingAreYouSerious).encode('utf-8')).hexdigest() #python.org


#instrospect is the endpoint that is used to validate tokens
@app.route('/introspect')
def introspect():
    sessionId = request.args.get('sessionId')
    #BSL TODO here we investigate the legitimacy of the session ID
    return "GOOD"

@app.route('/insurance')
def insurance():
	return render_template('insurance.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
	app.run(debug=True)






















#
@app.route('/results')
def results():
    init_db()
    includeStudents = request.args.get('includeStudents')
    threshold = request.args.get('passingThreshold')

    if includeStudents == "all":
        return render_template('results.html',students=query_db("select * from students"),threshold=int(threshold))

    #implied else
    return render_template('results.html',students=query_db("select * from students where grade > " + threshold),threshold=int(threshold))

@app.route('/addStudent')
def addStudent():
    name = request.args.get('studentName')
    grade = request.args.get('studentGrade')
    insertQuery("INSERT INTO students (name, grade) VALUES ('" + name + "'," + grade + ")")
    return render_template('home.html')

@app.route('/updateStudent')
def updateStudent():
    name = request.args.get('studentName')
    grade = request.args.get('studentGrade')
    insertQuery("UPDATE students SET grade = " + grade + " WHERE name = '" + name + "'")
    return render_template('home.html')

@app.route('/deleteStudent')
def deleteStudent():
    name = request.args.get('studentName')
    insertQuery("DELETE FROM students WHERE name = '" + name + "'")
    return render_template('home.html')

@app.route('/searchStudents')
def searchStudents():
    searchValue = request.args.get('searchValue')
    searchValue = searchValue.lower()
    allStudents = query_db("select * from students where lower(name) like ('%" + searchValue + "%')")
    return json.dumps(allStudents)


