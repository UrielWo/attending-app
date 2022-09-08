from flask import Flask, request, render_template
import attendance
import pandas as pd

app = Flask(__name__)
path_CSV_files = "C:\\Users\\97253\\Documents\\Uriel\\DevOps_Course\\03-Python\\Exercises\\attendance_Ex3\\csv"
@app.route('/Main')
def main():
   return render_template("Main.html")

@app.route('/table', methods=("POST", "GET"))
def Single_table():
    if request.method == 'POST':
        date = request.form['ed']
        csv_file = "C:\\Users\\97253\\Documents\\Uriel\\DevOps_Course\\03-Python\\Exercises\\attendance_Ex3\\csv\\{}.csv".format(date)
        df = pd.read_csv(csv_file, encoding="UTF-16LE", sep="\t")
        attendance.duration_Col(df)  # split Attendance Duration to use min as int for calculations
        attendance.private_cases(df)  # Convert Hebrew names to English
        Atten_Duration = (df['Duration'].max())  # get max value of from duration column
        pivot = attendance.single_Pivot_Parse(df, Atten_Duration)
        return render_template('simple.html',  tables=[pivot.to_html(classes='data')], titles="")

@app.route('/Integrated_table')
def integrated_table():
    summary_tab = attendance.attendance_summary(path_CSV_files)
    return render_template('summary.html', tables=[summary_tab.to_html(classes='data')], titles="")

if __name__ == '__main__':
    app.run(debug=True)

# dont forget do test!

