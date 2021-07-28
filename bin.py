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
@app.route('/newUser')
def newUser():
    return render_template('newUser.html',userAdded="")

@app.route('/newUserSubmit', methods=['POST'])
def newUserSubmit():
    name = request.form['name']
    newUserName = request.form['username']
    newUserPassword = request.form['password']
    newUserType = request.form['userType']

    newUserId = query_db("SELECT (max(userId) + 1) FROM users ")
    #newUserIdMadeIntoSomethingThatCanBeConcate
    newId = str(newUserId[0]).replace(',','',1).replace(')','',1).replace('(','',1)

    insertQuery("INSERT INTO users (userId, name, patientId, userName, password, userType) \
    VALUES (" + newId + ", \
    '" + name + "', \
    '" + newId + "', \
    '" + newUserName + "', \
    '" + newUserPassword + "', \
    '" + newUserType + "' \
    )")

    insertQuery("INSERT INTO patientInformation (userId) VALUES " + str(newUserId[0]).replace(',','',1) + "")

    return render_template('newUser.html',userAdded="Added " + newUserName)

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

    #insertQuery("CREATE TABLE IF NOT EXISTS patientInformation ( \
    #userId INTEGER PRIMARY KEY, \
    #address TEXT, \
    #city TEXT, \
    #state TEXT, \
    #zip TEXT, \
    #phoneH TEXT, \
    #phoneCW TEXT, \
    #dob TEXT, \
    #SSN TEXT, \
    #occupation TEXT, \
    #employer TEXT, \
    #email TEXT, \
    #orientation TEXT, \
    #relationshipStatus TEXT )")

    #insertQuery("DROP TABLE patientInformation")
    #insertQuery("CREATE TABLE IF NOT EXISTS patientInformation ( \
    #userId INTEGER PRIMARY KEY, \
    #address TEXT, \
    #city TEXT, \
    #state TEXT, \
    #zip TEXT, \
    #phoneH TEXT, \
    #phoneCW TEXT, \
    #dob TEXT, \
    #SSN TEXT, \
    #occupation TEXT, \
    #employer TEXT, \
    #email TEXT, \
    #orientation TEXT, \
    #relationshipStatus TEXT )")

    #insertQuery("DROP TABLE users")
    #insertQuery("CREATE TABLE IF NOT EXISTS users ( userId INTEGER PRIMARY KEY, \
    #name TEXT NOT NULL, patientId TEXT, userName TEXT NOT NULL, password TEXT NOT NULL, \
    #userType TEXT NOT NULL )")
    #insertQuery("CREATE TABLE IF NOT EXISTS insurance ( id INTEGER PRIMARY KEY, userId INTEGER NOT NULL, \
    #type TEXT NOT NULL, provider TEXT NOT NULL, groupFamily TEXT NOT NULL)")
    #insertQuery("DROP TABLE insurance")
    #insertQuery("CREATE TABLE IF NOT EXISTS insurance ( id INTEGER PRIMARY KEY, userId INTEGER NOT NULL, \
    #type TEXT NOT NULL, provider TEXT NOT NULL, groupFamily TEXT NOT NULL)")
    #insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    #(1,9, 'Dental','Delta','D234/F22')")
    #insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    #(2,9, 'Health','BCBS PPO','J0812-UI121212')")
    #insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    #(3,9, 'Medications','Quickscripts','D234/F22')")
    #insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    #(4,9, 'Supplemental','AFLAC','QuackQuack Squaaaaack')")
    #insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    #(5,9, 'Liability','GCL R Us','PP-2131ASD')")
    #insertQuery("INSERT INTO insurance (id, userId, type, provider, groupFamily) VALUES \
    #(6,9, 'Life','MetLife','MVMV/UWH')")
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



















###########################################################################
############################ Patient History and Forms#####################




# c.execute("""CREATE TABLE patients (
#    first_name TEXT,
#    middle_name TEXT,
#    last_name TEXT,
#    address TEXT,
#    city TEXT,
#    state TEXT,
#    zip TEXT,
#    phone_h TEXT,
#    phone_c_w TEXT,
#    dob TEXT,
#    ssn TEXT,
#    occupation TEXT,
#    employer TEXT,
#    email TEXT,
#    insurance_provider TEXT,
#    sexual_orientation TEXT,
#    relationship_status TEXT,
#    last_visit_before TEXT,
#    date_of_visit TEXT,
#    health_conditions TEXT,
#    medications TEXT
#    )""")

@app.route('/patientInformation', methods = ['POST', 'GET'])
def patientInformation():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    global SESSIONS
    thisSession = SESSIONS[sessionId]
    userId = thisSession.patient.userId
    patientInformation = query_db("SELECT * FROM patientInformation WHERE userId = '" + userId + "'")

    return render_template('patientInformation.html',patientInformation=patientInformation[0])

