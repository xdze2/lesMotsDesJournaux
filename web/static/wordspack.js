var wp = {
	sly_config: {
		horizontal: 1,
		itemNav: 'basic',
		smart: 1,
		activateOn: null, //'click',
		mouseDragging: 0,
		touchDragging: 1,
		releaseSwing: 1,
		scrollBy: 1,
		scrollTrap: 1,
		// scrollSource:  $('.wrap'),//$frame,
		activatePageOn: 'click',
		speed: 300,
		elasticBounds: 1,
		easing: 'easeOutExpo',
		dragHandle: 1,
		dynamicHandle: 1,
		clickBar: 1
	},
	targetedDayWidth: 300, // px
	dayMargin: 5, // px
	fontSizeMax: 4, // em
	init: function(data) {
		console.log('Hello / init');

		moment.locale('fr');

		// get elements
		var $frame  = $('#myTimeLine');
		var $slidee = $frame.children('ul').eq(0);
		var $wrap   = $frame.parent();

		// get size
		var fullWidth = $( '#page' ).width() ;

		var maxHeight = 3000; // :(

		var nFramesTot = data.length;
		var nFramesVisibles = Math.ceil( fullWidth / wp.targetedDayWidth );
		var dayWidth = Math.round( (fullWidth - (nFramesVisibles-1)*wp.dayMargin ) / nFramesVisibles );


		// dynamic sly config
		wp.sly_config.pagesBar = $wrap.find('.pages');
		wp.sly_config.scrollBar = $wrap.find('.scrollbar');
		wp.sly_config.startAt = nFramesTot - nFramesVisibles;

		// data
		for (var i = 0; i < nFramesTot; i++) {
			$slidee.append(
				$('<li />')
					.attr('id', data[i]['date'] )
					.css( {width:dayWidth,  'margin-left':wp.dayMargin} )
					.html( '<h3>'+ wp.formatday(data[i]['date']) +'</h3> <p></p>' )
			);
			wp.fillAday( data[i].date, data[i].mots, maxHeight  );
		};

		$frame.sly( wp.sly_config );
	},
	formatday: function(d){
		return moment(d, "YYYY-MM-DD").format('dddd Do MMMM');
	},

	clickNgram: function(event){
		ngramviewer.addngram(event.data); return false;
	},
	fillAday: function( idDate, blocks, maxHeight ){

		var $mardi = $( '#' + idDate + ' p' );
		var maxWidth = $mardi.width();

		var scoreRange = wp.getRangeScore( blocks );

		// Insert les mots dans le DOM pour avoir leurs taille
		$.each( blocks, function(i, d){
			var $mot = $('<span />')
				.attr('id', d['id'] )
				.css({ fontSize : wp.scaleFontSize(d['score'], scoreRange)+"em" })
				.click( d['label'], wp.clickNgram );

			//var label = wp.arrangeNgram( d['label'] )
			$mot.html( d['label'] );
			$mot.appendTo( $mardi );

			d['w'] = $mot.outerWidth(true);
			d['h'] = $mot.outerHeight(true);

			// Modifie la taille de police si le mot est trop long
			if (d['w']>maxWidth ){
				var newSize = wp.scaleFontSize(d['score'], scoreRange)/d['w']*maxWidth*0.97;
				$mot.css( {'fontSize': newSize+'em' } ); //, "font-weight":"bold"
				d['w'] = $mot.outerWidth(true);
				d['h'] = $mot.outerHeight(true);
			};
		});

		// Go for Packer
		blocks.sort( function(a, b){
			return b.w*b.h - a.w*a.h; // Aire
		});
		packer = new Packer( maxWidth, 4000 ); // w=Width, h=Infini
		packer.fit(blocks);

		// Move the blocks
		var maxHeight = 0;
		$.each( blocks, function(i, d){
			var $mot = $( '#'+d['id'] );
			if (d.fit){
				$mot.css( {  top:d.fit.y, left:d.fit.x, position:'absolute' } );
				if( d.fit.y+d.h > maxHeight  ){maxHeight = d.fit.y+d.h};
			}
			else { console.log( ' no fit.packer '+d.h ); }

		});
		$mardi.css({height:maxHeight});

	},
	getRangeScore: function(blocks){
		var scoreMin = blocks[0].score;
		var scoreMax = blocks[0].score;
		var score;
		for (var i = 0; i < blocks.length; i++) {
			score = blocks[i].score;
			if( score < scoreMin){
				scoreMin = score;
			}
			if( score > scoreMax) {
				scoreMax = score;
			}
		};
		return {'min':scoreMin, 'max':scoreMax};
	},
	scaleFontSize: function(score, range){
		var scoreNormed =  (score-range.min)/( range.max - range.min );
		var size = Math.round(  scoreNormed*(wp.fontSizeMax - 1)  ) + 1;
		return size;
	},
	arrangeNgram: function( ngram ){
		// pour les 2-grams:
		// ajoute un retour a la ligne quand mots de la même longueur
		var ngram = ngram.split(" ");
		if( ngram.length === 2 && Math.abs(ngram[0].length - ngram[1].length)<3 ){
			ngram = ngram[0]+'<br />'+ngram[1];
		}
		return ngram;
	}


};


$.getJSON( urlfor_last10days,
	function(data){ wp.init(data.data); }
);
