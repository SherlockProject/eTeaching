
	var ltIE8 = false; /*@cc_on ltIE8 = (@_jscript_version < 9); @*/

	String.prototype.is_string = true;
	Array.prototype.is_array = true;

	document.get = function ( ID ) { return document.getElementById( ID ); };
	document.getTags = function ( TAG, PARENT ) {
		if( PARENT.is_string )
			PARENT = document.getElementById( PARENT );

		if( !PARENT )
			PARENT = document;

		return PARENT.getElementsByTagName( TAG.toLowerCase() );
	};
	document.getChildTags = function ( TAG, PARENT ) {
		var
			l = PARENT.children.length,
			list = [],
			i = 0;

		for( ; i < l; i++ ) {
			if( PARENT.children[i].tagName.toLowerCase() == TAG.toLowerCase() )
				list.push( PARENT.children[i] );
		}

		return list;
	};

	window.animate = (function () {
		var
			self = this,

			run = function () {
				TWEEN.update() ? requestAnimationFrame(run) : self.running = false;
			};

		this.running = false;

		return function () {
			for( var i = 0, l = arguments.length; i < l; i++ ) {
				if( arguments[i].stop ) {
					arguments[i].stop();
					arguments[i].reverse();
				}

				arguments[i].start();
			}

			if( !self.running ) {
				self.running = true;
				run();
			}
		};
	})();

	var isIE = (function () {
		return new RegExp("(MSIE |Trident/.*rv:)([0-9]{1,}[\.0-9]{0,})").exec( navigator.userAgent ) != null;
	})();

	window.vp = (function() {
		var obj = window, prop = 'inner';

		if( !( 'innerWidth' in window ) ) {
			prop = 'client';
			obj = document.documentElement || document.body;
		}

		return {
			'height': function () {
				return obj[ prop + 'Height' ];
			},
			'width': function () {
				return obj[ prop + 'Width' ];
			}
		};
	})();

	window.onload = function () {
		var
			imcol	= document.get( 'image-col' ),
			chatcol	= document.get( 'chat-col' ),
			header	= document.get( 'header' ),
			title	= document.get( 'title' ),
			tools	= document.get( 'tools' ),
			input	= document.get( 'input' ),
			form	= document.get( 'form' ),

			lTime	= 1500,
			hTime	= 700,

			h		= window.vp.height(),
			w		= window.vp.width(),
			total	= (h+w) * 2,
			halfw	= w/2 * lTime / total,
			fullw	= w * lTime / total,
			fullh	= h * lTime / total,
			rwid	= 100*(w-h)/w,
			rwid	= rwid < 33.33 ? 33.33 : rwid,
			lwid	= 100 - rwid,

			cTime	= fullh,
			iTime	= 700,
			inTime	= 700,

			interfaceAnim,
			chatcolAnim,
			headerAnim,
			imcolAnim,
			animation,
			current,
			prev,
			i,

			lines = [
				{ o: document.get( 'l1' ), from: { v:0 }, to: { v:50 },  time: halfw, prop: 'width' },
				{ o: document.get( 'l2' ), from: { v:0 }, to: { v:100 }, time: fullh, prop: 'height' },
				{ o: document.get( 'l3' ), from: { v:0 }, to: { v:100 }, time: fullw, prop: 'width' },
				{ o: document.get( 'l4' ), from: { v:0 }, to: { v:100 }, time: fullh, prop: 'height' },
				{ o: document.get( 'l5' ), from: { v:0 }, to: { v:52 },  time: halfw, prop: 'width' }
			],

			lineAnim = function ( line ) {
				return new TWEEN.Tween( line.from )
					.to( line.to, line.time )
					.easing( TWEEN.Easing.Linear.None )
					.onUpdate( (function ( obj, prop ) {
						return function () {
							obj.style[prop] = this.v + '%';
						};
					})( line.o, line.prop ) );
			};

		for( i = 0; i < 5; i++ ) {
			prev = current;
			current = lineAnim( lines[i] );
			animation || (animation = current);
			prev && prev.chain( current );
		}

		interfaceAnim = new TWEEN.Tween( { p: 10000 } )
			.to( { p: 0 }, 1000 )
			.easing( TWEEN.Easing.Quintic.Out )
			.onUpdate( function () {
				tools.style.webkitTransform = 'translateY( ' + this.p/100 + '% )';
				tools.style.transform = 'translateY( ' + this.p/100 + '% )';
				form.style.webkitTransform = 'translateY( ' + this.p/100 + '% )';
				form.style.transform = 'translateY( ' + this.p/100 + '% )';
			} )
			.onComplete( function () {
				input.focus();
			} )
			.onStart( function () {
				document.body.className = document.body.className.replace( /( )?wait/, '' );
			} );

		imcolAnim = new TWEEN.Tween( { w: 0 } )
			.to( { w: lwid*100 }, iTime )
			.easing( TWEEN.Easing.Quintic.InOut )
			.onUpdate( function () {
				imcol.style.width = this.w/100 + 'vw';
			} )
			.onComplete( function () {
				tools.style.visibility = 'visible';
				form.style.visibility = 'visible';

				chat().init();
			} )
			.chain( interfaceAnim );

		chatcolAnim = new TWEEN.Tween( { h: 0 } )
			.to( { h: 10000 }, cTime )
			.easing( TWEEN.Easing.Linear.None )
			.onUpdate( function () {
				chatcol.style.height = this.h/100 + 'vh';
			} )
			.chain( imcolAnim );

		headerAnim = new TWEEN.Tween( { t: 5000, r: 5000, mr: -1900, mt: -450, w: 3332, h: 831, f: 500 } )
			.to( { t: 0, r: 0, mr: 0, mt: 0, w: rwid*100-468, h: 430, f: 187 }, hTime )
			.easing( TWEEN.Easing.Circular.InOut )
			.onStart( function () {
				header.style.lineHeight	= 'normal';
				header.style.textAlign	= 'left';
			} )
			.onUpdate( function () {
				header.style.marginRight = this.mr/100 + 'vw';
				header.style.marginTop = this.mt/100 + 'vw';
				title.style.fontSize = this.f/100 + 'vw';
				header.style.height = this.h/100 + 'vw';
				header.style.width = this.w/100 + 'vw';
				header.style.right = this.r/100 + '%';
				header.style.top = this.t/100 + '%';
			} )
			.onComplete( function () {
				document.body.className += ' ready';
			} )
			.chain( chatcolAnim );

		current.chain( headerAnim );

		chatcol.style.width = rwid + 'vw';
		imcol.style.right = rwid + 'vw';

		if( document.body.id == 'blue' ) {
			document.get( 'scale' ).src = 'images/zoom-scale-blue.jpg';
			document.get( 'zoom-drag' ).getElementsByTagName('img')[0].src = 'images/zoom-drag-blue.jpg';
			document.get( 'upload' ).getElementsByTagName('img')[0].src= 'images/upload-icon-blue.jpg';
			document.get( 'select' ).getElementsByTagName('img')[0].src= 'images/select-icon-blue.jpg';
			document.get( 'lasso' ).getElementsByTagName('img')[0].src= 'images/lasso-icon-blue.jpg';
			document.get( 'hand' ).getElementsByTagName('img')[0].src= 'images/drag-icon-blue.jpg';
			document.get( 'cursor' ).getElementsByTagName('img')[0].src= 'images/cursor-icon-blue.jpg';
		}

		animate( document.body.id != 'blue' ? animation : headerAnim );
	};