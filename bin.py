from flask import Flask, render_template, request, g ,redirect
import sqlite3
import json
import hashlib

app = Flask (__name__)

SESSIONS = {}

######################################################################################################
######################################Database Interaction############################################
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

def insertQuery(insertQuery):
    #init_db()
    get_db().execute(insertQuery)
    get_db().commit()
######################################################################################################
######################################################################################################

###########################################################################
############################Authentication Routes##########################
@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    loginCheck = query_db("SELECT userId, userType, userId, name FROM users WHERE userName = '" + username + "' \
         AND password = '" + password + "'")

    if len(loginCheck) == 0:
        return ""

    omfgEncodingAreYouSerious = username + '|' +  password
    global SESSIONS

    sessionId = hashlib.md5(str(omfgEncodingAreYouSerious).encode('utf-8')).hexdigest() #python.org

    SESSIONS[sessionId] = SessionObject()

    SESSIONS[sessionId].sessionId = sessionId
    SESSIONS[sessionId].patient = None
    SESSIONS[sessionId].userType = loginCheck[0][1]
    SESSIONS[sessionId].loggedInName = loginCheck[0][3]
    SESSIONS[sessionId].loggedInUserId = loginCheck[0][2]

    if loginCheck[0][1] == "patient":
        SESSIONS[sessionId].patient = getPatientFromUserId(loginCheck[0][2])

    return sessionId

@app.route('/logout')
def logout():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    global SESSIONS
    del SESSIONS[sessionId]

    return render_template('index.html')

#instrospect is the endpoint that is used to validate tokens
@app.route('/introspect')
def introspect():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    global SESSIONS
    thisSession = SESSIONS[sessionId]

    if thisSession == None:
        return None

    return "GOOD"
###########################################################################
###########################################################################


###########################################################################
####################################Single Routes##########################
@app.route('/setUpUsers')
def setUpUsers():

    #insertQuery("DROP TABLE users")
    #insertQuery("CREATE TABLE IF NOT EXISTS users ( userId INTEGER PRIMARY KEY, \
    # name TEXT NOT NULL, patientId TEXT, userName TEXT NOT NULL, password TEXT NOT NULL, \
   #  userType TEXT NOT NULL )")

    insertQuery("CREATE TABLE IF NOT EXISTS insurance ( id INTEGER PRIMARY KEY, userId INTEGER NOT NULL, \
    type TEXT NOT NULL, provider TEXT NOT NULL, groupFamily TEXT NOT NULL)")
    insertQuery("DROP TABLE insurance")
    insertQuery("CREATE TABLE IF NOT EXISTS insurance ( id INTEGER PRIMARY KEY, userId INTEGER NOT NULL, \
    type TEXT NOT NULL, provider TEXT NOT NULL, groupFamily TEXT NOT NULL)")

    insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    (1,9, 'Dental','Delta','D234/F22')")

    insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    (2,9, 'Health','BCBS PPO','J0812-UI121212')")

    insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    (3,9, 'Medications','Quickscripts','D234/F22')")

    insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    (4,9, 'Supplemental','AFLAC','QuackQuack Squaaaaack')")

    insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    (5,9, 'Liability','GCL R Us','PP-2131ASD')")

    insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    (6,9, 'Life','MetLife','MVMV/UWH')")

    #insertQuery("delete from users where userId >= 1")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (1,'firstUser', 'SUPERLONGPATIENTID1','user1','pass','provider')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (2,'secondUser','SUPERLONGPATIENTID2','user2','pass','provider')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (3,'thirdUser', 'SUPERLONGPATIENTID3','user3','pass','provider')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (4,'fourthUser','SUPERLONGPATIENTID4','user4','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (5,'fifthUser', 'SUPERLONGPATIENTID5','user5','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES ( 6,'User Six', 'SUPERLONGPATIENTID6','user5', 'pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES ( 7,'Ultimate User', 'SUPERLONGPAID7','user6', 'pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES ( 8,'Ocho Ba', 'SUPERLONGPATIENTI1D8','user7', 'pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES ( 9,'Jiao Sher', 'SUPERLONGPATIENTD9','user8', 'pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (10,'Gelada Italiano', 'SUPERLONGP15','user9', 'pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (11,'Tira Misu', 'SUPERLONGPA2TID135','user10','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (12,'Dolce de Leche', 'SUPERLOTID125','user11','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (13,'Helado Deliciodo', 'ATIENTID115','user12','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (14,'Legume Paste', 'SUPEaTIENTID165','user13','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (15,'Cafe Blanco', 'SUPERLIENTID1115','user14','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (16,'Delight Fully', 'GPATIENTID1335','user15','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (17,'Iced Cream', 'ONGPATIENTID18885','user16','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (18,'Home Made', 'RLONGPATIENTID5778','user17','pass','patient')")
    #insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) VALUES (19,'Tasty Treat', 'LONGPATIENTID588','user18','pass','patient')")

    global SESSIONS
    SESSIONS['81538bb3bf61fa90eea389a130bf50f2'] = SessionObject()
    thisSession = SESSIONS['81538bb3bf61fa90eea389a130bf50f2']
    thisSession.sessionId = "81538bb3bf61fa90eea389a130bf50f2"
    thisSession.patient = getPatientFromUserId(9)
    thisSession.userType= "provider"
    thisSession.loggedInName = ""
    thisSession.loggedInUserId = 1

    return render_template('setUpUsers.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getWelcomeMessage')
