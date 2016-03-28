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
