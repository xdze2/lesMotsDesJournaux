
# coding: utf-8

# In[ ]:

import json
import re


# In[ ]:

def printSorted(dico, n = 200 ):
    myDico_sorted = sorted(dico.iteritems(), key = lambda x:x[1], reverse=True)
    for m, c in myDico_sorted[:n]:
        print '%s (%0.2f) ' % (m, c),


# In[ ]:

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# In[ ]:

# Load "liste des mots"
import codecs

filename = './data_dico/liste_mots_utf8.txt'
# cf: http://www.lexique.org/listes/liste_mots.txt
# load
with codecs.open(filename, encoding='utf-8') as f:
    listemots = f.readlines()

for i, mot in enumerate( listemots ):
    a = mot.split('\t')
    freq = float(a[1])
    word = a[0]
    listemots[i] = (word, freq)

dicoFr = { x[0]:x[1] for x in listemots }


# In[ ]:

def cleanAndSplit( texte ):
    #texte = texte.lower()

    myRe = u"[:’',.«»?! ()\[\]…”\"0-9]+"
    texte = re.sub(myRe, u' ', texte)
    texte = texte.replace(u'\xa0', u' ')
    texte = texte.replace(u'-', u' ')
    L = texte.split(' ')

    for i, mot in enumerate( L ):
        if mot.lower() in dicoFr:
            L[i] = mot.lower()

    return L


# In[ ]:

# load
filename = './data_rss/rss_save_leMonde.json'

loaded_data = json.loads(open(filename).read())
print 'nbr articles: ', len( loaded_data )

# Work with DATE
from datetime import datetime

def jour_de_la_semaine(i):
    d = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    return d[i]

for k, post in loaded_data.iteritems():
    txt_date = post['pubDate']
    txt_date = txt_date.replace(u'GMT', u'')
    txt_date = re.sub('\+[0-9]{4}', u'', txt_date) # !! not the real hour ..
    txt_date = re.sub(r'\s+$', '', txt_date)

    date = datetime.strptime(txt_date, '%a,  %d %b %Y %H:%M:%S')
    loaded_data[k]['date'] = date


# In[ ]:

words_count = {}

for post in loaded_data.itervalues():
    title = post['title']
    description = post['description']
    if description:
        description = strip_tags( description )
    else:
        description = ''

    L = cleanAndSplit( title+' '+description )

    for mot in L:
        if words_count.has_key( mot ):
            words_count[mot ] += 1
        elif len( mot ) > 2:
            words_count[mot ] = 1

n_mots_globaux = len( words_count )

print 'nbr mots: ', n_mots_globaux


# In[ ]:

printSorted(words_count, 100)


### Norme avec DicoFr

# In[ ]:

black_liste =  ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi' ]
black_liste.extend( ['samedi', 'dimanche', 'jusqu', 'aujourd', 'France', 'mars', 'week', 'end', 'Etat', 'Etats'] )


# In[ ]:

words_count_dicoFr = {}
notInDicoFr = {}
for m, c in words_count.iteritems():
    if m in black_liste :
        continue
    elif m in dicoFr : # and c*n_mots > 1:
        score = float( c )/float( n_mots_globaux )  / (dicoFr[m]*1e-6)
        words_count_dicoFr[m] = score
    else:
        score =  c
        notInDicoFr[m] = score

words_sorted_dicoFr = sorted(words_count_dicoFr.iteritems(), key = lambda x:x[1], reverse=True)
notInDicoFr_sorted = sorted(notInDicoFr.iteritems(), key = lambda x:x[1], reverse=True)


# In[ ]:

printSorted(words_count_dicoFr, 100)


# In[ ]:

printSorted(notInDicoFr)


# In[ ]:

# norme: max not in dico = max in dico

max_notInDico = notInDicoFr_sorted[0][1]
max_inDico = words_sorted_dicoFr[0][1]

print max_notInDico, max_inDico


# In[ ]:

# Merge
myDico = {}

for mot, c in notInDicoFr.iteritems():
    myDico[mot] = float(c) / float( max_notInDico *3  )

for mot, c in words_count_dicoFr.iteritems():
    myDico[mot] = float(c) / float( max_inDico )


# In[ ]:

printSorted( myDico )


#### jour par jour

# In[ ]:

mois = u'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'
mois = mois.split(' ')
def writeDay( d ):
    i = d.weekday()
    jour = str( d.day )
    if jour == '1': jour = '1er'
    return jour_de_la_semaine(i)+' '+jour+' '+mois[d.month]


# In[ ]:

posts_by_day = {}
for post in loaded_data.itervalues():
    d = post['date'].date()

    title = post['title']
    description = post['description']
    if description:
        description = strip_tags( description )
    else:
        description = ''
    texte = title+' '+description

    if d not in posts_by_day:
        posts_by_day[d] = [ texte ]
    else:
        posts_by_day[d].append( texte )


# le nombre de mot par jour est pas trop significatif ...

# In[ ]:

count_by_days = {}
for day, textes in posts_by_day.iteritems():
    count_day = {}
    for titre in textes:
        L = cleanAndSplit( titre )

        for mot in L:
            if mot in myDico:
                count_day[mot] = myDico[mot]

    count_by_days[day] = count_day


# In[ ]:

for k in count_by_days.iterkeys():
    print '\n// '+writeDay( k )+' //'
    printSorted( count_by_days[k], 30 )


# In[ ]:

#norme by day


# In[ ]:

sizeMax = 6
data_json = []
count_by_days_sorted = sorted( count_by_days.iteritems(), key=lambda x:x[0] )
for k, mots_day in count_by_days_sorted:
    day_sorted = sorted( mots_day.iteritems(), key= lambda x:x[1], reverse=True )[:20]
    maxScore = day_sorted[0][1]
    minScore = day_sorted[-1][1]

    liste_day = []
    for mot, score in day_sorted:
        score_layout = 1 + round( float(sizeMax-1)/float(maxScore-minScore)*(score-minScore)   )
        node = {'label':mot, 'size':score_layout}
        liste_day.append( node )

    data_json.append({ 'mots':liste_day, 'day':writeDay( k )  })


# In[ ]:

# save JSON
json_file = './web/data.json'
with open(json_file, 'w') as outfile:
    json.dump(data_json, outfile)


# In[ ]:




# In[ ]:
