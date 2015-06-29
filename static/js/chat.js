
	chat = (function () {
		var
			messages = document.getElementById( 'messages' ),
			submit = document.getElementById( 'submit' ),
			input = document.getElementById( 'input' ),
			cform = document.getElementById( 'cform' ),

			scrollToBottom = function () {
				messages.scrollTop = messages.scrollHeight;
			},

			playAudio = function ( path ) {
				new Audio( path ).play();
			},

			trim = function( str ) {
				return str.replace( /^\s+|\s+$/gm, '' );
			};

		input.onkeydown = function ( e ) {
			e = e || window.event;

			if( (e.keyCode || e.which) == 13 ) {
				if( e.preventDefault )
					e.preventDefault();
				e.returnValue = false;
				chat.send();
				return false;
			}
		};

		submit.onclick = function () { chat.send(); };

		input.focus();

		return {
			'nosend': false,

			'send': function () {
				if( trim( input.value ) == '' || chat.nosend )
					return;

				chat.nosend = true;

				if( !window.fun || !funny || !funny( input ) ) {
					Ajax.POST( 'http://localhost:4242/speak-to-me', {
						'data': { 'input': input.value },
						'onload': function ( response ) {
							playAudio( 'sounds/answer.ogg' );

							chat.publish( 'you', response.text );
							chat.nosend = false;
						}
					} );

					chat.publish( 'me', input.value );
				}
			},

			'publish': function ( who, data ) {
				var
					div1 = document.createElement( 'div' ),
					div2 = document.createElement( 'div' ),
					img = document.createElement( 'img' );

				div1.className = 'message ' + ( who == 'me' ? 'me' : 'you' );
				div2.className = 'text';

				img.src = 'images/' + ( who == 'me' ? 'fry.jpg' : 'bender.jpg' );
				img.className = 'avatar';

				div1.appendChild( img );
				div1.appendChild( div2 );

				div2.appendChild( document.createTextNode( data ) );

				messages.appendChild( div1 );

				scrollToBottom();

				if( who == 'me' )
					input.value = '';
			}
		};
	})();