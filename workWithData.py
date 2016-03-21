
# coding: utf-8

# In[154]:

import json
import re


# -------- html tag remover -------------------------
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

# --------------------------------------------
# ------------------
# Load "liste des mots"

filename = './data_dico/liste_mots.txt'
# cf: http://www.lexique.org/listes/liste_mots.txt
# load
with open(filename) as f:
    listemots = f.readlines()
  
for i, mot in enumerate( listemots ):
    a = mot.split('\t')
    freq = float(a[1])
    word = a[0]
    listemots[i] = (word, freq)

dicoFr = { x[0]:x[1] for x in listemots }


def cleanAndSplit( texte ):
    #texte = texte.lower()

    myRe = u"[:’',.«»?! ()\[\]…”\"]+"
    texte = re.sub(myRe, u' ', texte)
    texte = texte.replace(u'\xa0', u' ')
    texte = texte.replace(u'-', u' ')
    L = texte.split(' ')
    
    for i, mot in enumerate( L ):
        if mot.lower() in dicoFr:
            L[i] = mot.lower()
    
    return L


# In[155]:

filename = './data_rss/rss_save_leMonde.json'
#filename = 'rss_save_lepoint.json'

# load
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


# ------+--+- Count Global -+--------------
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

n_mots_globaux = float( len( words_count ) )

print 'nbr mots: ', n_mots_globaux


words_sorted = sorted(words_count.iteritems(), key = lambda x:x[1], reverse=True)
# print words_sorted

print '--- words count global ---'

for mot, c in words_sorted[:50]:
    print '%s (%0.1f/k), ' % (mot, 1e3*c), 

print '-------'




## Avec la liste des pays
#filename = 'sql-pays.csv'
#with open(filename) as f:
#    data = f.readlines()
#    
#listePays = []    
#for line in data:
#    line = line.split(',')
#    pays = line[4].replace(u'"', u'')
#    listePays.append( pays.lower() )
    
black_liste =  ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche', 'jusqu', 'aujourd', 'France', 'mars']


words_count_dicoFr = {}
notInDicoFr = []
for m, c in words_count.iteritems():
    if m in black_liste or re.match(r'[0-9]+', m):
        continue
    elif m in dicoFr : # and c*n_mots > 1:
        score = float( c )/float( n_mots_globaux )  / (dicoFr[m]*1e-6)
        words_count_dicoFr[m] = score
    else:
        score = float( c ) 
        notInDicoFr.append( (m, score) )
        
words_sorted_dicoFr = sorted(words_count_dicoFr.iteritems(), key = lambda x:x[1], reverse=True)


print '--- words count / dicoFr ---'
print '--- Les mots du journalisme ---'
for m, c in words_sorted_dicoFr[:500]:
    print '%s (%0.2f), ' % (m, c), 

print ' ' 


notInDicoFr_sorted = sorted(notInDicoFr, key = lambda x:x[1], reverse=True)
print '--- not in dicoFr ---', len(notInDicoFr_sorted)
for m, c in notInDicoFr_sorted:
#    print '%s (%0.2f), ' % (m, c*1e3), 
    print '%s, ' %m, 
print ' '

# Define un masque
LesMotsDuJournalismes = []

for m, c in notInDicoFr:
    if c>1:
        LesMotsDuJournalismes.append( m )
for m, c in words_sorted_dicoFr[:500]:
        LesMotsDuJournalismes.append( m )
        
print len(  LesMotsDuJournalismes )

# ----------- Count Local -+--------------
#def count_local(i):
#    words_count_local = {}
#        
#    post = loaded_data.values()[i]
#        
#    title = post['title']
#    
#    description = post['description']
#    description = strip_tags( description )
#    
#  
#    L = cleanAndSplit( title+' '+description ) 
#    
#    for mot in L:
#        if words_count_local.has_key( mot ):
#            words_count_local[mot ] += 1
#        elif len( mot ) > 2:
#            words_count_local[mot ] = 1
#    
#    
#    n_mots = float( len( words_count_local ) )
#    print '> nbr mots: ', n_mots
#    
#
#    for mot, c_loc in  words_count_local.iteritems():
#        if mot in LesMotsDuJournalismes:
#            score = float( c_loc ) /  n_mots / words_count[mot] * n_mots_globaux        
#            words_count_local[mot] = score
#    
#    local_sorted = sorted(words_count_local.iteritems(), key = lambda x:x[1], reverse=True)
#    
#    return local_sorted
# 
#
##    for m, c in local_sorted:
##        print '%s (%0.2f), ' % (m, c),
#i = 2
#count_local(i)

#def count_post( post ):
#    words_count_local = {}
#    description = post['description']
#    description = strip_tags( description )
#    title = post['title']
#    L = cleanAndSplit( title+' '+description )
#    
#    for mot in L:
#        if words_count_local.has_key( mot ):
#            words_count_local[mot ] += 1
#        elif len( mot ) > 2:
#            words_count_local[mot ] = 1
#            
#    n_mots = float( len( words_count_local ) )
      
      
# --- By day ---
# liste des jours
     
jours_dispo = []
for post in loaded_data.itervalues():
    d = post['date'].date()
    if d not in jours_dispo:
        jours_dispo.append( d )
    
jours_dispo.sort(reverse=True)

#print jours_dispo




def count_by_day(myDay):
    words_day_count = {}
        
    for post in loaded_data.itervalues():
        d = post['date'].date()
        if d == myDay:       
            title = post['title']
            
            description = post['description']
            description = strip_tags( description )
              
            L = cleanAndSplit( title+' '+description ) 
            
            for mot in L:
                if words_day_count.has_key( mot ):
                    words_day_count[mot ] += 1
                elif len( mot ) > 2:
                    words_day_count[mot ] = 1
        else:
            continue
        
        
    n_mots_day = float( len( words_day_count ) )
   
    # norme:
    ratio= n_mots_day * float(  n_mots_globaux ) 
    words_day_count_final = {}
    for mot, c_loc in  words_day_count.iteritems():
        if mot in LesMotsDuJournalismes:
            score = float( c_loc ) * float( words_count[mot] ) / ratio
            words_day_count_final[mot] = score
    
    day_sorted = sorted(words_day_count_final.iteritems(), key = lambda x:x[1], reverse=True)
    
    return day_sorted

def writeDay( d ):
    i = d.weekday()
    jour = str( d.day )
    if jour == '1': jour = '1er'
    return jour_de_la_semaine(i)+' '+jour


print '> By day:'

score_max = 0
data_json = []
for d in jours_dispo:
    day_sorted = count_by_day( d )
    #{"size": 1, "label": "adieu"},
    mots = []
    for m, c in day_sorted:
        size = c
        if c > score_max:
            score_max = c
        dico = {'size':size, 'label':m  }
        mots.append( dico )
        
    data_json.append({ 'mots':mots, 'day':writeDay( d )  })
    
    print '\n'
    print '-- ', jour_de_la_semaine(d.weekday()), ' ', d, ' --'
    nMax = len( day_sorted )
    for m, c in day_sorted[:min(nMax, 80)]:
        print '%s/%0.5f, ' % (m, c), 

print score_max

#norme:
for d in data_json:
    for mot in d['mots']:
        mot['size'] = mot['size']/score_max*8.0


# save JSON
json_file = './web/data.json'
with open(json_file, 'w') as outfile:
    json.dump(data_json, outfile)
