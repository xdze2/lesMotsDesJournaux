var marcopolo_config = {
  url: urlfor_getNgrams,
  formatItem: function (data, $item) {
    return data.ngram;
  },
  onSelect: function (data, $item) {
    this.val(data.ngram);
    this.blur(); //marche pas...
    navposts.query(data.ngram);
  },
  formatData: function (data) {
    return data.data;
  },
  minChars: 2,
  required: true
};

var navposts = {

  init: function () {
    $('#ngraminput').marcoPolo( marcopolo_config );
  },

  query: function ( ngram ) {
    $.getJSON(urlfor_getPosts, { ngram: ngram  }, navposts.print );
  },

  print: function (data) {
    var $result =  $('#result');
    $result.empty();
    if ( data.posts.length > 0 ) {
      $.each( data.posts, function(i, d){
            navposts.addapost( $result, d  );
        }  );
    } else { $result.append( $('<p />').text('no results for '+data.ngram+'...') );  }
  },

  addapost: function ( $elt, fields ) {
    $elt.append(
      $('<div />', {'class':'post'})
        .append(
          $('<h3 />')
            .append( $('<a />', {'href':fields['link'], 'text':fields['title']} ) )
            .prepend(
                $('<span />', {'class':'date'})
                  .text( navposts.formatdate( fields['date'] ) )
            )
        )
        .append(
          $('<div />')
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

$(document).ready( navposts.init );
