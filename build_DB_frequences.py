# coding: utf-8
import sqlite3
import re

# load DB and create table
database_filename = './data/data_lmdjx.db'


database_connection = sqlite3.connect(database_filename)
cursor = database_connection.cursor()


# freq par jour et par un mot:
cursor.execute('''DROP TABLE IF EXISTS frequences''')
cursor.execute( '''CREATE TABLE frequences AS
                    SELECT Ttot.date, Tmot.ngram, cMot as count, cTot,
            1000.0*CAST(cMot as real)/CAST(cTot as real) as freq \
                    FROM (
                        SELECT date, COUNT(*) as cTot \
                        FROM occurences\
                        GROUP BY date \
                        HAVING cTot > 500 \
                        ) Ttot \
                    JOIN (
                        SELECT date, ngram, COUNT(*) as cMot\
                        FROM occurences\
                        GROUP BY date, ngram \
                        ) Tmot \
                    ON Ttot.date = Tmot.date ''')


# freq. Timeline
ngram = 'France'

cursor.execute( ''' SELECT Tall.date, IFNULL(Tngram.freq, 0)
                    FROM (
                        SELECT DISTINCT date \
                        FROM frequences\
                        ) Tall \
                    LEFT JOIN (
                        SELECT date, freq \
                        FROM frequences \
                        WHERE ngram = ? \
                        ) Tngram \
                    ON Tall.date = Tngram.date ''', (ngram, ) )
print('data for ngram=%s :'%ngram)

for line in cursor.fetchall():
    print( line )

# Count par jour
print( '\n---- Count par jour ----')
cursor.execute( '''SELECT date, Count(*)
                    FROM frequences
                    GROUP BY date
                    ORDER By -Date(date)
                    ''' )

for line in cursor.fetchall():
    print( line )

# --- Averages ---
from datetime import datetime

# Calcul le nombre de jours total:

cursor.execute( ''' SELECT MIN(date) FROM frequences; ''')
first_date = cursor.fetchone()[0]
first_date = datetime.strptime(first_date, '%Y-%m-%d' )

cursor.execute( ''' SELECT MAX(date) FROM frequences; ''')
last_date = cursor.fetchone()[0]
last_date = datetime.strptime(last_date, '%Y-%m-%d' )

print( first_date, last_date )

delta = last_date - first_date
nbr_jours = delta.days

#   enfait: un mot nouveau (qui apparait un seul jour) sort avec le score=nrb de jours
# parce que sa moyenne*bre jours et sa freq sont les mêmes  ... ?
# cad que faire des mots (non signifiant) qui apparaise que un seul jour -, 

cursor.execute('''DROP TABLE IF EXISTS moyennes''')
cursor.execute( '''CREATE TABLE moyennes AS
                    SELECT ngram, SUM(freq)/? as avg
                    FROM frequences
                    GROUP BY ngram
                    ORDER By -avg
                    ''', (float( nbr_jours ), ) )

for line in cursor.fetchall():
    print( line )


# --- SCORE ---
print( '\n---- score ----')
cursor.execute( ''' SELECT Tf.date, Tf.ngram,
            CAST(Tf.freq as real)/CAST(Tm.avg as real)-1.0 as score
                    FROM  (
                        SELECT date, ngram, freq
                        FROM frequences
                        ) Tf
                    LEFT JOIN (
                        SELECT ngram, avg
                        FROM moyennes
                        ) Tm
                    ON Tf.ngram = Tm.ngram
                    WHERE score > 1
                    ORDER BY DATE( Tf.date ) DESC, score DESC
                    LIMIT 5000
                    ''' )

import lmdjxtools
texte = ''
for line in cursor.fetchall():
    texte += str( line )+'\n'
lmdjxtools.log2file( texte, 'score_table.txt' )

# print('data for ngram=%s :'%ngram)
# for line in cursor.fetchall():
#     print( line )
# IFNULL(cMot, 0)

# for line in cursor.fetchall():
#     print(line)

# We can also close the connection if we are done with it.
database_connection.close()

print( '%s closed '% database_filename)
