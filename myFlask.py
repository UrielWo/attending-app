from flask import Flask, request, render_template
import attendance
import pandas as pd

app = Flask(__name__)

@app.route('/Single', methods=['POST', 'GET'])
def getDate():
    if request.method == 'POST':
        date = request.form['ed']
        return render_template('single_Report.html', name=date)# dataframe here i need to show the single pivot
app.add_url_rule('/', 'Single', getDate) # add the url to the localhost (http://127.0.0.1:5000/Single)

@app.route('/hello')
def index():
   return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

# dont forget do test!
