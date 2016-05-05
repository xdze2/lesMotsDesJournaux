# lesMotsDesJournaux
ngramviewer pour la presse française


ToDo
====
* redondance legend/search bar   et  marker_day/day
* Ne pas calculer la freq. mais le nbre d'apparition brut
* Gestion url
* uniform event: add/remove_ngram, selectAday

## ngramviewer
* Solution pour filter AND.OR  ( pick a color )
* nav using key <--> chg day

## wordspack
* infinite scroll, load day on the fly
* highlight mots selectionnés
* mouseOver.clik / Painter0.1: change style des ngram=ngram
* Grp. by week/month
* scroll bar joli, + label
* sync with ngramViewer ?

## navigatePosts
* highlight mots selectionnés
* Pagination
* fitler by source
* nav using key <--> chg day

# Data process:
* Update DB vs delete/create
* chercher les doublons dans DB.posts (il y en a)
* Use a better dicoFr ...
* Split JSON by days or weeks ...

## Nouvelles Fct. :
* cluster for each day, ngram similarity, cluster glissant ..
* Page de stats sur les Data, nbrs posts par jour


* Afficher Semaine #, les debut du mois en haut, repère visu


## Bugs:
* quand deux fois le même ngram
* pas de marker pour le dernier jour
* loop quand click depuis packedWords

Eventuellement
==============
* detect gram in ngram : "vache" < "vache folle"
* Detect "Nuit Debout" < "Nuit debout"
* getData_feedparser: verifier si max non attend (ex: 20 pour le Monde), reduire le délais si besoin

* alternat text sur les labelDay:  aujourd'hui, hier, il ya deux jours..., il y a une semaine, il y a un mois et 1 semaines, jours

* resume un livre... chaque page = un jour
* Faire une lib pour PackedCloud

Fonctionalités possible
=======================
* zoom _ Group by day/week/month
* search for a date

* Compare source - journaux, filtre par journaux
* smartphone support
* [plus de mots] affiche plus de mots

* pool/ selection un mot
  - tt les ngrams co-occurents
  - count moyen
  - group by source
  - score(m, s) = count( m, source ) / count( m, * )
  - order by score desc
pour voir les mots associés à un terme, et comparer les journaux


* [ok] search for a word
* [ok] see title/descript. for a word/day
* [ok] see TimeLine for a word/ or list of words
* [ok] Gestion max height
* [ok] voir les posts ?  mais pourquoi on parle de ça ??
* [ok] gestion des noFit ... [+]button . scroll vertical
  - infinite height bin_packing (+vertical scroll sur telephone...)


## Rebus:
Lé: vache ? robot ? (> about ?)
dé: http://mathematiques.ac-dijon.fr/indunet3/ipr/brochure_2011/images/socle_2.png
(> pick ngram random)
m: http://img.over-blog.com/100x70/3/81/21/27/Gif/mal-de-tete-dessin.jpg
(> Stats ?)
Jx: http://www.lacoupedelinfo.org/wp-content/uploads/2012/10/9251285-pile-de-journaux-neerlandais-sur-fond-blanc.jpg
(> list sources ?)


Lib
===
## JS:
* scroll Sly: http://darsa.in/sly/examples/horizontal.html
* Bin packing with Packer: https://github.com/jakesgordon/bin-packing

## Python:
* feedparser
* ELeVE: see https://github.com/kodexlab/eleve
* sqlite3



jQuerry plugins
===============

Popup AJAX:
http://dimsemenov.com/plugins/magnific-popup/

Dynamic auto complete:
jstayton.github.io/jquery-manifest
http://jstayton.github.io/jquery-marcopolo/

Highlight
http://www.jquery.info/scripts/SearchHighlight/demo_en.html
http://bartaz.github.io/sandbox.js/jquery.highlight.html

Time picker/slider
http://marcneuwirth.com/blog/2010/02/21/using-a-jquery-ui-slider-to-select-a-time-range/

Time series graph
http://metricsgraphicsjs.org/

CrossFilter
http://square.github.io/crossfilter/
