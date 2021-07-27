import sqlite3

conn = sqlite3.connect('patient.db')
c = conn.cursor()

m = "365-42-5987"
c.execute("SELECT rowid, * FROM patients")
items = c.fetchall()

for x in items:
    print(x)

conn.commit()

conn.close()



# m = c.execute("SELECT * FROM patients WHERE ssn = '356-26-5698'")

