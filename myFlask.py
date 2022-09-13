from flask import Flask, request, render_template
import attendance
import paramiko
import mysql.connector
import pandas as pd
from itertools import chain

app = Flask(__name__)
# connecting to remote database

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

@app.route('/Main')
def main():
    mycursor.execute("SELECT DISTINCT mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) FROM attendance_data2 WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3);")
    dates = mycursor.fetchall() #check how to send the list to drop list in html
   return render_template("Main.html")
@app.route('/Database_table', methods=("POST", "GET"))
def data_table():
    if request.method == 'POST':
        date = request.form['ed']
        query = "SELECT * FROM attendance_data2 WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) = %s ;"
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
    mycursor.execute("SELECT DISTINCT mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) FROM attendance_data2 WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3);")
    dates = mycursor.fetchall()
    #return dates# list of lists
    #dates = [["2022-08-01"],["2022-08-02"],["2022-07-26"]]
    for d in dates:
        mycursor.execute("SELECT * FROM attendance_data2 WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) = %s ;", d)
        records = mycursor.fetchall()
        df = pd.DataFrame(
            columns=['Meeting_Name', 'Meeting_Start_Time', 'Meeting_End_Time', 'Name', 'Attendee_Email', 'Join_Time',
                     'Leave_Time', 'Attendance_Duration', 'Connection_Type'])
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

    #return integrated_Table





"""@app.route('/Integrated_table')
def integrated_table():                      #version 2
    Atten_Duration = {}
    mycursor.execute("SELECT * FROM attendance_data2")
    records = mycursor.fetchall()
    df = pd.DataFrame(
        columns=['Meeting_Name', 'Meeting_Start_Time', 'Meeting_End_Time', 'Name', 'Attendee_Email', 'Join_Time',
                 'Leave_Time', 'Attendance_Duration', 'Connection_Type'])
    for row in records:
        df.loc[len(df)] = row
    # make a dictionary for max time lesson by day
    mycursor.execute("SELECT distinct mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) AS Date FROM attendance_data2")
    lesson_Dates = mycursor.fetchall()
    lesson_Dates = list(chain(*lesson_Dates))
    for dates in lesson_Dates:
        query_max_time = "SELECT SUBSTRING_INDEX(Attendance_Duration,' ',1) AS Attendance_Duration FROM attendance_data2 " \
                         "WHERE mid(SUBSTRING_INDEX(Meeting_Start_Time,' ',1),3) = %s " \
                         "ORDER BY CAST(SUBSTRING_INDEX(Attendance_Duration,' ',1) AS UNSIGNED) DESC LIMIT 1;"
        mycursor.execute(query_max_time, [dates])
        lists_max_lesson_time = mycursor.fetchall()
        max_lesson_time = []
        for sublist in lists_max_lesson_time:
            for item in sublist:
                max_lesson_time.append(item)
        s = [str(integer) for integer in max_lesson_time]
        a_string = "".join(s)
        res = int(a_string)
        Atten_Duration.update({dates: res})
    return (Atten_Duration)


    integrated_Count = attendance.Daily_Attendence(df)
    attendance.duration_Col(df)
    #Atten_Duration = (df['Duration'].max())# not true
    #f = df.assign(Time_On_Lesson=lambda x: round(x['Duration'] / Atten_Duration * 100))  # calculate percent of attendence
    integrated_Pivot = attendance.integrated_Table_Parse(df)
    merge_T = attendance.merge_daily_to_time(integrated_Count, integrated_Pivot)
    return render_template('summary.html', tables=[merge_T.to_html(classes='data')], titles="")"""

"""@app.route('/Integrated_table')
def integrated_table():
    summary_tab = attendance.attendance_summary(path_CSV_files)
    return render_template('summary.html', tables=[summary_tab.to_html(classes='data')], titles="")"""

if __name__ == '__main__':
    app.run(debug=True)


