# lesMotsDesJournaux
news timeline word cloud




TODO
=====

* function getTopScore( start_date, end_date, step ), zoom ...

* mouseOver.clik: painter0.1, change style des ngram=ngram
* on click: time line en bas, skyline

* cluster for each day, ngram similarity

* scroll bar joli

* gestion des noFit ... [+]button . scroll vertical
  - infinite height bin_packing (+vertical scroll sur telephone...)

* Afficher Semaine #, les debut du mois en haut, repère visu
* alternat text sur les labelDay:  aujourd'hui, hier, il ya deux jours..., il y a une semaine, il y a un mois et 1 semaines, jours, il y
http://stackoverflow.com/questions/21181621/displaying-some-text-when-mouse-is-over-an-input-text-box

* voir les posts ?  mais pourquoi on parle de ça ??

Popup AJAX:
http://dimsemenov.com/plugins/magnific-popup/

Dynamic auto complete:
http://jstayton.github.io/jquery-marcopolo/

Highlight
http://www.jquery.info/scripts/SearchHighlight/demo_en.html
http://bartaz.github.io/sandbox.js/jquery.highlight.html

Eventuellement
==============
* detect gram in ngram : "vache" < "vache folle"
* Detect "Nuit Debout" < "Nuit debout"
* getData_feedparser: verifier si max non attend (ex: 20 pour le Monde), reduire le délais si besoin
* resume un livre... chaque page = un jour
* chercher les doublons dans DB.posts (il y en  a)
* Faire une lib pour PackedCloud

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




Lib
===
## JS:
* scroll Sly: http://darsa.in/sly/examples/horizontal.html
* Bin packing with Packer: https://github.com/jakesgordon/bin-packing

## Python:
* feedparser
* ELeVE: see https://github.com/kodexlab/eleve
* sqlite3
