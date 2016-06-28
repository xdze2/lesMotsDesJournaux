# coding: utf-8
import sqlite3
import json
## import hashids
from datetime import datetime


#hashids = hashids.Hashids(salt="Comment Garder Son Anonymat Dans Un Paradis Fiscal")
#numbers = hashids.decode(id)
#hashids.encode(line[0])
# def getId( k ):
#     #myid = hashids.encode( k )
#     myId = 'oc'+str( k )
#     return str( myId )
#
# def getLabelDay( date ):
#     jour_de_la_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
#     mois_de_lannee = ['janvier', u'février', u'mars', 'avril', 'mai', 'juin', 'juiller', u'août', 'septembre', 'octobre',
#                       'novembre', u'décembre']
#     date = datetime.strptime(date, '%Y-%m-%d')
#     jour = jour_de_la_semaine[ date.weekday() ]
#     mois = mois_de_lannee[ date.month-1]
#     i = str( date.day )
#     #if i == 1: i='1er'
#     return '%s %s %s'%(jour, i, mois)

# load DB
database_filename = './data/data_lmdjx.db'

database_connection = sqlite3.connect(database_filename)
cursor = database_connection.cursor()



# Pack tout les jours pour web:


# liste des jours
cursor.execute( '''SELECT distinct date
                    FROM stats
                    ORDER By Date(date) DESC
                    LIMIT 400  ''' )

all_dates = []
for line in cursor.fetchall():
    all_dates.append( line[0] )

all_dates = all_dates[::-1]

print( 'nombres de jours: %i' % len(all_dates) )

data4web = []
for date in all_dates:
    cursor.execute( '''SELECT rowid,  ngram, score
                        FROM stats
                        WHERE date=?
                        ORDER BY score DESC
                        LIMIT 30   ''', (date, ) )  # nombre de ngram par jour

    ngrams4today = []
    for line in cursor.fetchall():
        ngram_dict = { 'label':line[1], 'score':line[2], 'id':line[0] }
        ngrams4today.append( ngram_dict )

    day_dict = {'mots':ngrams4today, 'date':date }
    data4web.append( day_dict )


# save JSON
json_file = './web/static/data4alldays.json'
with open(json_file, 'w') as outfile:
    json.dump(data4web, outfile, indent=4)
    print( ' Parsed data saved in %s'%json_file )

# Close the DB
database_connection.close()
print( '%s closed '% database_filename)


# -- old stuff:

# data4web = []
# sizeMax = 4
# for i in range( bigdataframe.shape[0] ):
#     L = bigdataframe.irow( i )
#     scoreList = L.tolist()
#
#     vector = zip(  L.index,  scoreList )
#     vector = sorted( vector, key=lambda x:x[1], reverse=True )
#
#     sorted_words = [ x for x in vector if x[1]>1 ][: 27]
#
#     scoreMax = sorted_words[0][1]
#     scoreMin = sorted_words[-1][1]
#     day = str( L.name ).split(' ')[0]
#     labelDay = getLabelDay( day )
#     print day,
#
#     mots = []
#     for mot, score in sorted_words:
#         scoreNormed =  (score-scoreMin)/float( scoreMax - scoreMin )
#         size = round(  scoreNormed*(sizeMax - 1)  ) + 1
#         id_int = liste_mots.index(mot) + i*len( liste_mots )
#         mots.append( { 'label':mot, 'size':size, 'id':id_int } )  # use http://hashids.org/python/
#
#     data4web.append( {'mots':mots, 'day':day, 'labelDay':labelDay} )
#
# # save JSON
# json_file = './web/data.json'
# with open(json_file, 'w') as outfile:
#     json.dump(data4web, outfile)
#     print( ' Parsed data saved in %s'%json_file )


#
# # liste des jours
# cursor.execute( '''SELECT distinct date
#                     FROM stats
#                     ORDER By Date(date)
#                     ''' )
#
# all_dates = []
# for line in cursor.fetchall():
#     all_dates.append( line[0] )
#
# data4web = []
# for date in all_dates:
#     cursor.execute( '''SELECT rowid,  ngram, score
#                         FROM stats
#                         WHERE score > 1 and date=?
#                         ORDER BY score DESC
#                         LIMIT 21   ''', (date, ) )
#
#     ngrams4today = []
#     for line in cursor.fetchall():
#         ngram_dict = { 'label':line[1], 'score':line[2], 'id': getId( line[0] )}
#         ngrams4today.append( ngram_dict )
#
#     day_dict = {'mots':ngrams4today, 'day':date, 'labelDay':getLabelDay(date) }
#     data4web.append( day_dict )
#
# # save JSON
# json_file = './web/static/data.json'
# with open(json_file, 'w') as outfile:
#     json.dump(data4web, outfile, indent=4)
#     print( ' Parsed data saved in %s'%json_file )
