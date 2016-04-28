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
    //console.log( Object.keys(ngramviewer.alldata).length );
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
      height: 230,
      top: 50,
      right:100,
      left: 80,
      x_extended_ticks: true,
      interpolate: 'basic',
      area:false,
      y_label: 'freq. ‰',
      xax_format:  function (d){
            return  moment(d).format('Do MMM');
      },
      mouseover: function(d, i) {
        ngramviewer.lastdateover = d.date;

        var cejour = moment(d.date).format('dddd Do MMMM');

        console.log( d3.select('#plotzone svg .mg-active-datapoint')
                );
      },
      //colors: ['#377eb8', '#ff7f00', '#a6d854', '#f781bf', '#e41a1c']
    },

  init: function () {
    moment.locale('fr'); // 'fr'

    if( typeof ngram_url !== 'undefined' ){
      ngram_url = ngram_url.split(',');

      var initvalues = [];
      for(var i=0, len=ngram_url.length; i < len; i++){
          //console.log( ngram_url[i] );
          ngramviewer.query(ngram_url[i]);
          initvalues.push( {'ngram':ngram_url[i]} );
      }
    }
    manifest_config.values = initvalues;
    $('#ngraminput').manifest( manifest_config );

  },
  clear: function(){
    //ngramviewer.updateurl();
    ngramviewer.selecteddate = false;
    ngramviewer.graphic.markers = null;
    MG.data_graphic( ngramviewer.graphic );
    $('#plotzone').empty();
    $('#doodle').show();
    $('.help').show();
  },
  addngram: function(ngram){
    ngramviewer.query(ngram);

    $('#ngraminput').manifest('add', {'ngram':ngram});
    return false;
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
    } else {
      var max = 1;
      console.log( ngramviewer.alldata  );
    }
    $('#doodle').hide();
    $('.help').hide();

  },
  updateurl: function() {
    var stateObj = { 'ngrams': Object.keys(ngramviewer.alldata) };
    if( Object.keys(ngramviewer.alldata).length>0 ){
      var newUrl = '/'+Object.keys(ngramviewer.alldata).join();
    } else {
      console.log( Object.keys(ngramviewer.alldata).length );
      var newUrl = '/';
    }
    history.replaceState(stateObj, "Hello", newUrl);
  },
  plot: function () {
    //ngramviewer.updateurl();
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
      ngramviewer.addmarkers( ngramviewer.lastdateover );
      var day = moment(ngramviewer.lastdateover).format('YYYY-MM-DD');
      ngramviewer.selecteddate = day;
      ngramviewer.viewposts( );

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
    return false;
  },
  print: function (data) {
    var $result =  $('#postzone');
    navposts.clear();
    $('#postzone').append(
      $('<h2 />').text( 'Titres du '+navposts.formatday( data.date ) )
        .append($('<a />',
          {'href':'/', 'text':'✖', 'class':'close'} ) ).on('click', navposts.clear )
    );
    if ( data.posts.length > 0 ) {
      $.each( data.posts, function(i, d){
            navposts.addapost( $result, d  );
        }  );
    } else { $result.append( $('<p />').text("Pas d'articles pour '"+data.ngrams+"' ce jour...") );  }
  },
  formatday: function (d){
    return moment(d, "YYYY-MM-DD").format('dddd Do MMMM');
  },
  addapost: function ( $elt, fields ) {

    var postdiv = $('<div />', {'class':'post'})
      .append( $('<h3 />', {'text':fields['title']})
        .append( $('<a />', {'href':fields['link'], 'text':fields['source']} ) )
            );
    if( fields['summary']  ){
      postdiv.append(  $('<div />')
        .html( fields['summary'] )
      );
    };

    $elt.append(postdiv);
  },
  formatdate : function ( date ){
  	var d = date.split("-");
    return d[2] + '/' + d[1] + '/' + d[0];
  }
}

$(document).ready( ngramviewer.init );

//
// // handle the back and forward buttons
// $(window).bind('popstate', function(event) {
//     // if the event has our history data on it, load the page fragment with AJAX
//     var state = event.originalEvent.state;
//     if (state) {
//         ngramviewer.init();
//     }
// });
