from flask import Flask, request, render_template
import attendance
#import paramiko
import mysql.connector
import pandas as pd
from table_create import table_create
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

#table_create() # make a flag for this function

mydb = mysql.connector.connect(host="127.0.0.1", user=os.getenv("DB_USER") ,password=os.getenv("DB_PASSWORD"), database="attendance")
mycursor = mydb.cursor()
mycursor.execute("select database();")
record = mycursor.fetchone()
print("You're connected to database in flask: ", record)
mycursor.execute("USE attendance;")

@app.route('/Main')
def main():
    return render_template("Main.html")


@app.route('/Database_table', methods=("POST", "GET"))
def data_table():
    if request.method == 'POST':
        date = request.form['ed']
        query = "SELECT * FROM attendance_data WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) = %s ;"
        mycursor.execute(query, [date])
        records = mycursor.fetchall()
        df = pd.DataFrame(columns=['Meeting_Name', 'Meeting_Start_Time', 'Meeting_End_Time', 'Name', 'Attendee_Email', 'Join_Time', 'Leave_Time', 'Attendance_Duration', 'Connection_Type'])
        for row in records:
            df.loc[len(df)] = row
        attendance.duration_Col(df)  # split Attendance Duration to use min as int for calculations
        attendance.private_cases(df)  # Convert Hebrew names to English
        Atten_Duration = (df['Duration'].max())  # get max value of from duration column
        pivot = attendance.single_Pivot_Parse(df, Atten_Duration)
        pivot = pivot.astype(str).replace(r'\.0$', '', regex=True)
        pivot['Time_On_Lesson'] = pivot['Time_On_Lesson'].astype(str) + '%'  # add % to percent
        return render_template('simple.html',  tables=[pivot.to_html(classes='data')], titles="")
        client.close()
        
        
@app.route('/Integrated_table')
def integrated_table():
    integrated_Table = pd.DataFrame()
    mycursor.execute("SELECT DISTINCT mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) FROM attendance_data WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3);")
    dates = mycursor.fetchall()
    for d in dates:
    	mycursor.execute("SELECT * FROM attendance_data WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) = %s ;", d)
    	records = mycursor.fetchall()
    	df = pd.DataFrame(columns=['Meeting_Name', 'Meeting_Start_Time', 'Meeting_End_Time', 'Name', 'Attendee_Email', 'Join_Time', 'Leave_Time', 'Attendance_Duration', 'Connection_Type'])
    	for row in records:
    		df.loc[len(df)] = row
    	attendance.duration_Col(df)  # split Attendance Duration to use min as int for calculations
    	attendance.private_cases(df)  # Convert Hebrew names to English
    	Atten_Duration = (df['Duration'].max())  # get max value of from duration column
    	pivot = attendance.single_Pivot_Parse(df, Atten_Duration)
    	integrated_Table = pd.concat([integrated_Table, pivot], axis=0)
    integrated_Count = attendance.Daily_Attendence(integrated_Table)
    integrated_Pivot = attendance.integrated_Table_Parse(integrated_Table)
    final_Table = attendance.merge_daily_to_time(integrated_Count, integrated_Pivot)
    return render_template('summary.html', tables=[final_Table.to_html(classes='data')], titles="")


if __name__ == '__main__':
    app.run(debug=True)

#mycursor.execute("SELECT DISTINCT mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) FROM attendance_data2 WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3);")
#dates = mycursor.fetchall() # check how to send the dates to droplist in html
