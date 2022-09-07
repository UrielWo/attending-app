from flask import Flask, request, render_template
import attendance
import pandas as pd
app = Flask(__name__)
""""@app.route('/Single', methods=['POST', 'GET'])
def getDate():
    if request.method == 'POST':
        date = request.form['ed']
        return render_template('single_Report.html', name=date) # dataframe here i need to show the single pivot
app.add_url_rule('/', 'Single', getDate) # add the url to the localhost (http://127.0.0.1:5000/Single)"""

@app.route('/Main')
def main():
   return render_template("Main.html")

@app.route('/table', methods=("POST", "GET"))
def html_table():
    if request.method == 'POST':
        date = request.form['ed']
        csv_file = "C:\\Users\\97253\\Documents\\Uriel\\DevOps_Course\\03-Python\\Exercises\\attendance_Ex3\\csv\\{}.csv".format(date)
        df = pd.read_csv(csv_file, encoding="UTF-16LE", sep="\t")
        attendance.duration_Col(df)  # split Attendance Duration to use min as int for calculations
        attendance.private_cases(df)  # Convert Hebrew names to English
        Atten_Duration = (df['Duration'].max())  # get max value of from duration column
        pivot = attendance.single_Pivot_Parse(df, Atten_Duration)
        return render_template('simple.html',  tables=[pivot.to_html(classes='data')], titles=pivot.columns.values)


if __name__ == '__main__':
    app.run(debug=True)

# dont forget do test!
