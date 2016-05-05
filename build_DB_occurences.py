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

cursor.execute('SELECT count(*) FROM posts')
nPosts = cursor.fetchone()[0]

nMots = 0
i = 0
cursor.execute('SELECT title, summary FROM posts')
for line in cursor.fetchall():
    for phrase in line:
        formattedtext = lmdjxtools.format( phrase )
        listeMots = formattedtext.split(' ')
        storage.add_sentence( listeMots  )
        nMots += len( listeMots )
    lmdjxtools.progressbar(i, nPosts) # print la bar de progression
    i += 1

print( '\t %s one-grams (non-unique) found in %s sentences'%\
    ( '{:,}'.format(nMots), '{:,}'.format(nPosts))  )

print( '> ELeVE: Segment & count')
dicoFr = lmdjxtools.getDicoFr()
blacklist_afterEleve = lmdjxtools.blacklist_afterEleve()

# Create table occurences
cursor.execute('''DROP TABLE IF EXISTS occurences''')
cursor.execute('''CREATE TABLE occurences
             (date text, ngram text, source text, postid integer)''')  #postid?
print('\t reset table DB.occurences')

from eleve import Segmenter
s = Segmenter(storage)

rejected_ngrams = set()
i = 0
cursor.execute('SELECT date, source, title, summary, rowid FROM posts')
for line in cursor.fetchall():
    date = line[0]
    source = line[1]
    postid = line[4]


    segmentedPhrase = []
    for phrase in line[2:3]:
        formattedtext = lmdjxtools.format( phrase   )
        segmentedPhrase += s.segment( formattedtext.split(' ') )


    ngramAdded = set()
    for ngram in segmentedPhrase:

        if len( ngram ) > 1:
            # Filrage pour les (<1)-grams
            # si le n-gram est trop rare, on le split en 1-gram
            if storage.query_count( ngram ) > 2:
                ngram = ' '.join( ngram )
            else:
                #segmentedPhrase.extend( [ [x] for x in ngram ] )
                rejected_ngrams.add( '_'.join( ngram ) )
                continue
        else:
            ngram = ngram[0]

        # Retire l'apostrophe du début:
        ngram = re.sub(u"^[LldDsSnNcCjJ]['`’]", u'', ngram)
        ngram = re.sub(u"^qu['`’]", u'', ngram)

        if len(ngram)<=1 or ngram.lower() in blacklist_afterEleve:
            continue

        if ngram.lower() in dicoFr and ngram != 'Paris':
            ngram = ngram.lower()

        # Insert a row of data
        if ngram not in ngramAdded:
            ngramAdded.add( ngram )
            cursor.execute("INSERT INTO occurences VALUES \
                    (?, ?, ?, ?)", (date, ngram, source, postid))

    lmdjxtools.progressbar(i, nPosts) # print la bar de progression
    i += 1


# log rejected ngrams
# nRejected = len(rejected_ngrams)
# lmdjxtools.log2file( '%i '%nRejected+ ', '.join(list(rejected_ngrams)), 'rejected_ngram.txt' )
#

# Save (commit) the changes
database_connection.commit()

## Some stats on DB.occurences:
# print( '\t %s n-grams rejected '% '{:,}'.format( nRejected ))

cursor.execute('SELECT COUNT(*) FROM occurences')
print( '\t %s lines in DB.occurences '% '{:,}'.format( cursor.fetchone()[0] ))

cursor.execute('SELECT COUNT( DISTINCT ngram )  FROM occurences')
print( '\t %s distinct n-grams in DB.occurences '% '{:,}'.format( cursor.fetchone()[0] ))

# We can also close the connection if we are done with it.
database_connection.close()

print( '%s closed '% database_filename)
