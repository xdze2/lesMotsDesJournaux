# lesMotsDesJournaux
N-gram-viewer pour se souvenir des infos passées, basé sur les flux RSS des quotidiens français. Ne parle t-on pas toujours de la même chose ?


Librairies utilisées
=====================
## Javascript:
* scroll Sly: http://darsa.in/sly/examples/horizontal.html
* Bin packing with Packer: https://github.com/jakesgordon/bin-packing
* Time series graph: http://metricsgraphicsjs.org/
* Dynamic auto complete input:
jstayton.github.io/jquery-manifest
http://jstayton.github.io/jquery-marcopolo/

## Python:
* RSS: feedparser
* ELeVE (segmentation des mots): see https://github.com/kodexlab/eleve
* SqLite3


To Do
=====

## Wordspack
* Infinite scroll: load day on the fly, load a particular day
* Plusieurs niveauw de zoom: Grp. by week/month


# Data process:
* Sauvegarder les données brutes dans plusieurs fichiers, ou DB
* Chercher les doublons dans DB.posts

## Ngramviewer
* Zoom sur la courbe, selection d'une plage de date
* Solution pour filtrer AND.OR  ( pick a color )


## Nouvelles Fct. possibles :
* Mots autour d'un mot (qu'est ce que l'on dit de .. ?)
* Filtrer par source
* Cluster for each day, ngram similarity, cluster glissant...



Pour la suite:
================
Highlight
http://www.jquery.info/scripts/SearchHighlight/demo_en.html
http://bartaz.github.io/sandbox.js/jquery.highlight.html

Time picker/slider
http://marcneuwirth.com/blog/2010/02/21/using-a-jquery-ui-slider-to-select-a-time-range/

CrossFilter
http://square.github.io/crossfilter/

* Detect gram in ngram : "vache" < "vache folle"
* Detect "Nuit Debout" < "Nuit debout"
