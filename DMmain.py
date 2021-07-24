from flask import Flask, render_template, request
import sqlite3
import random
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

## environment name = directMessagingEnv

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False

db=SQLAlchemy(app)


## Create a Model for User and Departments

class Employee(db.Model):
    __tablename__="employee"
    eID = db.Column(db.Text, primary_key=True)
    name = db.Column(db.Text)
    pos = db.Column(db.Text) ## position
    dpt = db.Column(db.Text) ## department


    def __init__(self, eID, name, pos, dpt):
        self.eID  = eID
        self.name = name
        self.pos  = pos
        self.dpt  = dpt


## Create a Model for Messages
class Message(db.Model):
    __tablename__="message"
    mID = db.Column(db.Text, primary_key=True)
    rName = db.Column(db.Text)
    mes= db.Column(db.Text)
    subj = db.Column(db.Text)

    def __init__(self, mID, rName, subj, mes):
        self.mID = mID      ## message ID
        self.rName = rName  ## recipiant name
        self.subj = subj    ## subject
        self.mes = mes      ## message



@app.route('/')
def home ():
    return render_template ('index.html')

@app.route('/messaging', methods = ["POST", "GET"])
def messaging ():

    all_messages = Message. query.all()

    return render_template ('messaging.html',all_messages=all_messages)

@app.route('/employeeForm', methods = ["POST", "GET"])
def employeeForm ():
    db.create_all()
    db.session.commit()
    if request.method == 'POST':
        eData = request.form
        idsuffix = random.randint(1111,9999)
        idprefix = "HC"
        eID = idprefix + str(idsuffix)

        name = eData["name"]
        pos = eData["pos"]
        dpt = eData["dpt"]

        emp_data = Employee(eID, name, pos, dpt)
        db.session.add(emp_data)
        db.session.commit()
        all_employees = Employee.query.all()
        return render_template('employeeList.html', all_employees = all_employees)

    return render_template ('employeeForm.html')

@app.route('/newMessage', methods = ["POST", "GET"])
def newMessage ():
    db.create_all()
    db.session.commit()

    if request.method == 'POST':
        data = request.form
        mprefix = "MS"
        mSuffix = random. randint(1000,9999)
        mID = mprefix + str(mSuffix)
        rName = data["rName"]
        subj = data["subj"]
        mes = data["mes"]

        new_data = Message(mID, rName, subj, mes)
        db.session.add(new_data)
        db.session.commit()
        all_messages = Message.query.all()
        return render_template('messaging.html', all_messages = all_messages)
    return render_template ('newMessage.html')



@app.route('/recipiant1', methods = ["POST", "GET"])
def recipiant1 ():
    all_employees = Employee.query.all()
    all_messages = Message. query.all()
    return render_template ('recipiant1.html',all_employees=all_employees, all_messages=all_messages)


@app.route('/rec1-Message', methods = ["POST", "GET"])
def rec1Message ():
    if request.method == "POST":
        select_recipiant =request.form.get("message.rName")
        Message.query.filter(Message.rName == select_recipiant)
        db.session.commit()
    all_messages = Message.query.all()
    return render_template ('rec1-Message.html',all_messages = all_messages)

## List All Employees
@app.route('/list_all', methods = ['POST', 'GET'])
def list_all ():
    all_employees = Employee.query.all()
    return render_template ('employeeList.html',all_employees = all_employees)

@app.route('/convList', methods = ['POST', 'GET'])
def results ():

    return render_template('convList.html')





@app.route('/recipiant2', methods = ["POST", "GET"])
def recipiant2 ():
    return render_template ('recipiant2.html')

@app.route('/recipiant3', methods = ["POST", "GET"])
def recipiant3 ():
    return render_template ('recipiant3.html')









if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
