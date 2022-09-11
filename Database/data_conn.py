import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="urielw",
  password="password"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE course_Attendance")

#Check if Database Exists
mycursor.execute("SHOW DATABASES")
for x in mycursor:
  print(x)
