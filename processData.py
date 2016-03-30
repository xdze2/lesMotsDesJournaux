import json
import re

# see https://github.com/kodexlab/eleve

print(' --- Process Data ---')
# --- Data for ELeVE ---

blacklist = [u'LE SCAN SPORT', u'EN IMAGES', u'LE SCAN POLITIQUE', u'LE SCAN TÉLÉ', u'LIRE AUSSI' ]
blacklist.extend( [u'LE SCAN TÉLÉ', u'LE SCAN ÉCO', u'LE SCAN ECO' , u"Toute l'actualité", u"Le Point", u'INFO LE FIGARO'] )
blacklist.extend( ['Le Monde', 'EN DIRECT', 'CARTE INTERACTIVE', 'FIGAROVOX TRIBUNE', u'VIDÉOS'] )
blacklist.extend( ['MILLIONS DE DOLLARS', 'INTERVIEW', 'ENTRETIEN', u'VIDÉO', 'INFOGRAPHIE'] )
blacklist.extend( ['FIGAROVOX', 'TRIBUNE', 'REPORTAGE'] )
blacklist.extend( ['entre eux', 'Top 14', 'Zapping du Point'] )

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

# load
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

# -- save JSON --
json_file = filename
with open(json_file, 'w') as outfile:
    json.dump(data, outfile)

print( ' [formatedtext] saved in %s'%json_file )


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


nuplets_set = set()
for post in data:
    phrase = post['formatedtext']
    segmentedPhrase = s.segment( phrase.split(' ') )

    for nuplet in segmentedPhrase:
        while '' in nuplet: nuplet.remove( '' )

        if len( nuplet )>1:
            nuplet = ' '.join( nuplet )

            # enleve l'apostrophe du debut:
            nuplet_apoless = re.sub(r"^[LldDsSnNcC][’']", u'', nuplet)

            nuplets_set.add( nuplet_apoless )

# Count global:
nuplets_count = {}
seuil = 3
print( ' // freq. min pour garder un Nuplet: %i' % seuil )

all_text = ' '.join( [post['formatedtext'] for post in data] )
for nuplet in nuplets_set:
     c = all_text.count( nuplet )
     if c > seuil:
         nuplets_count[ nuplet ] = c

sorted_nuplets = sorted( nuplets_count.items(), key=lambda x:x[1], reverse=True )

output = [ x[0]+' (%i)'%x[1] for x in sorted_nuplets ]# if x[1] > 1 ]

print( '; '.join( output) )

print('\n')

# save JSON
json_file = './data_rss/data_nuplets.json'
with open(json_file, 'w') as outfile:
    json.dump(nuplets_count, outfile)

print( ' Nuplets saved in %s'%json_file )
