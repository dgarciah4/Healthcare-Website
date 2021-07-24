import sqlite3

conn = sqlite3.connect('patient.db')
c = conn.cursor()

c.execute("SELECT * FROM patients")
print(c.fetchall())