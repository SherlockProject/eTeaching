
	var chat = function () {
		var
			iParent	= document.get( 'image-parent' ),
			fparent	= document.get( 'form-parent' ),
			cbody	= document.get( 'chat-body' ),
			form	= document.get( 'cform' ),
			input	= document.get( 'input' ),
			submit	= document.get( 'send' ),
			muteBtn	= document.get( 'mute' ),
			image	= document.get( 'image' ),
			thg		= document.get( 'thinking' ),

			audio	= null,
			nosend	= true,
			sound	= true,

			playAudio = function ( path, config ) {
				if( audio )
					audio.pause();

				audio = new Audio( path );

				if( typeof config !== 'undefined' ) {
					if( config.onstart )
						audio.oncanplay = config.onstart;
					if( config.onend )
						audio.onended = config.onend;
				}

				audio.play();
			},

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
					bigcont		= document.createElement( 'div' ),
					tmbParent,
					bigcont,
					avatar,
					mouth,
					face,
					eyes,
					tmb;

				container.className	= 'post human';
				bigcont.className	= 'bigcont';
				text.className		= 'message';

				if( who == 'robot' ) {
					avatar	= document.createElement( 'div' );
					face	= document.createElement( 'div' );
					eyes	= document.createElement( 'span' );
					mouth	= document.createElement( 'img' );
					container.className = 'post robot eyes-up';
					avatar.className = 'avatar';
					mouth.className = 'mouth';
					face.className = 'face';
					eyes.className = 'eyes';

					if( !thg ) {
						thg	= document.createElement( 'span' );
						thg.setAttribute( 'id', 'thinking' );
					}

					avatar.setAttribute( 'title', 'Thinking...' );

					avatar.appendChild( thg );
					avatar.appendChild( face );
					face.appendChild( eyes );
					container.appendChild( avatar );
				}
				else {
					text.innerHTML = escapeHtml( message );
					bigcont.appendChild( text );
					container.appendChild( bigcont );
				}

				cbody.appendChild( container );

				scrollToBottom();

				if( who == 'robot' ) {
					return function( message, thumb ) {
						text.innerHTML = escapeHtml( message );
						bigcont.appendChild( text );
						container.appendChild( bigcont );

						avatar.setAttribute( 'title', '' );
						container.className = 'post robot';
						thg.parentNode.removeChild( thg );

						mouth.setAttribute( 'src', 'images/mouth.gif' );

						avatar.appendChild( mouth );

						if( typeof thumb != 'undefined' ) {
							tmbParent	= document.createElement( 'div' );
							tmb			= document.createElement( 'img' );
							tmbParent.className = 'thumb';

							tmb.onload = scrollToBottom;
							tmb.src = thumb + '?rand=' + Math.random();

							tmbParent.appendChild( tmb );
							bigcont.appendChild( tmbParent );
						}

						scrollToBottom();

						if( sound ) {
							var path = 'sound/answer.ogg?rand=' + Math.random();

							if( message == 'Hello, my name is Sherlock! If you want to see a photo - type "image". If you\'d like to hear some latin - just type anything.' )
								path = 'sound/hello.ogg';

							playAudio( path, {
								'onstart': function () { if( sound ) mouth.src = 'images/mouth-talk.gif?a=5'; },
								'onend': function () { mouth.src = 'images/mouth.gif'; }
							} );
						}
					};
				}
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

		return {
			'init': function () {
				// Session Start
				Ajax.POST( '/process', {
					'data': { 'request': JSON.stringify( {
						'type':		'start',
						'sound':	sound ? 'on' : 'off'
					} ) },
					'onload': function ( response ) {
						response	= JSON.parse( response.text );
						nosend		= false;

						switch( response.type ) {
							case 'message':
								if( typeof response.text != 'undefined' )
									publish( 'robot' )( response.text );
							break;

							case 'error':
								publish( 'robot' )( 'Error: ' + response.error );
							break;
						}
					}
				} );

				chat = {
					'send': function () {
						var onloaded, text = trim( input.value );

						if( trim( input.value ) == '' || nosend )
							return input.focus();

						nosend = true;

						window.setTimeout( function() {
							onloaded = publish( 'robot' );

							cbody.style.height = 'calc( 100vh - 13.58vw )';
							input.placeholder = 'Type here...';
							input.value = '';

							Ajax.POST( '/process', {
								'data': { 'request': JSON.stringify( {
									'type':			'message',
									'text':			text,
									'sound':		sound ? 'on' : 'off'
								} ) },
								'onload': function ( response ) {
									response	= JSON.parse( response.text );
									nosend		= false;

									switch( response.type ) {
										case 'message':
											if( typeof response.text != 'undefined' )
												onloaded( response.text );
										break;

										case 'image':
											if( typeof response.text != 'undefined' )
												onloaded( response.text, response.thumb.replace( /^static\//, '' ) );

											if( typeof response.path != 'undefined' ) {
												if( !image ) {
													image = document.createElement( 'img' );
													image.setAttribute( 'id', 'image' );

													iParent.appendChild( image );
												}

												image.style.display = 'none';

												image.onload = function () {
													image.style.display = 'inline';
												};

												image.src = response.path.replace( /^static\//, '' ) + '?rand=' + Math.random();
											}
										break;

										case 'error':
											onloaded( 'Error: ' + response.error );
										break;
									}
								}
							} );
						}, 500 );

						publish( 'human', text );

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
			}
		};
	};