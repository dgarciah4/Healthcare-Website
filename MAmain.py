import os
import random
import string
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

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


@app.route('/')
def home():
    return render_template('index.html')

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


if __name__ == "__main__":
    app.run()

