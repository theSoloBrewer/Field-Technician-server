'''
Created on Nov 13, 2017

@author: theSoloBrewer
'''
from project import db, MA
import random

from flask_login import UserMixin

class Type(db.Model):
	t_id = db.Column(db.Integer, primary_key=True)
	type_name = db.Column(db.String(64), unique=True)
	#material_location = db.relationship('Material_Location', backref='type',lazy=True)
	def __init__(self,name=''):
		self.type_name = name


class typeSchema(MA.ModelSchema):
	class Meta:
		model = Type
		
class Address(db.Model):
	a_id = db.Column(db.Integer, primary_key=True)
	street = db.Column(db.String(128), unique=True, nullable=False)
	city = db.Column(db.String(128), unique=False, nullable=False)
	state = db.Column(db.String(64), unique=False, nullable=False)
	#geo in the future
	def __init__(self,s='',c='',st=''):
		self.street = s
		self.city = c
		self.state = st
		
class addrSchema(MA.ModelSchema):
	class Meta:
		model = Address
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



material_project = db.Table('material_project',db.Model.metadata,
						 db.Column('project_id',db.Integer, db.ForeignKey('project.p_id')),
						 db.Column('material_id',db.Integer, db.ForeignKey('material.m_id'))
						 )
material_contact = db.Table('material_contact', db.Model.metadata,
						 db.Column('material_id', db.Integer, db.ForeignKey('material.m_id')),
						 db.Column('contact_id', db.Integer, db.ForeignKey('contact_info.c_id'))
						 )
user_project = db.Table('user_project',db.Model.metadata,
						 db.Column('project_id',db.Integer, db.ForeignKey('project.p_id')),
						 db.Column('user_id',db.Integer, db.ForeignKey('user.u_id'))
						 )
labor_project = db.Table('labor_project',db.Model.metadata,
						 db.Column('project_id',db.Integer, db.ForeignKey('project.p_id')),
						 db.Column('labor_id',db.Integer, db.ForeignKey('labor.l_id'))
						 )

class Material_Location(db.Model):
	__tablename__ = 'material_location'
	ml_id = db.Column(db.Integer, primary_key=True)
	ml_name = db.Column(db.String(64), unique=True)
	type_id = db.Column( db.Integer,db.ForeignKey('type.t_id'))
	type = db.relationship('Type')
	def __init__(self,n,t=Type('unknown')):
		self.ml_name = n
		self.type = t

class mlSchema(MA.ModelSchema):
	class Meta:
		model = Material_Location

class Material(db.Model):
	m_id = db.Column(db.Integer, primary_key=True)
	mat_name = db.Column(db.String(64), unique=True)
	mat_model = db.Column(db.String(64))
	mat_manufacture = db.relationship('Contact_Info', secondary=material_contact, backref='material')
	sn = db.Column(db.String(64), unique=True)
	status = db.Column(db.Boolean, nullable=False, default=True)
	type_id = db.Column( db.Integer,db.ForeignKey('type.t_id'))
	type = db.relationship('Type')
	location_id = db.Column(db.Integer, db.ForeignKey('material_location.ml_id'))
	location = db.relationship('Material_Location', backref='material')
	def __init__(self,mtype,material_location,name='',sn=random.getrandbits(24) ,status=''):
		self.mat_name = name
		self.sn = sn
		self.status = status
		self.type = mtype
		self.location = material_location


class materialSchema(MA.ModelSchema):
	class Meta:
		model = Material

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


class Project(db.Model):
	p_id = db.Column(db.Integer, primary_key=True)
	pro_name = db.Column(db.String(64),nullable=False)
	code = db.Column(db.String(6), nullable=False, unique=True)
	description = db.Column(db.Text)
	status_id = db.Column(db.Integer, nullable=True)
	#status = db.relationship(db.Integer, db.ForeignKey()
	location_id = db.Column(db.Integer, db.ForeignKey('address.a_id'))
	location = db.relationship('Address')
	poc_id = db.Column(db.Integer, db.ForeignKey('contact_info.c_id'))
	poc = db.relationship('Contact_Info')
	material = db.relationship('Material', secondary=material_project, backref='project')
	users = db.relationship('User', secondary=user_project, backref='project')
	labor = db.relationship('Labor', secondary=labor_project, backref='project')
	def __init__(self,name,code,desc=None,location=None,material=[],user=[],labor=[]):
		self.pro_name = name
		self.code = code
		self.description = desc
		self.location = location
		self.material = material
		self.user = user
		self.labor = labor

class projectSchema(MA.ModelSchema):
	class Meta:
		model = Project
