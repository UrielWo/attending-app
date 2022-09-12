from flask import Flask, request, render_template
from flask_mysqldb import MySQL
import attendance
import paramiko
import mysql.connector
import pandas as pd

app = Flask(__name__)
path_CSV_files = "C:\\Users\\97253\\Documents\\Uriel\\DevOps_Course\\03-Python\\Exercises\\attendance_Ex3\\csv"

@app.route('/Database_table', methods=("POST", "GET"))
def data_table():
    if request.method == 'POST':
        date = request.form['ed']
        host = "192.168.56.101"
        username = "uriel"
        password = "aceituna1"
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        mydb = mysql.connector.connect(
            host="192.168.56.101",
            user="urielw",
            password="password"
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE course_Attendance;")
        query = "SELECT * FROM attendance_data2 WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) = %s ;"
        mycursor.execute(query, [date])
        records = mycursor.fetchall()
        df = pd.DataFrame(columns=['Meeting_Name', 'Meeting_Start_Time', 'Meeting_End_Time', 'Name', 'Attendee_Email', 'Join_Time', 'Leave_Time', 'Attendance_Duration', 'Connection_Type'])
        for row in records:
            df.loc[len(df)] = row
        #attendance.duration_Col(df)  # split Attendance Duration to use min as int for calculations
        return render_template('simple.html',  tables=[df.to_html(classes='data')], titles="")
        client.close()


@app.route('/Main')
def main():
   return render_template("Main.html")

"""@app.route('/table', methods=("POST", "GET"))
def Single_table():
    if request.method == 'POST':
        date = request.form['ed']
        csv_file = "C:\\Users\\97253\\Documents\\Uriel\\DevOps_Course\\03-Python\\Exercises\\attendance_Ex3\\csv\\{}.csv".format(date)
        df = pd.read_csv(csv_file, encoding="UTF-16LE", sep="\t")
        attendance.duration_Col(df)  # split Attendance Duration to use min as int for calculations
        attendance.private_cases(df)  # Convert Hebrew names to English
        Atten_Duration = (df['Duration'].max())  # get max value of from duration column
        pivot = attendance.single_Pivot_Parse(df, Atten_Duration)
        return render_template('simple.html',  tables=[pivot.to_html(classes='data')], titles="")"""

@app.route('/Integrated_table')
def integrated_table():
    summary_tab = attendance.attendance_summary(path_CSV_files)
    return render_template('summary.html', tables=[summary_tab.to_html(classes='data')], titles="")

if __name__ == '__main__':
    app.run(debug=True)


