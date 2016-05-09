

var stats = {
  graphic: {
      target: '#plotstats',
      full_width: true,
      height: 195,
      top: 20,
      right:100,
      left: 90,
      bottom: 28,
      x_extended_ticks: true,
      interpolate: 'basic',
      area:true,
      y_label: 'count posts',
      show_secondary_x_label: false,
      xax_format:  function (d){
            return  moment(d).format('Do MMM');
      }

    },
  init: function(data){
    moment.locale('fr'); // 'fr'


    //console.log(ngramviewer.alldata);
    var data2plot = [];

    // for (var ngram in ngramviewer.alldata){
    //     var data = ngramviewer.alldata[ngram].data;
    //     data2plot.push( data )
    //
    // }
    data  = MG.convert.date(data, 'date')
    this.graphic.data = data;
    this.graphic.x_accessor = 'date';
    this.graphic.y_accessor = 'count';
    this.graphic.chart_type = 'line';

    MG.data_graphic( this.graphic );

  }
}





$.getJSON( urlfor_nPostsByDay,
	function(data){ stats.init(data.data); }
);
