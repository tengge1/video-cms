from flask import Flask, url_for, render_template, request, session, json, send_from_directory
from base.sqlhelper import SqlHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'video-cms'

@app.route('/')
@app.route('/index')
@app.route('/index/<int:category_id>')
def index(category_id = None):
	if session.get('username') == None:
		return render_template('login.html')
	else:
		sql = "select * from category"
		helper = SqlHelper()
		categories = helper.fetchall(sql)

		videos = None
		if category_id is None:
			sql = "select * from video"
			videos = helper.fetchall(sql)
		else:
			sql = "select * from video where category_id=%s"
			videos = helper.fetchall(sql, (category_id,))

		return render_template('index.html', data = {
			'categories': categories,
			'current_id': category_id,
			'videos': videos
			});

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
				'msg': 'Login success!'
				});
	else:
		return render_template('login.html')

@app.route('/logout', methods = [ 'GET', 'POST' ])
def logout():
	session.clear()
	return json.dumps({
		'success': 'true',
		'msg': 'Logout success!'
		});

@app.route('/video/<int:video_id>')
def video(video_id):
	pass

@app.route('/upload/<path:path>')
def send_upload(path):
	return send_from_directory('upload', path)

@app.route('/setting')
def setting():
	return render_template('setting.html')
