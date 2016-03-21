import json

# save JSON
filename = 'data4eleve.json'

data = json.loads(open(filename).read())

print( 'nbr phrases: %i ' % len( data ) )


from eleve import MemoryStorage
storage = MemoryStorage()

# Then the training itself:
for sentence in data:
      storage.add_sentence( sentence)




from eleve import Segmenter
s = Segmenter(storage)
# segment up to 4-grams, if we used the same storage as before.

nuplets = []
for phrase in data[:100]:
      segmentedPhrase = s.segment( phrase )
      for mots in segmentedPhrase:
            if len( mots )>1:
                  mots = ' '.join( mots )
                  nuplets.append( mots )

print( ' / '.join(nuplets) )

