'''
Created on Dec 11, 2017

@author: theSoloBrewer
'''

from flask import request
from flask_restful import Resource, Api
import flask_restful as restful
import pandas as pd
from sqlalchemy import exc, or_, and_
from sqlalchemy.orm.exc import NoResultFound
import models, project, sys, random, csv, json, requests, time
from pip._vendor.pyparsing import Empty

api = Api(project.FTserver)

class IterMixin(object):
	def __iter__(self):
		for attr, value in self.__dict__.iteritems():
			yield attr, value

class SessionManager(Resource):
	def __init__(self):
		self.session = project.db.session

	def push(self, obj):
		try:
			self.session.add(obj)
			self.session.commit()
			return{'status' : 'ok'}
		except exc.SQLAlchemyError:
			print(vars(exc.SQLAlchemyError))
			restful.abort(500)
	def remove(self, obj):
		try:
			self.session.delete(obj)
			self.session.commit()
			return{'status':'ok'}
		except exc.SQLAlchemyError:
			print(vars(exc.SQLAlchemyError))
			restful.abort(500)

SM = SessionManager()

class Contact_Info(Resource):
	def get(self):
		pass
	def put(self):
		pass
api.add_resource(Contact_Info, '/api/contact')
class Project(Resource):
	def get(self, project_code=None):
		if project_code is None:
			pros_dict = dict()
			pros = models.Project.query.all()
			for index, pro in enumerate(pros):
				pros_dict[index] = {'code':pro.code,'name':pro.pro_name,'status':pro.status_id}
			return{'projects': pros_dict}
		else:
			pro = models.Project.query.filter_by(code=project_code).first()
			return{pro.code: pro.pro_name}

	def put(self):
		name = request.json['name']
		code = request.json['code']
		if name is not None and code is not None:
			pro = models.Project(name, code)
			if SM.push(pro)['status'] is 'ok':
				print(pro)

	def delete(self, project_code):
		print('deleting project code number:'+project_code)
		pro = models.Project.query.filter_by(code=project_code).first()
		if SM.remove(pro)['status'] is 'ok':
			return{'status':'ok'}
api.add_resource(Project, '/api/project', '/api/project/<string:project_code>')

class Mat_Loc(Resource):
	def new_Loc(self, request):
		pass

	def update_Loc(self, request, cloc):
		if len(cloc) > 1:
			restful.abort(501)
		else:
			ml = models.Material_Location.query.filter_by(ml_name=cloc[0].ml_name).one()
			ml.type = cloc[0]
		return ml

	def get(self, request, loc_id, loc_type):

		l = models.Type.query.filter_by(t_id=loc_id).all()
		return l

	def getByName(self,request, loc_name, loc_type):
		try:
			l = models.Material_Location.query.filter_by(ml_name=loc_name).all()
			ml = self.update_Loc(request, l)
		except NoResultFound:
			self.new_Loc(request, loc_type)
		return ml

class Type(Resource):
	def new_Type(self, request):
		try:
			t = models.Type(request['name'])
		except:
			restful.abort(501)
		return t

	def update_type(self, request, type_name=None):
		if type_name is None:
			try:
				type_name= request['name']
				return self.get(request, type_name)
			except:
				restful.abort(501)

	def get(self, type_id=None):
		if type_id is None:
			print('get type')
			restful.abort(404)
		t = models.Type.query.filter_by(t_id=type_id).one()
		return t

	def getByName(self, type_name=None):
		if type_name is None:
			restful.abort(404)
		t = models.Type.query.filter_by(type_name=type_name).one()
		return t

