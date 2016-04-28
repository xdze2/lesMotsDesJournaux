moment.locale('fr'); // 'fr'
datepicker = {
  startdate: moment('2016-03-09', "YYYY-MM-DD"),
  enddate:   moment('2016-05-02', "YYYY-MM-DD"),


  init: function (){

    moment.locale('fr'); // 'fr'


    console.log( datepicker.startdate.week() );
    // datepicker.startdate.weekYear()
    // datepicker.addbar('months');
    datepicker.addbar();

  },
  addbar: function( unit ){
    var w_start = datepicker.startdate.week();
    var w_end = datepicker.enddate.week();
    var n = w_end - w_start ;
    var $bar = $('<ul />', {'id':'weeks_bar'}).appendTo( $( '#datepicker' ) );

    var w =  100.0/(n+1 )+"%";
    var date = moment(datepicker.startdate).startOf( 'weeks' );

    for( var iter = 0; iter < n+1; iter++ ){
      var startdate = date.format('YYYY-MM-DD');
      $bar.append( $('<li />')
                      .text( date.format('Do MMM') )
                      .css( {'width':w} )
                      .click( datepicker.click_event(startdate) )
      );
      date.add(1, 'weeks');
    }

  },
  click_event: function( date ){
    return function(){datepicker.query(date);}
  },
  query: function( start ) {
    $.getJSON(urlfor_getWeek, { 'start': start  }, datepicker.printngrams );
  },
  printngrams: function(data) {

    console.log( data );
    $ngrams = $('#ngrams');
    $ngrams.empty();

    $.each( data.data, function(i, d){
      var $day = $('<div />').append(
            $('<h3 />').text( moment(d.date, "YYYY-MM-DD").format('dddd Do MMMM') )
      );
      $.each(d.mots,  function(i, dd){
          $day.append( $('<span />').text( dd.label+' ' ) ) ;
      }  );

      $day.appendTo( $ngrams );
    } );
  }
};


$(document).ready( datepicker.init );
