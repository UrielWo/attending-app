import mysql.connector
import pandas as pd
import os
import pysftp
import paramiko

def table_create():
	path = "/home/uriel/course/csv_files"

	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None 
	with pysftp.Connection('185.164.16.144', username='urielw', password='banana234', cnopts=cnopts) as sftp:
	    print ("connection succesfully")
	    sftp.cwd('/var/tmp/csv_files/')
	    directory_structure = sftp.listdir_attr()
	    for attr in directory_structure:
	    	fileName = attr.filename
	    	remoteFilePath = '/var/tmp/csv_files/{}'.format(fileName)
	    	localFilePath = '/home/uriel/course/csv_files/{}'.format(fileName)
	    	sftp.get(remoteFilePath, localFilePath)

	mydb = mysql.connector.connect(host="127.0.0.1", user="uriel",password="password", database="attendance")
	mycursor = mydb.cursor()
	mycursor.execute("select database();")
	record = mycursor.fetchone()
	print("You're connected to database: ", record)
	mycursor.execute('DROP TABLE IF EXISTS attendance_data;')

	mycursor.execute("CREATE TABLE attendance_data(Meeting_Name varchar(255),Meeting_Start_Time varchar(255),Meeting_End_Time varchar(255),Name varchar(255),Attendee_Email varchar(255),Join_Time varchar(255),Leave_Time varchar(255),Attendance_Duration varchar(255),Connection_Type varchar(255));")

	csv_files_list = list(map(lambda x: os.path.join(os.path.abspath(path), x), os.listdir(path)))
		
	#insert each csv to table
	for files in csv_files_list:
	    df = pd.read_csv(files, encoding="UTF-16LE", sep="\t")
	    df = df.where((pd.notnull(df)), None)
	    for i, row in df.iterrows():# here %S means string values
	    	sql = "INSERT INTO attendance.attendance_data (Meeting_Name, Meeting_Start_Time, Meeting_End_Time, Name,Attendee_Email,Join_Time,Leave_Time,Attendance_Duration, Connection_Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	    	mycursor.execute(sql, tuple(row))
	    	mydb.commit()
	print("table created")

if __name__ == '__main__':
	table_create()
       
        

