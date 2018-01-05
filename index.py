from flask import Flask, url_for, render_template, request, session, json, send_from_directory, current_app, g
from config.config import *
from base.sqlhelper import SqlHelper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'video-cms'

def init():
	g.website_name = website_name
	g.username = session.get('username')
	if g.username is not None:
		helper = SqlHelper()
		sql = "select * from category"
		g.categories = helper.fetchall(sql)

@app.route('/')
@app.route('/index')
@app.route('/index/<int:category_id>')
def index(category_id = None):
	init()
	if g.username == None:
		return render_template('login.html')
	else:
		g.category_id = category_id
		helper = SqlHelper()
		if category_id is None:
			sql = "select * from video"
			g.videos = helper.fetchall(sql)
		else:
			sql = "select * from video where category_id=%s"
			g.videos = helper.fetchall(sql, (category_id,))

		return render_template('index.html')

@app.route('/login', methods = [ 'GET', 'POST' ])
def login():
	init()
	if request.method == 'POST':
		username = request.values.get('username')
		password = request.values.get('password')
		helper = SqlHelper()
		sql = 'select * from user where username=%s and password=%s'
		result = helper.fetchone(sql, (username, password));
		if result is None:
			return json.dumps({
				'success': 'false',
				'msg': 'Username or password is wrong!'
				})
		else:
			session['username'] = result['username']
			return json.dumps({
				'success': 'true',
				'msg': 'Login success!'
				})
	else:
		return render_template('login.html')

@app.route('/logout', methods = [ 'GET', 'POST' ])
def logout():
	session.clear()
	return json.dumps({
		'success': 'true',
		'msg': 'Logout success!'
		})

@app.route('/video/<int:id>')
def video(id):
	init()
	helper = SqlHelper()
	sql = "select * from video where id=%s"
	g.video = helper.fetchone(sql, (id,))
	return render_template('video.html')

@app.route('/manage/category')
def category_manage():
	init()
	g.pageSize = request.values.get('pageSize')
	g.pageNum = request.values.get('pageNum')

	if g.pageSize is None:
		g.pageSize = 10
	if g.pageNum is None:
		g.pageNum = 1

	g.pageNum = int(g.pageNum)
	g.pageSize = int(g.pageSize)
	
	helper = SqlHelper()
	sql = "select count(1) total from category"
	g.total = helper.fetchone(sql)['total']
	g.totalPage = int(g.total / g.pageSize) if g.total % g.pageSize == 0 else g.total // g.pageSize + 1

	sql = "select * from category order by id desc limit %s,%s "
	g.rows = helper.fetchall(sql, (g.pageSize * (g.pageNum - 1), g.pageSize))
	
	g.category_id = 'system'
	return render_template('manage/category.html');

@app.route('/manage/category/edit', methods = [ 'GET','POST' ])
def category_edit():
	init()
	id = request.values.get('id')
	id = 0 if id is None else int(id)
	helper = SqlHelper()
	if request.method == 'POST':
		name = request.values.get('name')
		if id == 0:
			sql = "insert into category (name) values (%s)"
			helper.execute(sql, (name,))
		else:
			sql = "update category set name=%s where id=%s"
			helper.execute(sql, (name, id))
		return json.dumps({
			'success': 'true',
			'msg': 'Save success!'
			})
	else:
		g.id = id
		g.name = ''
		if g.id > 0:
			sql = "select name from category where id=%s"
			category = helper.fetchone(sql, (id,))
			g.name = category['name']
		g.category_id = 'system'
		return render_template('manage/category_edit.html');

@app.route('/manage/category/delete/<int:id>', methods = ['POST'])
def category_delete(id):
	init()
	helper = SqlHelper()
	sql = "delete from category where id=%s"
	helper.execute(sql, (id,))
	return json.dumps({
		'success': 'true',
		'msg': 'Delete success!'
		})

@app.route('/manage/video')
def video_manage():
	init()
	return render_template('manage/video.html')

@app.route('/manage/user')
def user_manage():
	init()
	g.pageSize = request.values.get('pageSize')
	g.pageNum = request.values.get('pageNum')

	if g.pageSize is None:
		g.pageSize = 10
	if g.pageNum is None:
		g.pageNum = 1

	g.pageNum = int(g.pageNum)
	g.pageSize = int(g.pageSize)
	
	helper = SqlHelper()
	sql = "select count(1) total from user"
	g.total = helper.fetchone(sql)['total']
	g.totalPage = int(g.total / g.pageSize) if g.total % g.pageSize == 0 else g.total // g.pageSize + 1

	sql = "select * from user order by id desc limit %s,%s "
	g.rows = helper.fetchall(sql, (g.pageSize * (g.pageNum - 1), g.pageSize))
	
	g.category_id = 'system'
	return render_template('manage/user.html');

@app.route('/manage/user/edit', methods = [ 'GET','POST' ])
def user_edit():
	init()
	id = request.values.get('id')
	id = 0 if id is None else int(id)
	helper = SqlHelper()
	if request.method == 'POST':
		username = request.values.get('username')
		password = request.values.get('password')
		name = request.values.get('name')
		if id == 0:
			sql = "insert into user (username,password,name) values (%s,%s,%s)"
			helper.execute(sql, (username,password,name))
		else:
			sql = "update user set username=%s,password=%s,name=%s where id=%s"
			helper.execute(sql, (username, password, name, id))
		return json.dumps({
			'success': 'true',
			'msg': 'Save success!'
			})
	else:
		g.id = id
		g.username = ''
		g.password = ''
		g.name = ''
		if g.id > 0:
			sql = "select username,password,name from user where id=%s"
			category = helper.fetchone(sql, (id,))
			g.username = category['username']
			g.password = category['password']
			g.name = category['name']
		g.category_id = 'system'
		return render_template('manage/user_edit.html');

@app.route('/manage/user/delete/<int:id>', methods = ['POST'])
def user_delete(id):
	init()
	helper = SqlHelper()
	sql = "delete from user where id=%s"
	helper.execute(sql, (id,))
	return json.dumps({
		'success': 'true',
		'msg': 'Delete success!'
		})

@app.route('/upload/<path:path>')
def send_upload(path):
	return send_from_directory('upload', path)

