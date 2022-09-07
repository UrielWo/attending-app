from flask import Flask, request
import attendance

app = Flask(__name__)

@app.route('/Single', methods=['POST', 'GET'])

def getDate():
    if request.method == 'POST':
        date = request.form['ed']
        return date # here i need to show the single pivot

app.add_url_rule('/', 'Single', getDate) # add the url to the localhost (http://127.0.0.1:5000/Attendance)

if __name__ == '__main__':
    app.run(debug=True)

# dont forget do test!