class Materials(Resource):
	def new_material(self, request, project_code=None):
		try:
			###
			### does this material already exist
			###
			###
			mat = models.Material.query.filter(
				or_(
					models.Material.sn==request['mat_sn'],
					and_(
						models.Material.location.has(models.Material_Location.ml_name==request['mat_loc']['name']),
						models.Material.mat_name==request['mat_name']
					)
			)).one()
			restful.abort(409)
		except NoResultFound:
			#
			# Material is new
			#
			print("is new")
			try:# see if type exists or need to create new
				ml = Mat_Loc()
				t = Type()
				ml_req = request['mat_loc']
				mat_type = t.getByName(request['type']['name'])
				# see if material location exists or need to create new
				mlt = t.getByName(ml_req['type']['name'])
				mat_loc = ml.getByName(request, ml_req['name'], mlt)
				#mlt = models.Type.query.filter_by(type_name=request['mat_loc']['type']['name']).one()
				#mat_loc = models.Material_Location.query.filter_by(ml_name=m_loc.name).one()
			except NoResultFound:
				try:
					mlt = models.Type(request['mat_loc']['type']['name'])
					mat_loc = models.Material_Location(request['mat_loc']['name'],mlt)
				except:
					raise ValueError("can't create Material Location")
			mat_name = request['mat_name']
			mat_sn = request['mat_sn']
			if mat_sn is None or mat_sn:
				mat_sn = random.getrandbits(24)
			mat = models.Material(mat_type, mat_loc, mat_name, mat_sn)


		#
		## is also not assigned to a project yet
		#

		if project_code is None:
			if SM.push(mat)['status'] is 'ok':
				return{'status':'ok'}
		else:
			try:
				p = models.Project.query.filter_by(code=project_code).one()
				p.material.append(mat)
				SM.push(p)
				return{'status':'ok'}
			except NoResultFound:
				restful.abort(404)
				return{'status':'err'}
		return{'status':'err'}

	def update_material(self, request, mat_id, project_code=None):
		if mat_id is None:
			try:
				print(json.dumps(request))
				mat_id = models.Material.query.filter_by(mat_name=request['mat_name']).one().m_id
			except:
				restful.abort(404)
		mat = models.Material.query.filter_by(m_id=mat_id).one()
		print('update', mat_id)
		if project_code is None:
			try:
				SM.push(mat)
			except:
				restful.abort(501)
		else:
			try:
				p = models.Project.query.filter_by(code=project_code).one()
				SM.push(p)
			except:
				restful.abort(501)

	def get(self, project_code=None):
		mat_dict = dict()
		if project_code is None:
			mats = models.Material.query.all()
		elif project_code is not None:
			if models.Project.query.filter_by(code=project_code).all() is None:
				return{'status':'err'}
			mats = models.Material.query.filter(models.Material.project.any(code=project_code)).all()
		for mat in mats:
			schema = models.materialSchema()
			result = schema.dump(mat)
			mat_dict[mat.m_id]=result.data
		if not bool(mat_dict):
			restful.abort(404)
		return mat_dict

	def put(self,project_code=None,mat_id=None):
		#
		## is a new material
		#
		print('put')
		try:
			print('new')
			self.new_material(request.json, project_code)
		except :
			print('old')
			self.update_material( request.json,mat_id, project_code)

	def delete(self, mat_id):
		mID = models.Material.query.filter_by(m_id=mat_id).first()
		if SM.remove(mID)['status'] is 'ok':
			return{'status':'ok'}

api.add_resource(Materials,'/api/project/<string:project_code>/material/',
				 '/api/material/',
				 '/api/project/<string:project_code>/material/<int:mat_id>/',
				 '/api/material/<int:mat_id>/')

class Import(Resource):
	def readFile(self, filename):
		try:
			df = filename
			return df
		except IOError:
			raise ValueError('cant open file')

	def put(self):
		try:
			df = pd.read_csv(request.json['filename'])
			d = df.to_dict(orient="records")
			row = []
			for r in d:
				url = "http://localhost:5000/project/"+r['proCode']+"/material/"
				head = {'Content-Type':'application/json'}
				data = {
						"type":
							{
							"name":r['matType']
							},
						"mat_loc":
							{
							"name":r['mlLocation'],
							"type":{"name": r['mlType']}
							},
					   "mat_name":r['matName'],
					   "mat_sn": str(r['matSN'])
					   }
				try:
					row.append(r)
					print('sending')
					#requests.put(url,headers=head,data=json.dumps(data))
					Materials.new_material(data)
					print('request complete')
				except TypeError as err:
					print("request error: ",err)
					restful.abort(409)


		except ValueError as err:
			print(err)
			#return restful.abort(501)

api.add_resource(Import, '/api/import')
