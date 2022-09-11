import mysql.connector
import pandas as pd
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="urielw",
    password="password",
    database="course_Attendance")

mycursor = mydb.cursor()
path = "/home/uriel/PythonExe/attendance_csv_files"
csv_files_list = list(map(lambda x: os.path.join(os.path.abspath(path), x), os.listdir(path)))

for files in csv_files_list:
    df = pd.read_csv(files, encoding="UTF-16LE", sep="\t")
    for i, row in df.iterrows():
        # here %S means string values
        sql = "INSERT INTO course_Attendance.attendance_data2 (Meeting_Name,Meeting_Start_Time,Meeting_End_Time,Name,Attendee_Email,Join_Time,Leave_Time,Attendance_Duration, Connection_Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql, tuple(row))
        print("Record inserted")
        mydb.commit()