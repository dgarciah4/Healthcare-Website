from paitentselect import db,Paitent

db.create_all()

mahmut = Paitent('Mahmut', 'Unan', '5-07-85', 'Male')
sam = Paitent('Sam', 'Wick', '10-01-63', 'Female')
carrie = Paitent('Carrie', 'Jones', '02-25-03', 'Female')

print(sam.id)
print(mahmut.id)
print(carrie.id)

db.session.add_all([mahmut,sam, carrie])

db.session.commit()

print(sam.dob)
print(mahmut.lastname)
print(carrie.gender)

all_students = Paitent.query.all()
print(all_students)