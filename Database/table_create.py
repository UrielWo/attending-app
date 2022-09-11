import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="urielw",
  password="password",
  database="course_Attendance"
)
mycursor = mydb.cursor()

mycursor.execute("select database();")
record = mycursor.fetchone()
print("You're connected to database: ", record)
mycursor.execute('DROP TABLE IF EXISTS attendance_data;')

mycursor.execute("CREATE TABLE attendance_data2(Meeting_Name varchar(255),"
                 "Meeting_Start_Time varchar(255),Meeting_End_Time varchar(255)"
                 ",Name varchar(255),Attendee_Email varchar(255),Join_Time varchar"
                 "(255),Leave_Time varchar(255),Attendance_Duration varchar(255)"
                 ",Connection_Type varchar(255));")