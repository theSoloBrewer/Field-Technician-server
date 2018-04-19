from project import db, MA

from flask_login import UserMixin

class User(UserMixin, db.Model):
	u_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), unique=True, nullable=False)
	password = db.Column(db.String(256), nullable=True)
	type_id = db.Column( db.Integer,db.ForeignKey('type.t_id'))
	type = db.relationship('Type')
	contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.c_id'))
	contact = db.relationship('Contact_Info')
	address_id = db.Column(db.Integer, db.ForeignKey('address.a_id'))
	address = db.relationship('Address')
	def __init__(self,username,password,contact):
		self.username = username
		self.password = password
		self.contact = contact


	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.u_id)
		
		
class Labor(db.Model):
	l_id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('user.u_id'))
	user = db.relationship('User')
	def __init__(self,user='',time=float(0.0),task=''):
		self.time = time
		self.task = task
		self.user = user
	def __repr__(self):
		return '<%s:%s>' % (
			self.__class__.__name__,
			self.task
		)

class Contact_Info(db.Model):
	__tablename__ = 'contact_info'
	c_id = db.Column(db.Integer, primary_key=True)
	contact_name = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(128), unique=True)
	phone = db.Column(db.Integer, unique=False)
	addr_id = db.Column(db.Integer, db.ForeignKey('address.a_id'))
	addr = db.relationship('Address')
	c_type_id = db.Column( db.Integer,db.ForeignKey('type.t_id'))
	c_type = db.relationship('Type')

	def __init__(self, name,email='',phone=''):
		self.contact_name = name
		self.email = email
		self.phone = phone


class ciSchema(MA.ModelSchema):
	class Meta:
		model = Contact_Info		