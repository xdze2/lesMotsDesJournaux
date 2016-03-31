# coding: utf-8

import json
import re

import dataExtern



# -- load --
filename = './data_rss/all_title.json'
data = json.loads(open(filename).read())

print( 'nombre de news: %i' % len(data) )




# ---------- count by day ----------
print( '   - Count by day -' )


from datetime import datetime

def jour_de_la_semaine(i):
    d = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    return d[i]

def updateDicoCount( base, newdico ):
    for k, c in newdico.items():
        if k in base:
            base[k] += c
        else:
            base[k] = c
    return base


count_by_day = {}
for i, post in enumerate( data ):
    # gestion date
    date_str = post['date']
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    date_tuple = ( date.day, date.month, date.year )

    # Group by day
    if date_tuple not in count_by_day:
        count_by_day[ date_tuple ] = {}

    count_by_day[date_tuple] = updateDicoCount(count_by_day[date_tuple], post['count']  )

# s = sorted( count_by_day[(29, 3, 2016)].items(), key=lambda x:x[1], reverse=False )
# print( ' '.join( [ '%s (%i)'%x for x in s ][-80:] ) )


# -- load --
json_file = './data_rss/count_global.json'
words_count = json.loads(open(json_file).read())

# -- Normalisation --
import dataExtern
dicoFr = dataExtern.getDicoFr()


nombre_mots = float( sum( words_count.values() ) )
nombre_jours = len( count_by_day )
print( ' nombre total de mots: %i'% nombre_mots )
print( ' nombre jours: %i'% nombre_jours )

for day in count_by_day.keys():

    count_today = count_by_day[day]

    n_mots_today = sum( count_today.values() )

    for mot, c in count_today.items():
        if mot in dicoFr and words_count[mot] > 10:
            w_count = dicoFr[mot]*1e-6*nombre_mots
        elif words_count[mot] > 10:
            w_count = words_count[mot]/nombre_mots
        else:
            w_count = 1/n_mots_today

        proba_random = w_count*n_mots_today
        new_c = c/float( proba_random )

        count_by_day[day][ mot ] = new_c

s = sorted( count_by_day[(31, 3, 2016)].items(), key=lambda x:x[1], reverse=True )
print( ' '.join( [ '%s (%.2f)'%x for x in s ][:80] ) )
