# lesMotsDesJournaux
news timeline word cloud



Data flow:
==========
+ Journaux
- get RSS
- save RSS

+Journaux
get title, description, source
parse date
save alldata.json

/data4Eleve
+ Blacklist
Clean( title + description ) -> formated text
save data4Eleve.json

/Eleve
find nuplet
count global... Seuil>3
save nuplets_count

/ afterEleve
  count, merge, dicoDuSignifiant...

/count by day...


TODO
=====
* parse to DB.posts   rss2db
* cluster for each day
* Flask web site
* Layout d3js+svg...
* lundi vs lundi
* detect gram in ngram : "vache" < "vache folle"
* work with date... fr //  , en --?

* resume un livre... chaque page = un jour

Fonctionalités possible
=======================
* zoom _ Group by day/week/month
* search for a date
* search for a word
* see title/descript. for a word/day
* see TimeLine for a word/ or list of words
* compare source - journaux
* smartphone support
* [plus de mots] affiche plus de mots

Interface
=========
* scroll locked + inertie (smartphone like)
http://darsa.in/sly/examples/horizontal.html
* full time line en bas/fond -> selection date + affichage time si mot
