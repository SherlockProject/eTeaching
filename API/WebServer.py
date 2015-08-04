from time import gmtime, strftime;
import subprocess, os;

def printTitle( str ):
	print( ( '{0}| ' + str + '{0}' ).format( '\n|------------------------------------------------\n' ) );

printTitle( 'Installing packages from requirements.txt ...' );
subprocess.call( "pip install -r requirements.txt" );#, stdout=subprocess.PIPE
print( 'Done.\n' );
printTitle( 'Web Server starting...' );

from beaker.middleware import SessionMiddleware;
import pymysql, pymysql.cursors, beaker;
from bottle import *;

# Connect to MySQL db
connection = pymysql.connect(
	cursorclass = pymysql.cursors.DictCursor,
	host = 'us-cdbr-iron-east-02.cleardb.net',
	db = 'ad_96cd6dc8fac0ede',
	user = 'b3517254728bb2',
	passwd = '3e269665'
);

"""
create table `conversations` (
	`id` INTEGER(10) UNSIGNED AUTO_INCREMENT,
	`conversation` varchar(100),
	`user` varchar(100),
	`started` timestamp default '0000-00-00 00:00:00',
	`ended` timestamp default now() on update now() ,
	PRIMARY KEY (id)
)
"""

#with connection.cursor() as cursor:
	#cursor.execute( 'drop table if exists `conversations`;' );

	#cursor.execute( """
	#	create table `conversations` (
	#		`id` INTEGER(10) UNSIGNED AUTO_INCREMENT,
	#		`conversation` varchar(100),
	#		`user` varchar(100),
	#		`started` datetime,
	#		`ended` datetime,
	#		PRIMARY KEY (id)
	#	)
	#""" );

	#cursor.execute( 'delete from `conversations`;' );

	#now = strftime( "%Y-%m-%d %H:%M:%S", gmtime() );

	#sql = "insert into `conversations` (`conversation`,`user`,`started`,`ended`) values(%s, %s, %s, %s);";
	#cursor.execute( sql, ('1234','5678',now,now) );
	#connection.commit();

	#cursor.execute( "select * from `conversations`;" );
	#result = cursor.fetchone();
	#print( result );

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

		return s.get( name, 0 );

	def set( self, name, value ):
		s = request.environ.get( 'beaker.session' );
		s[name] = value;
		s.save();

response.delete_cookie( 'beaker.session.id' );

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

def processResponse( r ):
	return r;

def start_conversation():
	session.set( 'user', {} );

	conversation = request.get_cookie( 'beaker.session.id' );

	print( conversation );

	with connection.cursor() as cursor:
		now = strftime( "%Y-%m-%d %H:%M:%S", gmtime() );

		cursor.execute( "delete from `conversations`;" );

		sql = "insert into `conversations` (`conversation`,`user`,`started`,`ended`) values(%s, %s, %s, %s);";
		cursor.execute( sql, (conversation,'5678',now,now) );
		connection.commit();

		cursor.execute( "select * from `conversations`;" );
		result = cursor.fetchone();
		print( result );

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