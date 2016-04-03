# coding: utf-8

import json
import re

import dataExtern
import dataset

print(' --- Process Data ---')
# --- Data for ELeVE ---

blacklist = dataExtern.getBlacklistBeforeEleve()
def cleanIt( texte ):
    # Rq: l'ordre est important ...

    texte = texte.replace(u'\xa0', u' ') # espace insécable

    # Ponctuation:
    myRe = u'[,;:«»"?!\n\r…©]'
    texte = re.sub(myRe, u' ', texte)

    # enleve les points en gardant ceux des initials:
    texte = re.sub(r'(?<![A-Z])\.', u'', texte)
    # espace dans les chiffres 10_000->10000:
    texte = re.sub(r'([0-9]+)\s([0-9]+)', r'\1\2', texte)

    texte = re.sub(r'(FIGAROVOX/[A-ZÉ\s]+)', r'', texte)

    # for mot in blacklist:
    #      texte = texte.replace( mot, u'')

    texte = re.sub(r'\s[.\-]\s', u' ', texte) # point ou tiret solo
    texte = re.sub(r'\s', u' ', texte) # remove tab and other strange space
    texte = re.sub(r'\s+', u' ', texte) # remove double space

    return texte

# -- load --
filename = './data_rss/all_title.json'
data = json.loads(open(filename).read())

print( 'nombre de news: %i' % len( data ) )

for post in data:
    texte = ''

    if 'title' in post:
        title = post['title']
        if title: texte += title

    if 'description' in post:
        description = post['description']
        if description: texte +=  ' ' + description

    if texte:
        post['formatedtext'] = cleanIt( texte )
    else:
        print(  post )


#  --- ELeVE ---
# see https://github.com/kodexlab/eleve
print( '   - ELeVE -')

from eleve import MemoryStorage
storage = MemoryStorage()

# Then the training itself:
n = 0
for post in data:
      sentence = post['formatedtext']
      mots = sentence.split(' ')
      n += len( mots )
      storage.add_sentence(  mots )

print( 'nombre de mots: %i ' % n )

print( '   - Segment & count -')
from eleve import Segmenter
s = Segmenter(storage)

dicoFr = dataExtern.getDicoFr()
blacklist = dataExtern.getBlacklistAfterEleve()

# --- create DB ---
import os

db_file = 'database_occurences.db'

if os.path.isfile('./'+db_file):
    os.remove( db_file )
    print( '  // %s removed'% db_file)

db = dataset.connect('sqlite:///%s'%db_file)
occurences = db.create_table( 'occurences' )
db.begin()

for postid, post in enumerate(data):

    phrase = post['formatedtext']
    segmentedPhrase = s.segment( phrase.split(' ') )

    for ngram in segmentedPhrase:
        while '' in ngram: ngram.remove( '' )
        if not ngram: continue

        if len( ngram ) > 1:
            c = storage.query_count( ngram )
            if c < 10: # 1er filrage
                segmentedPhrase.extend( [ [x] for x in ngram ] )
                continue
            ngram = ' '.join( ngram )
            # enleve l'apostrophe du debut si besoin:
            ngram = re.sub(r"^[LldDsSnNcC][’']", u'', ngram)

        elif len( ngram[0] )>2 and storage.query_count( ngram )>5:
            ngram = ngram[0]
            ngram = re.sub(u"[Aa]ujourd.hui",  '', ngram)
            ngram = re.sub(u"jusqu.([àa]|en)",  '', ngram)

            ngram = re.sub(u"(^|\s)[LldDsSnNcCjJ]['`’]", "", ngram)
            ngram = re.sub(u"(^|\s)qu['`’]", "", ngram)
            ngram = re.sub(r"[0-9\.\(\)]", u'', ngram)
            ngram = re.sub(r"-$", u'', ngram)
            ngram = re.sub(r"\s", u'', ngram)

            if ngram.lower() in dicoFr and ngram != 'Paris':
                ngram = ngram.lower()

        if len(ngram)>2 and ngram not in blacklist:
            oc = dict(mot=ngram, day=post['day'], source=post['source'], postid=postid)
            occurences.insert( oc )

db.commit()
print( ' .. database commit: %i .. ' % occurences.count() )

# # -- export all users into a single CSV
# result = db['occurences'].all()
# dataset.freeze(result, format='csv', filename='occurences.csv')


# # --  print words_count
# sorted_words = sorted( words_count.items(), key=lambda x:x[1], reverse=True )
# output = [ x[0]+' %i, '%x[1] for x in sorted_words[:600] ] #+' (%i)'%x[1]
# print( '\t'.join( output ) )
# print('\n')
#
# print('  -nombre de mot: %i'%len(words_count ))
# print('  -nombre de jour: %i'%len(count_by_day ))
#
#
# # -- save JSON --
# json_file = './data_rss/count_global.json'
# with open(json_file, 'w') as outfile:
#     json.dump(words_count, outfile)
#
# print( ' words_count saved in %s'%json_file )
#
# # -- save JSON --
# json_file = './data_rss/count_by_day.json'
# with open(json_file, 'w') as outfile:
#     json.dump(count_by_day, outfile)
#
# print( ' count_by_day saved in %s'%json_file )
#

# # -- save JSON --
# json_file = './data_rss/count_global.json'
# with open(json_file, 'w') as outfile:
#     json.dump(nuplets_count, outfile)
#
# print( ' Nuplets saved in %s'%json_file )

#
# # ---------- After ELeVE ----------
# print( '   - After ELeVE -')
#
#
#
#
# # count words
# words_count = nuplets_count  # merge nuplets et single
# for post in data:
#     if 'count' not in post:  post['count'] = {}
#     phrase = post['formatedtext']
#
#     sortedNuplet = sorted( nuplets_count.keys(), key=lambda x:len(x), reverse=True )
#     for nuplet in sortedNuplet:
#         if nuplet in phrase:
#             c = phrase.count( nuplet )
#             if nuplet in post['count']:
#                 post['count'][ nuplet ] += c
#             else:
#                 post['count'][ nuplet ] = c
#             post['formatedtext'] = post['formatedtext'].replace(  nuplet, u' ' )
#
#     mots = post['formatedtext'].split(' ')
#
#     for mot in mots:
#         mot = re.sub(u"[Aa]ujourd.hui",  '', mot)
#         mot = re.sub(u"jusqu.([àa]|en)",  '', mot)
#
#         mot = re.sub(u"(^|\s)[LldDsSnNcCjJ]['`’]", "", mot)
#         mot = re.sub(u"(^|\s)qu['`’]", "", mot)
#         mot = re.sub(r"[0-9\.\(\)]", u'', mot)
#         mot = re.sub(r"-$", u'', mot)
#         mot = re.sub(r"\s", u'', mot)
#
#         if mot.lower() in dicoFr and mot != 'Paris':
#             mot = mot.lower()
#
#         #if mot.endswith( 's' ) and mot[0:-1] in dicoFr:
#         #    mot = mot[:-1]      ... pas une bonne idee dans>dan
#
#         if len( mot )>2 and mot.lower() not in blacklist:
#             if mot in words_count:
#                 words_count[ mot ] += 1
#             elif mot:
#                 words_count[ mot ] = 1
#
#             if mot in post['count']:
#                 post['count'][ mot ] += 1
#             elif mot:
#                 post['count'][ mot ] = 1
#
# print( '\n   - words_count:')
# dataExtern.printSorted( words_count , 200)
#
#
# # -- save JSON --
# json_file = filename
# with open(json_file, 'w') as outfile:
#     json.dump(data, outfile)
#
# print( ' [formatedtext]&[count] saved in %s'%json_file )
