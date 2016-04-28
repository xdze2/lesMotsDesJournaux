

$.getJSON(urlfor_last10days, function (data) {
		moment.locale('fr'); // 'fr'
		formatday = function (d){
			return moment(d, "YYYY-MM-DD").format('dddd Do MMMM');
		}

	 data = data.data;
		// get elements
		var $frame  = $('#myTimeLine');
		var $slidee = $frame.children('ul').eq(0);
		var $wrap   = $frame.parent();

		// window size
		var windowHeight = $( window ).height();
		var windowWidth = $( window ).width() - 5*2 ;// 5:margin

		$wrap.css({ height : windowHeight - 10  }); // safety margin

		var maxHeight = windowHeight - 150;

		var targetedDayWidth = 300;
		var nFramesVisibles = Math.ceil( windowWidth/targetedDayWidth );
		var actualDayWidth = Math.round( windowWidth / nFramesVisibles );
		var nFramesTot = data.length;

    // data
		$.each( data, function(i, d){
			var day = d['date']
			var blocks = d['mots']

			$slidee.append( $('<li />')
				.attr('id', day )
				.css( {width:actualDayWidth, height:maxHeight} )
				.html( '<h3>'+ formatday(d['date']) +'</h3> <p></p>' )
			);

			fillAday( day, blocks, maxHeight  );
		});
		//console.log( $slidee.children('li').length );

		/* - Call Sly  (scrolling lib) - */

		var sly_config = {
			horizontal: 1,
			itemNav: 'basic',
			smart: 1,
			activateOn: null, //'click',
			mouseDragging: 0,
			touchDragging: 1,
			releaseSwing: 1,
			startAt: nFramesTot - nFramesVisibles,
			scrollBar: $wrap.find('.scrollbar'),
			scrollBy: 1,
			scrollTrap: 1,
			scrollSource:  $('body'),//$frame,
			pagesBar: $wrap.find('.pages'),
			activatePageOn: 'click',
			speed: 300,
			elasticBounds: 1,
			easing: 'easeOutExpo',
			dragHandle: 1,
			dynamicHandle: 1,
			clickBar: 1
		};
		$frame.sly( sly_config );
});


function fillAday( id, blocks, maxHeight  ){
	// selectionne le jour
	var $mardi = $( '#' + id + ' p' );
	$mardi.css({ position:'relative', height:maxHeight});

	// Scale score -> size
	var scoreMin = blocks[0].score;
  var scoreMax = blocks[0].score;

	 blocks.forEach(function (mot, index, blocks) {
		 if(index > 0) {
			 if(mot.score < scoreMin){
				 scoreMin = mot.score;
			 }
			 if(mot.score > scoreMax) {
				 scoreMax = mot.score;
			 }
		 }
	 });

function scaleFontSize(score){
				 var sizeMax = 4;
 					var scoreNormed =  (score-scoreMin)/( 1.0*scoreMax - scoreMin );
          var size = Math.round(  scoreNormed*(sizeMax - 1)  ) + 1;
					return size;
 }
	// insert les mots dans le DOM pour avoir leurs taille
	$.each( blocks, function(i, d){
		var $mot = $('<a />', {
			id : d['id'],
			href: 'freqs/'+d['label'],
			css : { fontSize : scaleFontSize(d['score'])+"em"	, //d['score']+
							padding: '0px 10px 0px 0px', // t r b l
							'white-space': 'nowrap',
							position : 'absolute',
							'line-height': '95%'
						 }
		});
		var label = arrangeLabel( d['label'] )
		$mot.html( label ); // insert html: pas cool ??
		$mot.appendTo( $mardi )

		d['w'] = $mot.outerWidth();
		d['h'] = $mot.outerHeight();

		var maxWidth = $mardi.width();

		if (d['w']>maxWidth ){
		/* ReScale la taille de police, si mot trop long */
			var newSize = scaleFontSize(d['score'])/d['w']*maxWidth*0.97;
			$mot.css( {'fontSize': newSize+'em' } ); //, "font-weight":"bold"
			d['w'] = $mot.outerWidth();
			d['h'] = $mot.outerHeight();
			//console.log( 'not fit '+d['label']+' '+newSize );
		}

	});

	// go for Packer
	var wFrame = $mardi.width();
	var hFrame = 10*$mardi.height();

	blocks.sort( function(a, b){
		var aire = b.w*b.h - a.w*a.h;
		return aire;
	});
	packer = new Packer( wFrame, hFrame );
	packer.fit(blocks);

	// move the blocks
	$.each( blocks, function(i, d){
		var $mot = $( '#'+d['id'] );

		if (d.fit){
			$mot.css( {  top:d.fit.y, left:d.fit.x } );
		} else { console.log( ' no fit.packer '+d['label'] ); }

	});


};


function arrangeLabel( label ){
// ajoute un retour a la ligne quand mots de la même longueur
	var mots = label.split(" ");

	if( mots.length === 2 && Math.abs(mots[0].length - mots[1].length)<3 ){
		// console.log( label );
		return mots[0]+'<br />'+mots[1];
	} else { 	return label;  }
}

function dayLabel( day ){
// formate le 'jour' en français
	var chiffres = day.split("-");

	if( mots.length === 2 && Math.abs(mots[0].length - mots[1].length)<3 ){
		// console.log( label );
		return mots[0]+'<br />'+mots[1];
	} else { 	return label;  }
}
