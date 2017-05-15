var wp = {
	firstdayloaded: undefined,
	sly: undefined,
	data: undefined,
	dayWidth: undefined,
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
	maxHeight: 3000, // :(
	targetedDayWidth: 300, // px
	dayMargin: 5, // px
	fontSizeMax: 4, // em

	init: function(data) {

		moment.locale('fr');

		wp.data = data;

		// get elements
		var $frame  = $('#myTimeLine');
		var $slidee = $frame.children('ul').eq(0);
		var $wrap   = $frame.parent();

		// get size
		var fullWidth = $( '#page' ).width() ;

		var nFramesTot = data.length;
		var nFramesVisibles = Math.ceil( fullWidth / wp.targetedDayWidth );
		var dayWidth = Math.round( (fullWidth - (nFramesVisibles-1)*wp.dayMargin ) / nFramesVisibles );
		wp.dayWidth = dayWidth;

		// dynamic sly config
		wp.sly_config.pagesBar = $wrap.find('.pages');
		wp.sly_config.scrollBar = $wrap.find('.scrollbar');


		wp.sly = new Sly($frame, wp.sly_config).init();


		wp.firstdayloaded = wp.addNdays(nFramesTot);
		wp.sly.toEnd();


	},
	addNdays: function(iEnd){
		/* ajoute N jours avant i End (après le bouton PLUS)
		   retourne le nouveau iEnd
		*/
		var $plusbutton = $('#plusbutton');

		var N = 7;
		var data = wp.data;
		var iStart = Math.max( iEnd-N, 0 )
		for (var i = iEnd-1; i >= iStart; i--) {
			var $page = $plusbutton.after(
				$('<li />')
					.attr('id', data[i]['date'] )
					.css( {width: wp.dayWidth,  'margin-left':wp.dayMargin} )
					.html( '<h3>'+ wp.formatday(data[i]['date']) +'</h3> <p></p>' )
			);
			wp.fillAday( data[i].date, data[i].mots, wp.maxHeight  );
		}
		wp.sly.reload();
		return iStart;
	},
	formatday: function(d){
		return moment(d, "YYYY-MM-DD").format('dddd Do MMMM');
	},

	clickNgram: function(event){
		// action sur le clic d'un mot
		ngramviewer.selecteddate = moment(event.data.date, "YYYY-MM-DD");
		ngramviewer.addngram(event.data.ngram);
		return false;
	},
	fillAday: function( idDate, blocks, maxHeight ){

		var $mardi = $( '#' + idDate + ' p' ); //li elt.
		var maxWidth = $mardi.width();

		var scoreRange = wp.getRangeScore( blocks );

		// Insert les mots dans le DOM pour avoir leurs taille
		$.each( blocks, function(i, d){
			var $mot = $('<span />')
				.attr('id', d['id'] )
				.css({ fontSize : wp.scaleFontSize(d['score'], scoreRange)+"em" })
				.click( {ngram:d['label'], date:idDate}, wp.clickNgram );

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
	},
	afficherplus(){
		/* Action du bouton Plus, affiche plus de jours */
		console.log('Plus?');
		console.log(wp.firstdayloaded);
		wp.firstdayloaded = wp.addNdays(wp.firstdayloaded);
	}

};


$.getJSON( 'static/data4alldays.json', //urlfor_last10days,
	function(data){ wp.init(data); } //wp.init(data.data);
);
