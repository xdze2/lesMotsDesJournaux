import json
import re

import dataExtern
# see https://github.com/kodexlab/eleve

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
# segment up to 4-grams, if we used the same storage as before.

nuplets_count = {}
for post in data:
    phrase = post['formatedtext']
    segmentedPhrase = s.segment( phrase.split(' ') )

    nuplet_set = set()
    for nuplet in segmentedPhrase:
        while '' in nuplet: nuplet.remove( '' )

        if len( nuplet ) > 1:
            nuplet = ' '.join( nuplet )

            # enleve l'apostrophe du debut si besoin:
            nuplet_apoless = re.sub(r"^[LldDsSnNcC][’']", u'', nuplet)

            nuplet_set.add( nuplet_apoless )

    # -- count local & global
    if 'count' not in post:  post['count'] = {}

    for nuplet in nuplet_set:
        c = post['formatedtext'].count( nuplet )

        # remove nuplet from formatedtext to count 1-uplets
        post['formatedtext'] = post['formatedtext'].replace(  nuplet, u'<>' )

        post['count'].update( {nuplet:c} )

        # count global
        if nuplet in nuplets_count:
            nuplets_count[nuplet] += c
        else:
            nuplets_count[nuplet] = c

#seuil = 3
#print( ' // freq. min pour garder un Nuplet: %i' % seuil )

# --  print Nuplets
sorted_nuplets = sorted( nuplets_count.items(), key=lambda x:x[1], reverse=True )
output = [ x[0]+' (%i)'%x[1] for x in sorted_nuplets[:100] ]

print( '; '.join( output ) )
print('\n')

# save JSON
json_file = './data_rss/data_nuplets.json'
with open(json_file, 'w') as outfile:
    json.dump(nuplets_count, outfile)

print( ' Nuplets saved in %s'%json_file )


# -- save JSON --
json_file = filename
with open(json_file, 'w') as outfile:
    json.dump(data, outfile)

print( ' [formatedtext]&[count] saved in %s'%json_file )

# ---------- After ELeVE ----------
print( '   - After ELeVE -')

dicoFr = dataExtern.getDicoFr()

blacklist = dataExtern.getBlacklistAfterEleve()


# count words
words_count = {}
for post in data:
    mots = post['formatedtext'].split(' ')

    for mot in mots:
        mot = re.sub(u"[Aa]ujourd.hui",  '', mot)
        mot = re.sub(u"jusqu.([àa]|en)",  '', mot)

        mot = re.sub(u"(^|\s)[LldDsSnNcCjJ]['`’]", "", mot)
        mot = re.sub(u"(^|\s)qu['`’]", "", mot)
        mot = re.sub(r"[0-9\.\(\)]", u'', mot)
        mot = re.sub(r"-$", u'', mot)
        mot = re.sub(r"\s", u'', mot)

        if mot.lower() in dicoFr:
            mot = mot.lower()

        #if mot.endswith( 's' ) and mot[0:-1] in dicoFr:
        #    mot = mot[:-1]      ... pas une bonne idee dans>dan

        if len( mot )>2 and mot.lower() not in blacklist:
            if mot in words_count:
                words_count[ mot ] += 1
            elif mot:
                words_count[ mot ] = 1

            if mot in post['count']:
                post['count'][ mot ] += 1
            elif mot:
                post['count'][ mot ] = 1

dataExtern.printSorted( words_count , 200)
