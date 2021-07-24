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
#Migrate(app,db)

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
    if request.method == 'POST':
        option = request.form['option']
        if option == "name":
            return redirect(url_for('indexname'))
        elif option == "dob":
            return redirect(url_for('indexdob'))
        elif option == "gender":
        	return redirect(url_for('indexgender'))
        else:
            return redirect(url_for('indexsearch'))

    return render_template('paitentselectprototype.html', paitents = Paitent.query.all())
    
@app.route('/name', methods = ['GET','POST'])
def indexname():
    return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.firstname+Paitent.lastname == search ))
        
        
    return render_template('paitentselectprototype.html')

@app.route('/dob', methods = ['GET','POST'])
def indexdob():
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.dob == search ))
    

@app.route('/gender', methods = ['GET','POST'])
def indexgender():
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.gender == search ))
@app.route('/search', methods = ['GET','POST'])
def indexsearch():
        return render_template('paitentselectprototype.html', paitents = Paitent.query.filter(Paitent.gender == search or Paitent.dob == search or Paitent.firstname+Paitent.lastname == search  ))


if __name__ == '__main__':
	db.create_all()
	app.run(debug = False)
