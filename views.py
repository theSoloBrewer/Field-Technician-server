from project import FTserver, db
from flask_login import LoginManager, login_user, logout_user, current_user
from flask import send_from_directory, render_template, request, flash, redirect, url_for, jsonify
from models import *
import api
login = LoginManager(FTserver)


@login.user_loader
def load_user(u_id):
	return User.query.get(int(u_id))


@FTserver.route('/register' , methods=['GET','POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html', active='none')
	cInfo = Contact_Info(request.form['fname'] + ' ' + request.form['lname'], request.form['email'], request.form['phone'])
	user = User(request.form['username'] , request.form['password'], cInfo)
	db.session.add(user)
	db.session.commit()
	flash('User successfully registered', 'success')
	return redirect(url_for('login'))



@FTserver.route('/login', methods=['GET','POST'])
def login():
	# Here we use a class of some kind to represent and validate our
	# client-side form data. For example, WTForms is a library that will
	# handle this for us, and we use a custom LoginForm to validate.
	if request.method == 'GET':
		return render_template('login.html', active='login')
	error = None
	username = request.form['user']
	password = request.form['pass']
	registered_user = User.query.filter_by(username=username,password=password).first()
	if registered_user is None:
		flash(u'Invalid username or password. Please try again!', 'danger')
	else:
		login_user(registered_user)
		flash('You were successfully logged in', 'success')
		return redirect(url_for('indexView'))

	return render_template('login.html', error = error)


@FTserver.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@FTserver.route('/static/<path:asset>/<page>')
def send_static( asset, page):
	print('asset')
	return send_from_directory("/templates/static/" +asset, page, active=page, title=page, db=db)

@FTserver.route('/materials', methods=['GET','POST'])
def materialView():
	if request.method == 'POST' and request.form['dist']:
		ciS = ciSchema()
		d = Contact_Info.query.get(request.form['dist_id'])
		return jsonify(ciS.dump(d).data)
	types = Type.query
	dist = Contact_Info.query.filter(Contact_Info.c_type_id=='7').all()
	return render_template("materials.html", active='materials', title='Materials', types=types, distributors=dist)

@FTserver.route('/project/<string:act>', methods=['GET','POST'])
def projectView(act):
	if act == 'new':
		return render_template("project.html", active='cProject', title='New Project', project=None)
	if act == 'list':
		p = Project.query.all()
		return render_template("project_list.html", active='eProject', title='Projects List', projects=p)
	if act == 'edit':
		p = Project.query.filter_by(code = request.form['code']).first()
		return render_template("project.html", active='eProject', title='Edit Project', project=p)
	return render_template("project.html", active='eProject', title='Project List')

@FTserver.route('/calendar')
def calendarView():
	return render_template("calendar.html", active='calendar', title='Calendar')


@FTserver.route('/favicon.ico')
def favicon():
	return ''
@FTserver.route('/')
@FTserver.route('/index')
def indexView():
	if current_user.is_authenticated:
		p = Project.query.all()

		return render_template('dashboard.html', title='Dashboard', active='dashboard', projects=p)
	return render_template('index.html', title='Home', active='home')
