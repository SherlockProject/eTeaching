from API.watson import WatsonService
from API import WebServer
from API.bottle import *

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

# Returning text (http://localhost:4242/speak-to-me)
@post( '/speak-to-me' )
def speak_to_me():
	# English - male voice
	voice = 'VoiceEnUsMichael';

	# Text sent from the chat
	user_input = request.POST[ 'input' ];

	# If empty - exit
	if( user_input is None ):
		return;

	# Say <sentence> (say command)
	if( user_input[0:4].lower() == 'say ' ):
		message = user_input[4:];

	# Scary goodbye message
	elif( user_input.lower() in [ 'bye', 'goodbye', 'chao', 'bye, et', 'goodbye, et', 'bye et', 'goodbye et' ] ):
		message = 'Goodbye, human. Now, prepare to be terminated!';

	else:
		message = 'Hello, my name is E.T.';

	# Transform text to audio
	result = textToSpeech.synthesize( params={
		'accept': 'audio/ogg;codecs=opus',
		'voice': voice,
		'text': message
	} );

	# Save it as a file
	ogg = open( 'static/sounds/answer.ogg', 'wb' );
	ogg.write( result );

	return message;

WebServer.start();