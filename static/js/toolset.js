
	var toolset = function () {
		var
			zoomPerc	= document.get( 'zoom-percent' ),
			zoomDrag	= document.get( 'zoom-drag' ),
			zoomOut		= document.get( 'zoom-out' ),
			zoomIn		= document.get( 'zoom-in' ),
			upload		= document.get( 'upload' ),
			select		= document.get( 'select' ),
			cursor		= document.get( 'cursor' ),
			lasso		= document.get( 'lasso' ),
			scale		= document.get( 'scale' ),
			hand		= document.get( 'hand' );

		var
			lis = document.getTags( 'li', 'tools' ),
			l = lis.length,
			i = 0;

		for( ; i < l; i++ ) {
			lis[i].style.opacity = '.3';
		}

		toolset = {
			'disable': function ( config ) {
				// ...
			}
		};
	};