@app.route('/patientInformationUpdate', methods = ['POST', 'GET'])
def patientInformationUpdate():
    sessionId = request.cookies.get('sessionId') #request.args.get('sessionId')
    global SESSIONS
    thisSession = SESSIONS[sessionId]
    userId = thisSession.patient.userId

    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    zip = request.form['zip']

    phoneH = request.form['phoneH']
    phoneCW = request.form['phoneCW']
    dob = request.form['dob']
    ssn = request.form['ssn']

    occupation = request.form['occupation']
    employer = request.form['employer']
    email = request.form['email']

    gender = request.form['gender']
    status = request.form['status']

    insertQueryString = "UPDATE patientInformation SET \
    zip = '" + zip + "', \
    address = '" + address + "', \
    city = '" + city + "', \
    state = '" + state + "', \
    zip = '" + zip + "', \
    phoneH = '" + phoneH + "', \
    phoneCW = '" + phoneCW + "', \
    dob = '" + dob + "', \
    ssn = '" + ssn + "', \
    occupation = '" + occupation + "', \
    employer = '" + employer + "', \
    email = '" + email + "', \
    gender = '" + gender + "', \
    status = '" + status + "' WHERE \
    userId = '" + userId + "'";

    return redirect('patientInformation')

@app.route('/patientHistory', methods = ['POST', 'GET'])
def patientHistory():
    return render_template('patientHistory.html')

@app.route('/patientHistoryUpdate', methods = ['POST', 'GET'])
def patientHistoryUpdate():
    return render_template('patientHistoryUpdate.html')

@app.route('/patientHistoryRetrieve', methods = ['POST', 'GET'])
def patientHistoryRetrieve():
    return render_template('enterSSN.html')

@app.route('/formProcess', methods = ['POST', 'GET'])
def formProcess():
    if request.method == 'POST':
        try:
            first_name = request.form.get('fname')
            middle_name = request.form.get('mname')
            last_name = request.form.get('lname')
            address = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip')
            phone_h = request.form.get('home_phone')
            phone_c_w = request.form.get('cell_work_phone')
            dob = request.form.get('dob')
            ssn = request.form.get('ss#')
            occupation = request.form.get('occupation')
            employer = request.form.get('employer')
            email = request.form.get('email')
            insurance_provider = request.form.get('insurance-provider')
            sexual_orientation = request.form.get('gender')
            relationship_status = request.form.get('status')
            last_visit_before = request.form.get('visit')
            date_of_visit = request.form.get('lastvisit')
            health_conditions = request.form.get('health-conditions')
            medications = request.form.get('medication')

            with sqlite3.connect('patient.db') as conn:
                c = conn.cursor()

                c.execute("""INSERT INTO patients (first_name,middle_name,last_name,address,city,state,zip,phone_h,phone_c_w,dob,ssn,occupation,employer,email,insurance_provider,sexual_orientation,relationship_status,last_visit_before,date_of_visit,health_conditions,medications)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (first_name,middle_name,last_name,address,city,state,zip_code,phone_h,phone_c_w,dob,ssn,occupation,employer,email,insurance_provider,sexual_orientation,relationship_status,last_visit_before,date_of_visit,health_conditions,medications))

                conn.commit()
                result = 'You have submitted your form successfully'
        except:
            conn.rollback()
            result = 'There was an error when attempting to submit your form'

        finally:
            return render_template('feedback.html', result=result)
            conn.close()

@app.route('/formUpdate', methods = ['POST', 'GET'])
def formUpdate():
    if request.method == 'POST':
        try:
            first_name = request.form.get('fname')
            middle_name = request.form.get('mname')
            last_name = request.form.get('lname')
            address = request.form.get('address')
            city = request.form.get('city')
            state = request.form.get('state')
            zip_code = request.form.get('zip')
            phone_h = request.form.get('home_phone')
            phone_c_w = request.form.get('cell_work_phone')
            dob = request.form.get('dob')
            ssn = request.form.get('ss#')
            occupation = request.form.get('occupation')
            employer = request.form.get('employer')
            email = request.form.get('email')
            insurance_provider = request.form.get('insurance-provider')
            sexual_orientation = request.form.get('gender')
            relationship_status = request.form.get('status')
            last_visit_before = request.form.get('visit')
            date_of_visit = request.form.get('lastvisit')
            health_conditions = request.form.get('health-conditions')
            medications = request.form.get('medication')

            with sqlite3.connect('patient.db') as conn:
                c = conn.cursor()

                c.execute("""UPDATE patients SET first_name=?,middle_name=?,last_name=?,address=?,city=?,state=?,zip=?,phone_h=?,phone_c_w=?,dob=?,occupation=?,employer=?,email=?,insurance_provider=?,sexual_orientation=?,relationship_status=?,last_visit_before=?,date_of_visit=?,health_conditions=?,medications=? 
                          WHERE ssn = ?""",(first_name,middle_name,last_name,address,city,state,zip_code,phone_h,phone_c_w,dob,occupation,employer,email,insurance_provider,sexual_orientation,relationship_status,last_visit_before,date_of_visit,health_conditions,medications,ssn))

                conn.commit()
                result = 'Your form was updated successfully'

        except:
            conn.rollback()
            result = 'Something went wrong with updating your form'

        finally:
            return render_template('feedback.html', result = result)
            conn.close()

@app.route('/historyDisplay', methods = ['POST', 'GET'])
def historyDisplay():
    if request.method == 'GET':
        social = request.values.get('social-security')

        with sqlite3.connect('patient.db') as conn:
            c = conn.cursor()

            c.execute("SELECT * FROM patients WHERE ssn = ?",(social,))
            items = c.fetchall()

            conn.commit()

            return render_template('historyDisplay.html', items = items)
            conn.close()

    return render_template('patientHistory.html')



















###########################################################################
########################### Main App ######################################

if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

