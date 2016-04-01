# coding: utf-8

import json
import re

import dataExtern


# ---------- count by day ----------
print( '   - Count by day -' )

# -- load --
filename = './data_rss/count_by_day.json'
data_by_day = json.loads(open(filename).read())

print( 'nombre de mots: %i' % len(data_by_day) )

nbrs_mot_parJour = {}
for daycount in data_by_day.values():
    for day, c in daycount.items():

        if day in nbrs_mot_parJour:
            nbrs_mot_parJour[day] += c
        else:
            nbrs_mot_parJour[day] = c

print( 'nombre de jours: %i' % len(nbrs_mot_parJour) )

# print( data_by_day.keys() )

# s = sorted( count_by_day[(31, 3, 2016)].items(), key=lambda x:x[1]['score'], reverse=True )
# s = [ (mot, c['count'], c['score']) for mot, c in s  ]
# print( ' '.join( [ '%s (%i, %.2f)'% x for x in s ][:30] ) )
#
# print('\n')
# s = sorted( count_by_day[(30, 3, 2016)].items(), key=lambda x:x[1]['score'], reverse=True )
# s = [ (mot, c['count'], c['score']) for mot, c in s  ]
# print( ' '.join( [ '%s (%i, %.2f)'% x for x in s ][:30] ) )
