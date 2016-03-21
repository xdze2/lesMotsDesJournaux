/******************************************************************************

 This is a demo page to experiment with binary tree based
 algorithms for packing blocks into a single 2 dimensional bin.

 See individual .js files for descriptions of each algorithm:

  * packer.js         - simple algorithm for a fixed width/height bin
  * packer.growing.js - complex algorithm that grows automatically

 TODO
 ====
  * step by step animated render to watch packing in action (and help debug)
  * optimization - mark branches as "full" to avoid walking them
  * optimization - dont bother with nodes that are less than some threshold w/h (2? 5?)

*******************************************************************************/

Demo = {

  init: function(data) {

    Demo.el = {
      canvas:   $('#canvas')[0],
      nofit:    $('#nofit')
    };

    if (!Demo.el.canvas.getContext) // no support for canvas
      return false;

    Demo.el.draw = Demo.el.canvas.getContext("2d");


    Demo.run(data);


  },

  //---------------------------------------------------------------------------

  run: function(data) {
    var len = data.length;
    Demo.canvas.reset( len*(Demo.param.day_width+Demo.param.daymargin), Demo.param.height);

    var blocks, packer, offset;
    for (n = 0 ; n < len ; n++) {
            blocks = data[n].mots;
            day = data[n].day;
            blocks = Demo.evaluateSize(blocks);
            Demo.sort.now(blocks);
            packer = new Packer(Demo.param.day_width, Demo.param.height)
            packer.fit(blocks);
            Demo.report(blocks, packer.root.w, packer.root.h);

            offset = n*Demo.day_width + Demo.param.daymargin;
            Demo.canvas.blocks(blocks, Demo.param.day_width*n, day);
    }
    
    

  },


  //---------------------------------------------------------------------------

  report: function(blocks, w, h) {
    var fit = 0, nofit = [], block, n, len = blocks.length;
    for (n = 0 ; n < len ; n++) {
      block = blocks[n];
      if (block.fit)
        fit = fit + block.area;
      else
        nofit.push("" + block.w + "x" + block.h);
    }
    //Demo.el.ratio.text(Math.round(100 * fit / (w * h)));
    console.log("Did not fit (" + nofit.length + ") :<br>" + nofit.join(", "));
  },

  //---------------------------------------------------------------------------
  param: {
      padding: 3 ,
      height:650,
      day_width: 380,
      top_margin: 50,
      color:'none',
      sortFun:'a',
      daymargin:8
      },
  getFontSize: function(i){
            var fontsize_min = 14, fontsize;
            return Math.round( fontsize_min*i );
      },
  evaluateSize: function(blocks) {
      var n, block, w, h;
      var padding = Demo.param.padding;
      for (n = 0 ; n < blocks.length ; n++) {
        block = blocks[n];
        Demo.el.draw.font= Demo.getFontSize(block.size)+"px Georgia Bold";
        w = Demo.el.draw.measureText(block.label).width;

        h = Demo.el.draw.measureText('M').width; //yes!
        if( w > Demo.param.day_width ){
                  w = w/2.0;
                  h = h/2.0;
                  blocks[n].size = blocks[n].size/2.0;
            }
        blocks[n].w = w + 2*padding;
        blocks[n].h = h ;
      }
      return blocks;
      },
  sort: {

    random  : function (a,b) { return Math.random() - 0.5; },
    w       : function (a,b) { return b.w - a.w; },
    h       : function (a,b) { return b.h - a.h; },
    a       : function (a,b) { return b.w*b.h - a.w*b.h; },
    max     : function (a,b) { return Math.max(b.w, b.h) - Math.max(a.w, a.h); },
    min     : function (a,b) { return Math.min(b.w, b.h) - Math.min(a.w, a.h); },

    height  : function (a,b) { return Demo.sort.msort(a, b, ['h', 'w']);               },
    width   : function (a,b) { return Demo.sort.msort(a, b, ['w', 'h']);               },
    area    : function (a,b) { return Demo.sort.msort(a, b, ['a', 'h', 'w']);          },
    maxside : function (a,b) { return Demo.sort.msort(a, b, ['max', 'min', 'h', 'w']); },

    msort: function(a, b, criteria) { /* sort by multiple criteria */
      var diff, n;
      for (n = 0 ; n < criteria.length ; n++) {
        diff = Demo.sort[criteria[n]](a,b);
        if (diff != 0)
          return diff;  
      }
      return 0;
    },

    now: function(blocks) {
      var sort = Demo.param.sortFun;
      if (sort != 'none')
        blocks.sort(Demo.sort[sort]);
    }
  },

  //---------------------------------------------------------------------------

  canvas: {

    reset: function(width, height) {
      Demo.el.canvas.width  = width  + 1; // add 1 because we draw boundaries offset by 0.5 in order to pixel align and get crisp boundaries
      Demo.el.canvas.height = height + 1; // (ditto)
      Demo.el.draw.clearRect(0, 0, Demo.el.canvas.width, Demo.el.canvas.height);
    },

    rect:  function(x, y, w, h, color, label, size) {
      var pad =  Demo.param.padding
      Demo.el.draw.fillStyle = color;
      Demo.el.draw.fillRect(x + 0.5, y + 0.5, w, h);
      Demo.el.draw.font= Demo.getFontSize( size )+"px Georgia Bold";
      Demo.el.draw.textBaseline="hanging"; 
      Demo.el.draw.fillStyle = 'black';
      Demo.el.draw.fillText(label, x+pad, y+pad);
    },

    stroke: function(x, y, w, h) {
      Demo.el.draw.strokeRect(x + 0.5, y + 0.5, w, h);
    },

    blocks: function(blocks, offset, day) {
      var n, block;
      var topM = Demo.param.top_margin;
      for (n = 0 ; n < blocks.length ; n++) {
        block = blocks[n];
        if (block.fit)
          Demo.canvas.rect(offset + block.fit.x , topM+block.fit.y, block.w, block.h, Demo.color(n), block.label, block.size);
      }
      Demo.el.draw.font= "18px Georgia";
      Demo.el.draw.textBaseline="hanging"; 
      Demo.el.draw.fillStyle = 'black';
      Demo.el.draw.fillText( day, offset+2, 2);
    }
},


  //---------------------------------------------------------------------------

  colors: {
    pastel:         [ "#FFF7A5", "#FFA5E0", "#A5B3FF", "#BFFFA5", "#FFCBA5" ],
    basic:          [ "silver", "gray", "red", "maroon", "yellow", "olive", "lime", "green", "aqua", "teal", "blue", "navy", "fuchsia", "purple" ],
    gray:           [ "#111", "#222", "#333", "#444", "#555", "#666", "#777", "#888", "#999", "#AAA", "#BBB", "#CCC", "#DDD", "#EEE" ],
    vintage:        [ "#EFD279", "#95CBE9", "#024769", "#AFD775", "#2C5700", "#DE9D7F", "#7F9DDE", "#00572C", "#75D7AF", "#694702", "#E9CB95", "#79D2EF" ],
    solarized:      [ "#b58900", "#cb4b16", "#dc322f", "#d33682", "#6c71c4", "#268bd2", "#2aa198", "#859900" ],
    none:           [ "transparent" ]
  },

  color: function(n) {
    var cols = Demo.colors[Demo.param.color];
    return cols[n % cols.length];
  }

  //---------------------------------------------------------------------------

}
var data_filename = 'data.json'
$.getJSON(data_filename, function (json) {
      $( Demo.init(json) );
});



