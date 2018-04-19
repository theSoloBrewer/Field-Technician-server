'''
Created on Oct 18, 2017

@author: theSoloBrewer
'''
from migrate.versioning import api
import os.path, sys
import imp
import project
from models import *
import optparse

def managerun(cmd='db_migrate', app='FTserver', database='db'):
	"""
	Takes a flask.Flask instance and runs it. Parses
	command-line flags to configure the app.
	"""
	this = sys.modules[__name__]
	# Set up the command-line options
	parser = optparse.OptionParser()
	parser.add_option("-c", "--cmd",
					  help="Command to run " + \
						   "[default %s]" % cmd,
					  default=cmd)
	parser.add_option("-a", "--app",
					  help="App to be managed " + \
						   "[default %s]" % app,
					  default=app)
	parser.add_option("-d", "--db",
					  help="Database to manager" + \
						   "[default %s]" % database,
					  default=database)

	# Two options useful for debugging purposes, but
	# a bit dangerous so not exposed in the help message.
	'''parser.add_option("-d", "--debug",
					  action="store_true", dest="debug",
					  help=optparse.SUPPRESS_HELP)
	parser.add_option("-p", "--profile",
					  action="store_true", dest="profile",
					  help=optparse.SUPPRESS_HELP)'''

	options, _ = parser.parse_args()
	this.db = getattr(this.project, options.db, None)
	tmpapp = getattr(this.project,options.app, None)
	this.SQLALCHEMY_DATABASE_URI = tmpapp.config['SQLALCHEMY_DATABASE_URI']
	this.SQLALCHEMY_MIGRATE_REPO = tmpapp.config['SQLALCHEMY_MIGRATE_REPO']
	getattr(this, options.cmd)()


def db_migrate():
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
	tmp_module = imp.new_module('old_model')
	old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	exec(old_model, tmp_module.__dict__)
	script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
	open(migration, "wt").write(script)
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('New migration saved as ' + migration)
	print('Current database version: ' + str(v))

def db_create():
	print('Creating new database' )
	db.create_all()
	if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
		api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
		api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	else:
		api.version
		
def db_upgrade():
	api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('Current database version: ' + str(v))
	
def db_downgrade():
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
	v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
	print('Current database version: ' + str(v))
	

managerun()