import sqlite3

conn = sqlite3.connect('LicenseInfo.db')

'''
conn.execute(CREATE TABLE Holders
         (ID INT PRIMARY KEY     NOT NULL,
         NAME           TEXT    NOT NULL,
         GENDER         TEXT    NOT NULL,
         DOB            CHAR(20)     NOT NULL,
         ADDRESS        CHAR(50),
         PhoneNumber   INT);)      '''

'''
conn.execute("INSERT INTO Holders (ID, NAME, GENDER, DOB, ADDRESS, PhoneNumber) \
      VALUES (8866, 'Rahul Tripathi', 'Male', '26/5/1996', '253, Gavli Galli, Kolhapur', 5689532145)")

conn.execute("INSERT INTO Holders (ID, NAME, GENDER, DOB, ADDRESS, PhoneNumber) \
      VALUES (9655, 'Pranav Mukharji', 'Male', '15/2/1991', '123, Chauthai Galli, Miraj', 7486231289)")

conn.execute("INSERT INTO Holders (ID, NAME, GENDER, DOB, ADDRESS, PhoneNumber) \
      VALUES (1433, 'Nirmala Pawar', 'Female', '21/3/1994', 'A/p Dhavli, Sangli', 6532149856)")

conn.execute("INSERT INTO Holders (ID, NAME, GENDER, DOB, ADDRESS, PhoneNumber) \
      VALUES (8765, 'Harishchandra mehta', 'Male', '12/4/1997', 'A/p Islampur, Sangli', 2351654785)")
'''

cursor = conn.execute("SELECT ID, NAME, GENDER, DOB, ADDRESS, PhoneNumber from Holders")

for row in cursor:
   print("ID = ", row[0])
   print("NAME = ", row[1])
   print("GENDER = ", row[2])
   print("DOB = ", row[3])
   print("ADDRESS = ", row[4])
   print("PhoneNumber = ", row[5])
   print("\n\n\n")

print("Operation done successfully")
conn.close()
