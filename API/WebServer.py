import subprocess;
import beaker;
import os;

def printTitle( str ):
	print( ( '{0}| ' + str + '{0}' ).format( '\n|------------------------------------------------\n' ) );

printTitle( 'Installing packages from requirements.txt ...' );

subprocess.call( "pip install -r requirements.txt", stdout=subprocess.PIPE );
print( 'Done.\n' );

printTitle( 'Web Server starting...' );

from beaker.middleware import SessionMiddleware
from bottle import *;

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': 300,
	'session.data_dir': './API/sessions',
	'session.auto': True
};
app = SessionMiddleware( app(), session_opts );

class ManageSessions:
	def get( self, name ):
		s = request.environ.get( 'beaker.session' );

		if( name == 'user' and s.get( 'user', 0 ) == 0 ):
			session.set( 'user', {} );
			return session.get( 'user' );

		return s.get( name, 0 );

	def set( self, name, value ):
		s = request.environ.get( 'beaker.session' );
		s[name] = value;
		s.save();

session = ManageSessions();

def user( value = None ):
	if value != None:
		if not isinstance( value, dict ):
			raise ValueError( '"user" accepts argument of type "dict"' );
		else:
			session.set( 'user', value );
	else:
		u = session.get( 'user' );

		return u;

def start_conversation():
	response.delete_cookie( 'beaker.session.id' );

def start( host = 'localhost', port = 4242 ):
	host = os.getenv( 'VCAP_APP_HOST', host );
	port = int( os.getenv( 'PORT', port ) );

	# Set up index page
	@route( '/' )
	def index_page():
		return static_file( 'index.html', root='./static' );

	# Static files
	@route('/<filepath:path>')
	def server_static(filepath):
		return static_file(filepath, root='./static');

	run( host = host, port = port, app=app );
