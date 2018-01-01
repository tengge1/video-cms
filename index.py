from flask import Flask, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods = [ 'GET', 'POST' ])
def login():
	if request.method == 'POST':
		pass
	else:
		pass

@app.route('/list/<int:type_id>')
def list(type_id):
	pass

@app.route('/video/<int:video_id>')
def video(video_id):
	pass

@app.route('/setting')
def setting():
	return render_template('setting.html')
