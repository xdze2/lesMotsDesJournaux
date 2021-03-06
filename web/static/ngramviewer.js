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

      navposts.clear();
      ngramviewer.clear();
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
      height: 195,
      top: 20,
      right:100,
      left: 50,
      bottom: 28,
      x_extended_ticks: true,
      interpolate: 'basic',
      area:false,
      y_label: 'freq. ‰',
      show_secondary_x_label: false,
      xax_format:  function (d){
            return  moment(d).format('Do MMM');
      },
      mouseover: function(d, i){
            ngramviewer.lastdateover = d.date;
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
    $('#ngraminput').manifest('add', {'ngram':ngram});
    return false;
  },
  query: function ( ngram ) {
    $.getJSON(urlfor_getFreqs, { ngram: ngram  }, ngramviewer.adddata );
  },
  adddata: function( data ){
    data.data  = MG.convert.date(data.data, 'date')

    ngramviewer.alldata[ data.ngram ] = data ;
    //console.log(ngramviewer.alldata)

    // mise à jour des posts:
    if( ngramviewer.selecteddate ){
      console.log('addData: update posts view')
      ngramviewer.viewposts();
    };

    ngramviewer.plot();

    $('#doodle').hide();
    $('.help').hide();

  },
  plot: function () {

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

    if( ngramviewer.selecteddate ){
      ngramviewer.addmarkers(ngramviewer.selecteddate);
    }else{
      this.loadPlot();
    }

  },
  loadPlot: function(){
    MG.data_graphic( this.graphic );
    d3.selectAll("text.label") // hack pour le yLabel
      .attr('dominant-baseline', 'hanging')
      .attr("y", 0);

    $('#plotzone svg').unbind().click( ngramviewer.clickOnPlot );
  },
  clickOnPlot: function(){
    ngramviewer.selecteddate = moment( ngramviewer.lastdateover );
    ngramviewer.addmarkers( ngramviewer.selecteddate );
    // console.log('Click plot: update posts')
    ngramviewer.viewposts( );
  },
  viewposts: function (){
    console.log('view posts')
    var ngrams = Object.keys(ngramviewer.alldata);
    navposts.query( ngramviewer.selecteddate, ngrams.join() )
  },
  addmarkers: function( date ){
    var markers = [{
       'date': date,
       'label': "\u00A0\u00A0"+date.format('ddd Do MMM') //spaces: hack pour le style
     }];
    this.graphic.markers = markers;
    this.loadPlot();
  },
  clearmarkers: function( date ){
    this.graphic.markers = null;
    this.loadPlot();
  }
}

var navposts = {
  query: function (  date, ngrams ) {
    $.getJSON(urlfor_getSomePosts, { ngrams: ngrams, date:date.format('YYYY-MM-DD')  }, navposts.print );
  },
  clear: function (){
    $('#postzone').empty();
    $('#postzone').hide();
  },
  clickRemove: function (){
    navposts.clear();
    ngramviewer.clearmarkers();
    return false;
  },
  print: function (data) {
    var $result =  $('#postzone');
    $result.empty();
    $result.show();

    $('#postzone').append(
      $('<h2 />').text( navposts.formatday( data.date )+' ('+data.posts.length+')' )
        .append($('<a />',
          {'href':'/', 'text':'✖', 'class':'close'} ) ).on('click', navposts.clickRemove )
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
