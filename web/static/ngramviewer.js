var marcopolo_config = {
  url: urlfor_getNgrams,
  formatItem: function (data, $item) {
    return data.ngram;
  },
  formatData: function (data) {
    return data.data;
  },

  minChars: 1,
  required: true
};
var manifest_config = {
  marcoPolo: marcopolo_config,
  formatDisplay: function (data, $item, $mpItem) {
    return data.ngram;
  },
  formatValue: function (data, $value, $item, $mpItem) {
    return data.ngram;
  },
  onAdd: function (data, $item, initial) {
    ngramviewer.query( data.ngram );
  },
  onRemove: function (data, $item) {
    delete ngramviewer.alldata[ data.ngram ];
    console.log( Object.keys(ngramviewer.alldata).length );
    if( Object.keys(ngramviewer.alldata).length>0 ){
          ngramviewer.plot();
          ngramviewer.viewposts();
    } else {
      ngramviewer.clear();
      navposts.clear();
    }

  },
  formatRemove: function ($remove, $item) {
    return '✖';
  },
  required: true,
  separator: ''
};

var ngramviewer = {
  alldata: {},
  lastdateover: '',
  selecteddate: false,
  graphic: {},
  graphic_init: {
      target: '#plotzone',
      full_width: true,
      height: 250,
      top: 15,
      right:100,
      x_extended_ticks: true,
      interpolate: 'basic',
      area:false,
      mouseover: function(d, i) {
        ngramviewer.lastdateover = d.date;
      }
    },

  init: function () {
    $('#ngraminput').manifest( manifest_config );
  },
  clear: function(){
    ngramviewer.selecteddate = false;
    ngramviewer.graphic.markers = null;
    MG.data_graphic( ngramviewer.graphic );
    $('#plotzone').empty();
  },
  query: function ( ngram ) {
    $.getJSON(urlfor_getFreqs, { ngram: ngram  }, ngramviewer.adddata );
  },
  adddata: function( data ){
    data.data  = MG.convert.date(data.data, 'date')
    // console.log( this ) ... query
    ngramviewer.alldata[ data.ngram ] = data ;
    console.log(ngramviewer.alldata)

    ngramviewer.plot();
    if( ngramviewer.selecteddate ){
      ngramviewer.viewposts();
    }
  },
  plot: function () {
    console.log( '-- plot:')
    //console.log(ngramviewer.alldata);
    var data2plot = [];
    var legendLabels = [];
    for (var ngram in ngramviewer.alldata){
        var data = ngramviewer.alldata[ngram].data;
        data2plot.push( data )
        legendLabels.push( ngram )
    }
    // for (var i = 0; i < ngramviewer.alldata.length; i++) {
    //   var data = ngramviewer.alldata[i].data;
    //   data2plot.push( data )
    // }

    this.graphic = this.graphic_init;
    this.graphic.data = data2plot;
    this.graphic.x_accessor = 'date';
    this.graphic.y_accessor = 'freq';
    this.graphic.chart_type = 'line';
    this.graphic.legend = legendLabels;
    MG.data_graphic( this.graphic );

    $('#plotzone svg').click( function(){
      formatdate = d3.time.format("%Y-%m-%d");
      ngramviewer.selecteddate = formatdate(ngramviewer.lastdateover);
      ngramviewer.viewposts();
      ngramviewer.addmarkers( ngramviewer.lastdateover );
      }
      );
  },
  viewposts: function (){
    var ngrams = Object.keys(ngramviewer.alldata);
    navposts.query( ngramviewer.selecteddate, ngrams.join() )
  },
  addmarkers: function( date ){
    formatdate = d3.time.format("%d/%m");
    var markers = [{
       'date': date,
       'label': formatdate(date)
   }];
    this.graphic.markers = markers;
    MG.data_graphic( this.graphic );
  }
}

var navposts = {
  query: function (  date, ngrams ) {
    console.log( date );
    console.log( ngrams );
    $.getJSON(urlfor_getSomePosts, { ngrams: ngrams, date:date  }, navposts.print );
  },
  clear: function (){
    $('#postzone').empty();
  },
  print: function (data) {
    var $result =  $('#postzone');
    navposts.clear();
    $('#postzone').append( $('<h2 />').text( data.day ) );
    if ( data.posts.length > 0 ) {
      $.each( data.posts, function(i, d){
            navposts.addapost( $result, d  );
        }  );
    } else { $result.append( $('<p />').text("Pas d'articles pour '"+data.ngrams+"' ce jour...") );  }
  },

  addapost: function ( $elt, fields ) {
    $elt.append(
      $('<div />', {'class':'post'})
        .append( $('<h3 />')
            .append( $('<a />', {'href':fields['link'], 'text':fields['title']} ) )
        )
        .append(  $('<div />')
            .html( fields['summary'] )
            .prepend(
                $('<span />', {'text': '('+fields['source']+') '} )
              )
        )
    );

  },
  formatdate : function ( date ){
  	var d = date.split("-");
    return d[2] + '/' + d[1] + '/' + d[0];
  }
}

$(document).ready( ngramviewer.init );
