'''
Created on Dec 12, 2017

@author: theSoloBrewer
'''
from project import FTserver
import views, api

from flask_debugtoolbar import DebugToolbarExtension
import optparse

def flaskrun(app, default_host="127.0.0.1",
				  default_port="5000"):
	"""
	Takes a flask.Flask instance and runs it. Parses
	command-line flags to configure the app.
	"""

	# Set up the command-line options
	parser = optparse.OptionParser()
	parser.add_option("-H", "--host",
					  help="Hostname of the Flask app " + \
						   "[default %s]" % default_host,
					  default=default_host)
	parser.add_option("-P", "--port",
					  help="Port for the Flask app " + \
						   "[default %s]" % default_port,
					  default=default_port)

	# Two options useful for debugging purposes, but
	# a bit dangerous so not exposed in the help message.
	parser.add_option("-d", "--debug",
					  action="store_true", dest="debug",
					  help=optparse.SUPPRESS_HELP)
	parser.add_option("-p", "--profile",
					  action="store_true", dest="profile",
					  help=optparse.SUPPRESS_HELP)

	options, _ = parser.parse_args()

	# If the user selects the profiling option, then we need
	# to do a little extra setup
	if options.profile:
		from werkzeug.contrib.profiler import ProfilerMiddleware

		app.config['PROFILE'] = True
		app.wsgi_app = ProfilerMiddleware(a4pp.wsgi_app,
					   restrictions=[30])
		options.debug = True
	
	app.run(
		debug=options.debug,
		host=options.host,
		port=int(options.port)
	)
	
	

if __name__ == "__main__":
	FTserver.debug = True
	FTserver.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	DebugToolbarExtension(FTserver)
	FTserver.run()