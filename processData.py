# coding: utf-8

import json
import re

import dataExtern


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

    for mot in blacklist:
         texte = texte.replace( mot, u'')

    texte = re.sub(r'\s[.\-]\s', u' ', texte) # point ou tiret solo
    texte = re.sub(r'\s', u' ', texte) # remove tab and other strange space
    texte = re.sub(r'\s+', u' ', texte) # remove double space

    return texte

# -- load --
filename = './data_rss/all_title.json'
alldata = json.loads(open(filename).read())

print( 'nombre de news: %i' % len(alldata) )

data = []
for post in alldata:
    texte = ''

    if 'title' in post:
        title = post['title']
        if title: texte += title

    if 'description' in post:
        description = post['description']
        if description: texte +=  ' ' + description

    if texte:
        post['formatedtext'] = cleanIt( texte )
        data.append( post )
    else:
        print(  post )

delta = len(alldata) - len( data )
print( 'nbr posts perdu: %i ' %  delta )

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


from eleve import Segmenter
s = Segmenter(storage)

dicoFr = dataExtern.getDicoFr()
blacklist = dataExtern.getBlacklistAfterEleve()

count_by_day = {}
words_count = {}
for post in data:

    phrase = post['formatedtext']
    segmentedPhrase = s.segment( phrase.split(' ') )

    for nuplet in segmentedPhrase:
        while '' in nuplet: nuplet.remove( '' )
        if not nuplet: continue
        if len( nuplet ) > 1:
            nuplet = ' '.join( nuplet )
            # enleve l'apostrophe du debut si besoin:
            nuplet = re.sub(r"^[LldDsSnNcC][’']", u'', nuplet)

        elif len( nuplet[0] )>2:
            mot = nuplet[0]
            mot = re.sub(u"[Aa]ujourd.hui",  '', mot)
            mot = re.sub(u"jusqu.([àa]|en)",  '', mot)

            mot = re.sub(u"(^|\s)[LldDsSnNcCjJ]['`’]", "", mot)
            mot = re.sub(u"(^|\s)qu['`’]", "", mot)
            mot = re.sub(r"[0-9\.\(\)]", u'', mot)
            mot = re.sub(r"-$", u'', mot)
            mot = re.sub(r"\s", u'', mot)

            if mot.lower() in dicoFr and mot != 'Paris':
                mot = mot.lower()

            if len(mot)>2 and mot not in blacklist:
                nuplet = mot
            else:
                nuplet = None
        else:
            nuplet = None

        if nuplet:
            # count global
            if nuplet in words_count:
                words_count[ nuplet ] += 1
            else:
                words_count[ nuplet ] = 1

            if 'count' not in post:  post['count'] = {}
            if nuplet in post['count']:
                post['count'][ nuplet ] += 1
            elif nuplet:
                post['count'][ nuplet ] = 1

            day =  post['day']
            if nuplet not in count_by_day: count_by_day[nuplet] = {}
            
            if day in count_by_day[nuplet]:
                count_by_day[ nuplet ][day] += 1
            elif nuplet:
                count_by_day[ nuplet ][day] = 1

# --  print words_count
sorted_words = sorted( words_count.items(), key=lambda x:x[1], reverse=True )
output = [ x[0]+' %i, '%x[1] for x in sorted_words[:600] ] #+' (%i)'%x[1]
print( '\t'.join( output ) )
print('\n')

print('  -nombre de mot: %i'%len(words_count ))
print('  -nombre de jour: %i'%len(count_by_day ))


# -- save JSON --
json_file = './data_rss/count_global.json'
with open(json_file, 'w') as outfile:
    json.dump(words_count, outfile)

print( ' words_count saved in %s'%json_file )

# -- save JSON --
json_file = './data_rss/count_by_day.json'
with open(json_file, 'w') as outfile:
    json.dump(count_by_day, outfile)

print( ' count_by_day saved in %s'%json_file )


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
