from datetime import datetime, timedelta;
from time import gmtime, strftime;
import subprocess, os;
import pprint;

def printTitle( str ):
	print( ( '{0}| ' + str + '{0}' ).format( '\n|------------------------------------------------\n' ) );

printTitle( 'Installing packages from requirements.txt ...' );
subprocess.call( "pip install -r requirements.txt", stdout=subprocess.PIPE );
print( 'Done.\n' );
printTitle( 'Web Server starting...' );

from beaker.middleware import SessionMiddleware;
import pymysql, pymysql.cursors, beaker;
from PIL import Image;
from bottle import *;
import beaker;

# Connect to MySQL db
def connect():
	global connection;

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
create table `users` (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
)
"""

class ManageSessions:
	def get( self, name ):
		s = request.environ.get( 'beaker.session' );

		return s.get( name, 0 );

	def set( self, name, value ):
		s = request.environ.get( 'beaker.session' );
		s[name] = value;
		s.save();

class ManageUsers:
	@property
	def data( self ):
		return session.get( 'user' )['data'];

	@property
	def info( self ):
		return session.get( 'user' )['info'];

def processResponse( r ):
	if( r['type'] == 'image' ):
		thumb_path = 'static/work_images/' + str( user.info['userID'] ) + '.thumb.jpg';

		im = Image.open( r['path'] );
		im.thumbnail( (128,128) );
		im.save( thumb_path, "JPEG" );

		r['thumb'] = thumb_path;

	now = strftime( "%Y-%m-%d %H:%M:%S", gmtime() );
	conversationID = user.info['conversationID'];

	connect();

	with connection.cursor() as cursor:
		sql = 'update `conversations` set `ended` = "%s" where `id` = "%s"';
		cursor.execute( sql, (now,conversationID) );
		connection.commit();

	return r;

def start_conversation():
	userID = request.get_cookie( 'user' );

	connect();

	with connection.cursor() as cursor:
		now = strftime( "%Y-%m-%d %H:%M:%S", gmtime() );

		if( userID is None ):
			cursor.execute( "insert into `users` (`id`) values (NULL)" );
			cursor.execute( "select * from `users` order by `id` desc;" );
			row = cursor.fetchone();

			response.set_cookie( 'user', str(row['id']), expires = datetime.today() + timedelta( weeks=52 ) );
			userID = row['id'];

		sql = "insert into `conversations` (`user`,`started`,`ended`) values(%s, %s, %s);";
		cursor.execute( sql, (userID,now,now) );
		connection.commit();

		cursor.execute( "select `id` from `conversations` order by `id` desc;" );
		row = cursor.fetchone();

		session.set( 'user', { 'info': { 'userID': userID, 'conversationID': row['id'] }, 'data': {} } );

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

session_opts = {
	'session.type': 'file',
	'session.data_dir': './API/sessions',
	'session.auto': True
};
app = SessionMiddleware( app(), session_opts );

response.delete_cookie( 'beaker.session.id' );
session = ManageSessions();
user = ManageUsers();