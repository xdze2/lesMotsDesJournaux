var data_filename = 'data.json'
$.getJSON(data_filename, function (data) {
		// get elements
		var $frame  = $('#myTimeLine');
		var $slidee = $frame.children('ul').eq(0);
		var $wrap   = $frame.parent();

		// window size
		var windowHeight = $( window ).height();
		var windowWidth = $( window ).width();

		$wrap.css({ height : windowHeight });

		var maxHeight = windowHeight - 150;


    // data
		$.each( data, function(i, d){
			var day = d['day']
			var blocks = d['mots']

			$slidee.append( $('<li />').attr('id', day ) );
			//$('<li />').appendTo( $slidee ).text(day); //, { id : day }

			fillAday( day, blocks, maxHeight  );
		});

		// param and coll Sly
		$frame.sly({
			horizontal: 1,
			itemNav: 'basic',
			smart: 1,
			activateOn: 'click',
			mouseDragging: 1,
			touchDragging: 1,
			releaseSwing: 1,
			startAt: 0,
			scrollBar: $wrap.find('.scrollbar'),
			scrollBy: 1,
      scrollTrap: 1,
      scrollSource:  $frame,
			pagesBar: $wrap.find('.pages'),
			activatePageOn: 'click',
			speed: 300,
			elasticBounds: 1,
			easing: 'easeOutExpo',
			dragHandle: 1,
			dynamicHandle: 1,
			clickBar: 1
		});
});


function fillAday( id, blocks, maxHeight  ){
	// selectionne le jour
	var $mardi = $( '#' + id );
	$mardi.css({ position:'relative', height:maxHeight});

	// insert les mots dans le DOM pour avoir leurs taille
	$.each( blocks, function(i, d){
		var $mot = $('<span />', {
			id : d['id'],
			css : { fontSize : d['size']+"em"	,
							padding: '4px',
							position : 'absolute' }
		});
		$mot.text( d['label'] );
		$mot.appendTo( $mardi )

		d['w'] = $mot.outerWidth();
		d['h'] = $mot.outerHeight();
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
		}

	});


};
