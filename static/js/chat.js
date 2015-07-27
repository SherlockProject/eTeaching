
	var chat = function () {
		var
			fparent	= document.get( 'form-parent' ),
			cbody	= document.get( 'chat-body' ),
			form	= document.get( 'cform' ),
			input	= document.get( 'input' ),
			submit	= document.get( 'send' ),
			muteBtn	= document.get( 'mute' ),

			session	= null,
			nosend	= true,
			sound	= true,

			trim = function( str ) {
				return str.replace( /^\s+|\s+$/gm, '' );
			},

			scrollToBottom = function () {
				cbody.scrollTop = cbody.scrollHeight;
			},

			escapeHtml = function( text ) {
				return text
					.replace( /&/g, "&amp;" )
					.replace( /</g, "&lt;" )
					.replace( />/g, "&gt;" )
					.replace( /"/g, "&quot;" )
					.replace( /'/g, "&#039;" );
			},

			publish = function ( who, message ) {
				var
					container	= document.createElement( 'div' ),
					text		= document.createElement( 'div' ),
					avatar,
					face,
					eyes;

				container.className	= 'post human';
				text.className		= 'message';
				text.innerHTML		= escapeHtml( message );

				if( who == 'robot' ) {
					avatar	= document.createElement( 'div' );
					face	= document.createElement( 'div' );
					eyes	= document.createElement( 'span' );
					container.className = 'post robot';
					avatar.className = 'avatar';
					face.className = 'face';
					eyes.className = 'eyes';

					avatar.appendChild( face );
					face.appendChild( eyes );
					container.appendChild( avatar );
				}
				container.appendChild( text );
				cbody.appendChild( container );

				scrollToBottom();
			},

			resizeField = function () {
				input.style.height = '19px';

				if( input.offsetHeight != input.scrollHeight ) {
					input.style.marginBottom = input.scrollHeight > 20 ? '2.34vw' : '0px';

					if( input.scrollHeight > 100 ) {
						input.style.overflow = 'auto';
						input.style.height = '100px';
					}
					else {
						input.style.height = input.scrollHeight + 'px';
						input.style.overflow = 'hidden';
					}

					cbody.style.height = 'calc( 100vh - 7.33vw - ' + fparent.offsetHeight + 'px )';
				}
			};

			input.onkeydown = function ( e ) {
				var key = e.keyCode || e.which;
				resizeField();

				e = e || window.event;

				if( key == 13 && !e.shiftKey && !e.shiftKey ) {
					e.preventDefault && e.preventDefault();
					e.returnValue = false;
					chat.send();
					return false;
				}
				if( input.value == '' && key == 38 ) {
					
				}
			};
			submit.onclick	= function () { chat.send(); };
			input.onkeyup	= resizeField;
			input.focus();

		// Session Start
		Ajax.POST( '/process', {
			'data': { 'request': JSON.stringify( {
				'type':		'start',
				'sound':	sound
			} ) },
			'onload': function ( response ) {
				response	= JSON.parse( response.text );
				nosend		= false;

				if( response.type == 'message' ) {
					if( typeof response.text != 'undefined' )
						publish( 'robot', response.text );
				}
			}
		} );

		chat = {
			'send': function () {
				if( trim( input.value ) == '' || nosend )
					return input.focus();

				nosend = true;

				Ajax.POST( '/process#test', {
					'data': { 'request': JSON.stringify( {
						'type':			'message',
						'text':			trim( input.value ),
						'session_id':	session,
						'sound':		sound
					} ) },
					'onload': function ( response ) {
						response	= JSON.parse( response.text );
						nosend		= false;

						if( response.type == 'message' && typeof response.text != 'undefined' ) {
							publish( 'robot', response.text );
						}
					}
				} );

				publish( 'human', input.value );

				cbody.style.height = 'calc( 100vh - 13.58vw )';
				input.placeholder = 'Type here...';
				input.value = '';
				input.focus();
			},

			'mute': function () {
				sound = !sound;
				muteBtn.style.backgroundPosition = ( sound ? 'top ' : 'bottom ' ) + 'left';
				muteBtn.setAttribute( 'title', sound ? 'Sound On' : 'Sound Off' );
			}
		};
	};