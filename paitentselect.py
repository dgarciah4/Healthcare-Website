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
	

	def __init__(self, firstname, lastname, dob, gender):
		self.firstname=firstname
		self.lastname=lastname
		self.dob=dob
		self.gender=gender
		

	

@app.route('/', methods = ['GET','POST'])
def index():
    
    search = request.form.get('search', False)
    if request.method == 'POST':
        option = request.form['option']
        if option == "name":
            return indexname(search)
        elif option == "dob":
            return indexdob(search)
        elif option == "gender":
        	return indexgender(search)
        elif option == None:
        	return indexsearch(search)
        else:
            return indexsearch(search)

    return render_template('paitentselectprototype.html', paitents = Paitent.query.all())
    
@app.route('/name', methods = ['GET','POST'])
def indexname(search):
    return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(search == Paitent.firstname or search == Paitent.lastname ))
        
        
    return render_template('paitentselectprototype.html')

@app.route('/dob', methods = ['GET','POST'])
def indexdob(search):
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.dob == search ))
    

@app.route('/gender', methods = ['GET','POST'])
def indexgender(search):
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.gender == search ))
@app.route('/search', methods = ['GET','POST'])
def indexsearch(search):
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.gender == search or Paitent.dob == search or Paitent.firstname+Paitent.lastname == search  ))


if __name__ == '__main__':
	db.create_all()
	
	mahmut = Paitent('Mahmut', 'Unan', '5-07-85', 'Male')
	sam = Paitent('Sam', 'Wick', '10-01-63', 'Female')
	carrie = Paitent('Carrie', 'Jones', '02-25-03', 'Female')
	db.session.add_all([mahmut,sam, carrie])
	db.session.commit()
	
	app.run(debug = True)

