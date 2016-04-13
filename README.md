# lesMotsDesJournaux
news timeline word cloud




TODO
=====
* parse to DB.posts   rss2db
* cluster for each day
* Flask web site
* Layout d3js+svg...
* lundi vs lundi
* detect gram in ngram : "vache" < "vache folle"
* work with date... fr //  , en --?
* full time line en bas/fond -> selection date + affichage time si mot

* infinite height bin_packing (+vertical scroll sur telephone...)

* alternat text sur les labelDay:  aujourd'hui, hier, il ya deux jours..., il y a une semaine, il y a un mois et 1 semaines, jours, il y
http://stackoverflow.com/questions/21181621/displaying-some-text-when-mouse-is-over-an-input-text-box

* Faire une lib pour WordsPacking

Eventuellement
==============
* getData: verifier si max non attend (ex: 20 pour le Monde), reduire le délais si besoin
* resume un livre... chaque page = un jour
* chercher les doublons dans DB.posts (il y en  a)

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
