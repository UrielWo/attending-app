from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/Attendance', methods = ['POST', 'GET'])

def Attendance():
	if request.method == 'POST':
		date = request.form['ed']
		return date

app.add_url_rule('/', 'Attendance',Attendance) #add the url to the localhost (http://127.0.0.1:5000/Attendance)

if __name__ == '__main__':
	app.run(debug=True)


# the html and the py speaking!!
# dont forget do test!
