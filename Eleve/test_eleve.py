import json
import re

# https://github.com/kodexlab/eleve

# save JSON
filename = 'data4eleve.json'

data = json.loads(open(filename).read())

print( 'nombre de phrases: %i ' % len( data ) )


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
seuil = 2

all_text = ' '.join( [post['formatedtext'] for post in data] )
for nuplet in nuplets_set:
     c = all_text.count( nuplet )
     if c > seuil:
         nuplets_count[ nuplet ] = c

sorted_nuplets = sorted( nuplets_count.items(), key=lambda x:x[1], reverse=True )

output = [ x[0]+' (%i)'%x[1] for x in sorted_nuplets ]# if x[1] > 1 ]

print( '; '.join( output) )

# save JSON
json_file = './data_nuplets.json'
with open(json_file, 'w') as outfile:
    json.dump(nuplets_count, outfile)
