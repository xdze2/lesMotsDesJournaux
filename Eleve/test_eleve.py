import json

# save JSON
filename = 'data4eleve.json'

data = json.loads(open(filename).read())

print( 'nombre de phrases: %i ' % len( data ) )


from eleve import MemoryStorage
storage = MemoryStorage()

# Then the training itself:
n = 0
for sentence in data:
      n += len( sentence )
      storage.add_sentence( sentence )

print( 'nombre de mots: %i ' % n )


from eleve import Segmenter
s = Segmenter(storage)
# segment up to 4-grams, if we used the same storage as before.

nuplets_count = {}
for phrase in data:
      segmentedPhrase = s.segment( phrase )
      for nuplet in segmentedPhrase:
            if len( nuplet )>1:
                  nuplet = ' '.join( nuplet )
                  if nuplet in nuplets_count:
                        nuplets_count[ nuplet ] += 1
                  else:
                        nuplets_count[ nuplet ] = 1

sorted_nuplets = sorted( nuplets_count.items(), key=lambda x:x[1], reverse=True )

output = [ x[0]+' (%i)'%x[1] for x in sorted_nuplets ]

print( '; '.join( output) )

