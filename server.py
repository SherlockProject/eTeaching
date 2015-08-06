from API import WebServer # also install requirements.txt
from sherlock.watson.watson import WatsonService
import bottle, requests, shutil
from API.WebServer import user
import json as JSON

textToSpeech = WatsonService(
	url = 'https://stream.watsonplatform.net/text-to-speech/api',
	auth = ( '24bdc1c7-3e7e-46e5-9e6b-17d45d15b14e', '3W29o3r6OV5X' ),
	operations = {
		'synthesize': {
			'method': 'GET',
			'path': '/v1/synthesize'
		}
	}
);

hello = 'Hello, my name is Sherlock! If you want to see a photo - type "image". If you\'d like to hear some latin - just type anything.';

# Returning text (http://localhost:4242/process)
@bottle.post( '/process' )
def process_func():
	request = JSON.loads( bottle.request.POST[ 'request' ] );

	if( request['type'] == 'start' ):
		WebServer.start_conversation();

		response = {
			'type': 'message',
			'text': hello
		};

	elif( request['type'] == 'message' ):
		# import pprint;
		# pprint.pprint( user.info ); # user and conversation identifiers
		# pprint.pprint( user.data ); # empty dict that can be used throughout the whole conversation as storage
		                              # e.g. you can store all images that you have already used in a conversation

		# Example usage of user.data: counting answers
		if( 'iteration' not in user.data ):
			user.data['iteration'] = 0;

		user.data['iteration'] = user.data['iteration'] + 1;
		print( '\nIteration: ' + str( user.data['iteration'] ) );

		# If user typed "image" in the text box
		if( request['text'] == 'image' ):

			#-------------------------- Download Random Image --------------------------------------------------------#
			r = requests.get( 'http://lorempixel.com/600/400/', stream=True );
			image_path = 'static/work_images/' + str( user.info['userID'] ) + '.jpg';

			if r.status_code == 200:
				with open( image_path, 'wb' ) as f:
					r.raw.decode_content = True;
					shutil.copyfileobj( r.raw, f );
			#---------------------------------------------------------------------------------------------------------#

			response = {
				'type': 'image',
				'text': 'Take a look at this photo. Can you help me find Waldo?',
				'path': image_path,
				'imid': 'image-identifier' # unique identifier (image name/id in a database)
			};

		else:

			#-------------------------- Generate Random Text ---------------------------------------------------------#
			randomText = requests.get( 'http://loripsum.net/api/plaintext/1/short/headers' ).text.split( '\n' )[0];
			#---------------------------------------------------------------------------------------------------------#

			response = {
				'type': 'message',
				'text': randomText
			};

	else:
		response = {
			'type': 'error',
			'error': 'Unknown request type'
		};

	# generate sound file
	if( request['sound'] == 'on' and response['text'] and response['text'] != hello ):
		result = textToSpeech.synthesize( params = {
			'voice': 'en-US_MichaelVoice',
			'text': response['text'],
			'accept': 'audio/wav'
		} );

		# Save File
		ogg = open( 'static/sound/answer.wav', 'wb' );
		ogg.write( result );

	return WebServer.processResponse( response );

WebServer.start();

# cf push eTeaching -p eTeaching -m 512M -n eteaching