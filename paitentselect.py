import os
from flask import Flask, render_template, flash, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask (__name__)

app.config['SQLAlchemy_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLAlchemy_TRAC_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'oursecretkey'

db=SQLAlchemy(app)
Migrate(app,db)

class Paitent(db.Model):
	__tablename__="paitent"
	id= db.Column(db.Integer, primary_key=True)
	firstname= db.Column(db.Text)
	lastname= db.Column(db.Text)
	dob= db.Column(db.Text)
	gender= db.Column(db.Text)
	chosen= db.Column(db.Boolean)
	

	def __init__(self, firstname, lastname, dob, gender):
		self.firstname=firstname
		self.lastname=lastname
		self.dob=dob
		self.gender=gender
		self.chosen=False
		

	

@app.route('/', methods = ['GET','POST'])
def index():
    
    search = request.form.get('search', False)
    if request.method == 'POST':
        option = request.form.get('option', False)
        if option == "fname":
            return indexfname(search)
        elif option == "dob":
            return indexdob(search)
        elif option == "gender":
        	return indexgender(search)
        elif option == "lname":
        	return indexlname(search)
        elif option == None:
            return indexsearch(search)

    return render_template('paitentselectprototype.html', paitents = Paitent.query.all())
    
@app.route('/fname', methods = ['GET','POST'])
def indexfname(search):
    
    return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(search == Paitent.firstname ))
        
        
    #return render_template('paitentselectprototype.html')

@app.route('/dob', methods = ['GET','POST'])
def indexdob(search):
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.dob == search ))
    

@app.route('/gender', methods = ['GET','POST'])
def indexgender(search):
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.gender == search ))
@app.route('/lname', methods = ['GET','POST'])
def indexlname(search):
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(search == Paitent.lastname ))

@app.route('/search', methods = ['GET','POST'])
def indexsearch(search):
        arr = [Paitent.query.all()]
        paitents=[]
        for i in arr:
            if i.gender == search or i.dob == search or i.firstname+i.lastname == search:
                paitents.append(i)
        return render_template('paitentselectprototype.html', paitents = paitents)
@app.route('/submit', methods = ['GET','POST'])
def indexsubmit():
        if request.method == 'POST':
           chosen = request.form.get('select', False) 
        return render_template('paitentselectprototype.html')


if __name__ == '__main__':
	db.create_all()
	
	mahmut = Paitent('Mahmut', 'Unan', '05-07-85', 'Male')
	sam = Paitent('Sam', 'Wick', '10-01-63', 'Female')
	carrie = Paitent('Carrie', 'Jones', '02-25-03', 'Female')
	db.session.add_all([mahmut,sam, carrie])
	db.session.commit()
	
	app.run(debug = True)

