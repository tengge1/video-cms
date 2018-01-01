from flask import Flask, url_for, render_template, request, session, json
from base.sqlhelper import SqlHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'video-cms'

@app.route('/')
def index():
	if session.get('username') == None:
		return render_template('login.html')
	else:
		return render_template('index.html')

@app.route('/login', methods = [ 'GET', 'POST' ])
def login():
	if request.method == 'POST':
		username = request.values.get('username')
		password = request.values.get('password')
		helper = SqlHelper()
		sql = 'select * from user where username=%s and password=%s'
		result = helper.fetchone(sql, (username, password));
		if(result == None):
			return json.dumps({
				'success': 'false',
				'msg': 'Username or password is wrong!'
				});
		else:
			session['username'] = result['username']
			return json.dumps({
				'success': 'true',
				'msg': 'Login succeed!'
				});
	else:
		return render_template('login.html')

@app.route('/list/<int:type_id>')
def list(type_id):
	pass

@app.route('/video/<int:video_id>')
def video(video_id):
	pass

@app.route('/setting')
def setting():
	return render_template('setting.html')
