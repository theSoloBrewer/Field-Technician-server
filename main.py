'''
Created on Dec 12, 2017

@author: theSoloBrewer
'''
from project import FTserver, db
from flask_login import LoginManager, login_user, logout_user
from flask import send_from_directory, render_template, request, flash, redirect, url_for
from models import User, Contact_Info

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
	flash('User successfully registered')
	return redirect(url_for('login'))



@FTserver.route('/login', methods=['GET','POST'])
def login():
	# Here we use a class of some kind to represent and validate our
	# client-side form data. For example, WTForms is a library that will
	# handle this for us, and we use a custom LoginForm to validate.
	if request.method == 'GET':
		return render_template('login.html', active='login')

	username = request.form['user']
	password = request.form['pass']
	registered_user = User.query.filter_by(username=username,password=password).first()
	if registered_user is None:
		flash('Username or Password is invalid' , 'error')
		return redirect(url_for('login'))
	login_user(registered_user)
	flash('Logged in successfully')
	return redirect(request.args.get('next') or url_for('index'))

@FTserver.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@FTserver.route('/static/<path:asset>/<page>')
def send_static( asset, page):
	print('asset')
	return send_from_directory("/templates/static/" +asset, page, active=page, title=page)

@FTserver.route('/<page>')
def path(page):
	return render_template(page + ".html", active=page, title=page)
@FTserver.route('/favicon.ico')
def favicon():
	return ''
@FTserver.route('/')
@FTserver.route('/index')
def index():
	return render_template('index.html', title='Home', active='home')

if __name__ == "__main__":

	FTserver.run(debug=True)
