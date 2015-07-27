from sherlock.watson.watson import WatsonService
from sherlock.response.response import Answer
from API import WebServer
import json as JSON
import bottle

textToSpeech = WatsonService(
	url = 'https://stream.watsonplatform.net/text-to-speech-beta/api',
	auth = ( 'ce3219f1-fae8-40d0-ae1b-e1f17fa4074c', '6MN0tdcfU4f6' ),
	operations = {
		'synthesize': {
			'method': 'GET',
			'path': '/v1/synthesize'
		}
	}
);

# Returning text (http://localhost:4242/process)
@bottle.post( '/process' )
def process_func():
	req = JSON.loads( bottle.request.POST[ 'request' ] );

	if( req['type'] == 'start' ):
		bottle.response.delete_cookie( 'beaker.session.id' );
		response = {
			'type': 'message',
			'text': "Hello, my name is ET! How you doin'?"
		};

	elif( req['type'] == 'message' ):
		response = {
			'type': 'message',
			'text': 'answer something'
		};

	else:
		response = {
			'type': 'error',
			'error': 'Unknown request type'
		};

	if( req['sound'] == 'on' and response['text'] ):
		# generate sound file
		pass;

	return response;

WebServer.start();
