# coding: utf-8
import sqlite3
import re

# load DB and create table
database_filename = './data/data_lmdjx.db'


database_connection = sqlite3.connect(database_filename)
cursor = database_connection.cursor()



# --- Train ELeVE ---
print( '> ELeVE: training')

import lmdjxtools
from eleve import MemoryStorage
storage = MemoryStorage()

n, nPosts = 0, 0
cursor.execute('SELECT title, summary FROM posts')
for line in cursor.fetchall():
    formattedtext = lmdjxtools.format( ' '.join( line )   )
    mots = formattedtext.split(' ')
    storage.add_sentence( mots  )
    n += len( mots )
    nPosts += 1

print( '\t %s one-grams (non-unique) found in %s sentences'%\
    ( '{:,}'.format(n), '{:,}'.format(nPosts))  )


print( '> ELeVE: Segment & count')
dicoFr = lmdjxtools.getDicoFr()
blacklist_afterEleve = lmdjxtools.blacklist_afterEleve()

# Create table occurences
cursor.execute('''DROP TABLE IF EXISTS occurences''')
cursor.execute('''CREATE TABLE occurences
             (date text, ngram text, source text)''')  #postid?
print('\t reset table DB.occurences')

from eleve import Segmenter
s = Segmenter(storage)

rejected_ngrams = set()
i = 0
cursor.execute('SELECT date, source, title, summary  FROM posts')
for line in cursor.fetchall():
    date = line[0]
    source = line[1]
    formattedtext = lmdjxtools.format( ' '.join( line[2:3] )   )

    segmentedPhrase = s.segment( formattedtext.split(' ') )

    # print(segmentedPhrase)

    for ngram in segmentedPhrase:

        if len( ngram ) > 1:
            # Filrage pour les (<1)-grams
            # si le n-gram est trop rare, on le split en 1-gram
            if storage.query_count( ngram ) > 2:
                ngram = ' '.join( ngram )
            else:
                segmentedPhrase.extend( [ [x] for x in ngram ] )
                rejected_ngrams.add( '_'.join( ngram ) )
                continue
        elif len( ngram[0] )>2:# and storage.query_count( ngram ) > 1 :
            # Filrage pour les 1-grams
            ngram = ngram[0]
        else:
            rejected_ngrams.add( ngram[0] )
            continue

        # Retire l'apostrophe du début:
        ngram = re.sub(u"^[LldDsSnNcCjJ]['`’]", u'', ngram)
        ngram = re.sub(u"^qu['`’]", u'', ngram)

        if ngram.lower() in dicoFr and ngram != 'Paris':
            ngram = ngram.lower()

        if len(ngram)>2 and ngram in blacklist_afterEleve:
            continue

        # Insert a row of data
        cursor.execute("INSERT INTO occurences VALUES \
                (?, ?, ?)", (date, ngram, source))

    lmdjxtools.progressbar(i, nPosts) # print la bar de progression
    i += 1


# log rejected ngrams
lmdjxtools.log2file( '%i '%len(rejected_ngrams)+ ', '.join(list(rejected_ngrams)), 'rejected_ngram.txt' )


# Save (commit) the changes
database_connection.commit()

# Some stats on DB.occurences:
cursor.execute('SELECT COUNT(*) FROM occurences')
print( '\t %s lines in DB.occurences '% '{:,}'.format( cursor.fetchone()[0] ))

cursor.execute('SELECT COUNT( DISTINCT ngram )  FROM occurences')
print( '\t %s distinct n-grams in DB.occurences '% '{:,}'.format( cursor.fetchone()[0] ))

# We can also close the connection if we are done with it.
database_connection.close()

print( '%s closed '% database_filename)
