var marcopolo_config = {
  url: urlfor_getNgrams,
  formatItem: function (data, $item) {
    return data.ngram;
  },
  onSelect: function (data, $item) {
    this.val(data.ngram);
    this.blur(); //marche pas...
    ngramviewer.query(data.ngram);
  },
  formatData: function (data) {
    return data.data;
  },
  minChars: 2,
  required: true
};

var ngramviewer = {

  init: function () {
    $('#ngraminput').marcoPolo( marcopolo_config );
  },

  query: function ( ngram ) {
    $.getJSON(urlfor_getFreqs, { ngram: ngram  }, ngramviewer.plot );
  },
  plot: function (data) {
    console.log('plot');
    $("#plotici").empty();
    var svg = dimple.newSvg("#plotici", 900, 250);

    console.log(data)
    var myChart = new dimple.chart(svg, data.data);
    myChart.setBounds(60, 40, 900-120, 250-100);
    var x = myChart.addCategoryAxis("x", "date", "%Y-%m-%d", "%d-%B");
    x.addOrderRule("date");

    myChart.addMeasureAxis("y", "freq");
    var s = myChart.addSeries('ngram', dimple.plot.bar);
    s.lineWeight =  2;
    //myChart.addLegend(60, 10, 500, 20, "right");
    myChart.draw();
  },
  print: function (data) {
    var $result =  $('#result');
    $result.empty();
    if ( data.posts.length > 0 ) {
      $.each( data.posts, function(i, d){
            ngramviewer.addapost( $result, d  );
        }  );
    } else { $result.append( $('<p />').text('no results for '+data.ngram+'...') );  }
  },

  addapost: function ( $elt, fields ) {
    $elt.append(
      $('<div />', {'class':'post'})
        .append( $('<h3 />')
            .append( $('<a />', {'href':fields['link'], 'text':fields['title']} ) )
            .prepend(
                $('<span />', {'class':'date'})
                  .text( ngramviewer.formatdate( fields['date'] ) )
            )
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


};

$(document).ready( ngramviewer.init );
