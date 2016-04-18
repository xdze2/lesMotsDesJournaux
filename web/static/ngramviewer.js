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
  // onSelect: function (data, $item) {
  //   console.log( 'hello' )
  //   console.log( data );
  // },
  onAdd: function (data, $item, initial) {
    ngramviewer.query( data.ngram );
  },
  onRemove: function (data, $item) {
    delete ngramviewer.alldata[ data.ngram ];
    if( Object.keys(ngramviewer.alldata).length>0 ){
          ngramviewer.plot();
          console.log( Object.keys(ngramviewer.alldata).length );
    } else {
      $('#plotzone').empty();
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
  graphic: {
      target: '#plotzone',
      full_width: true,
      height: 250,
      top: 15,
      right:100,
      x_extended_ticks: true,
      interpolate: 'basic',
      area:false,
       mouseover: function(d, i) { console.log(d); }
    },
  init: function () {
    $('#ngraminput').manifest( manifest_config );



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

    this.graphic.data = data2plot;
    this.graphic.x_accessor = 'date';
    this.graphic.y_accessor = 'freq';
    this.graphic.chart_type = 'line';
    this.graphic.legend = legendLabels;
    MG.data_graphic( this.graphic );

    $('#plotzone svg').click(
      function (){
        console.log('click');
      }   );
  },
  formatdate : function ( date ){
  	var d = date.split("-");
    return d[2] + '/' + d[1] + '/' + d[0];
  }


};

$(document).ready( ngramviewer.init );