def getWelcomeMessage():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    global SESSIONS
    thisSession = SESSIONS[sessionId]
    thisSession.patientName = getPatientFromUserId(thisSession.loggedInUserId).name

    if thisSession.patient == None:
        return "Select Patient To Proceed"

    if thisSession.userType == "provider":
        return "Patient Selected " + thisSession.patient.name

    return "Welcome " + thisSession.patientName


###########################################################################
###########################################################################


###########################################################################
############################Patient Select Routes##########################

#This is initial landing to page with no submitted data
@app.route('/patientSelect')
def patientSelect():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    allowAccess = verifyProviderAccess(sessionId)

    if allowAccess == False:
        return render_template('notAllowed.html')

    return render_template('patientSelect.html')


@app.route('/patientSearchCriteria', methods=['POST'])
def patientSearchCriteria():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    allowAccess = verifyProviderAccess(sessionId)

    if allowAccess == False:
        return render_template('notAllowed.html')

    searchCriteria = request.form['searchText']

    searchResults = query_db("SELECT userId, name FROM users WHERE userType = 'patient' AND \
    lower(name) LIKE '%" + searchCriteria.lower() + "%' order by userId desc limit 10")

    return render_template('patientSelect.html',searchResults=searchResults)


@app.route('/patientSelectSubmit', methods=['POST'])
def patientSelectSubmit():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    allowAccess = verifyProviderAccess(sessionId)

    if allowAccess == False:
        return render_template('notAllowed.html')

    patientUserId = request.form['patientId']

    global sessions
    thisSession = SESSIONS[sessionId]
    thisSession.patient = getPatientFromUserId(patientUserId)

    return redirect('/')
###########################################################################
###########################################################################

###########################################################################
############################Insurance Routes###############################

@app.route('/insurance')
def insurance():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')

    global SESSIONS
    thisSession = SESSIONS[sessionId]
    userId = thisSession.patient.userId

    retInsurance = query_db("SELECT type, provider, groupFamily FROM insurance \
    WHERE userId = '" + str(userId) + "'")

    return render_template('insurance.html',insurances=retInsurance)

@app.route('/insuranceAdd', methods=['POST'])
def insuranceAdd():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    global SESSIONS
    thisSession = SESSIONS[sessionId]
    userId = thisSession.patient.userId

    insuranceType = request.form['addType']
    insuranceProvider = request.form['addProvider']
    insuranceGroup = request.form['addGroup']

    currentMax = query_db("SELECT MAX(id) + 1  FROM insurance")
    #nextInsuranceId = int(str(currentMax[0])) + 1

    print(str(currentMax[0]))
    print(str(currentMax[0]))
    print(str(currentMax[0]))
    print(str(currentMax[0]))
    print(str(currentMax[0]))

    nextInsuranceId = str(currentMax[0]).replace(',','',2).replace(')','',2).replace('(','',2)

    insertQueryString = "INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES ('" + nextInsuranceId + "'," + userId + ", '" + insuranceType + "','" + insuranceProvider + "','" + insuranceGroup + "')"

    insertQuery(insertQueryString)

    return redirect('/insurance')


###########################################################################
###########################################################################


def verifyProviderAccess(sessionId):
    global SESSIONS
    thisSession = SESSIONS[sessionId]
    if thisSession == None:
        return False
    if thisSession.userType == "provider":
        return True

    return False

def getPatientFromUserId(userId):
    thisPatientQueryResult = query_db("SELECT name, patientId, userId FROM users WHERE userId = '" + str(userId) + "'")
    retPatient = PatientObject()
    retPatient.name = str(thisPatientQueryResult[0][0])
    retPatient.patientId = str(thisPatientQueryResult[0][1])
    retPatient.userId = str(thisPatientQueryResult[0][2])
    return retPatient

###########################################################################
############################Object Library#################################
class SessionObject:
    def __init__(self):
        self.sessionId = ""
        self.patient = None
        self.userType = ""
        self.loggedInName = ""
        self.loggedInUserId = ""

        #self.expiration ... dont feel like fooling with timestamp manipulation
        #odd that time is the most predictable thing in the universe yet somehow
        #   its still a PITA for us to program around


class PatientObject:
    def __init__(self):
        self.name = ""
        self.patientId = ""
        self.userId = ""


















@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
	app.run(debug=True)






















#
@app.route('/results')
def results():
    #init_db()
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


