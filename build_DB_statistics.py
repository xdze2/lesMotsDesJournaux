# coding: utf-8
import sqlite3
import re

# load DB and create table
database_filename = './data/data_lmdjx.db'


database_connection = sqlite3.connect(database_filename)

cursor = database_connection.cursor()


cursor.execute('''DROP TABLE IF EXISTS frequences''')
cursor.execute( '''CREATE TABLE frequences AS
            SELECT Tdn.date as date, Tdn.ngram as ngram, Tdn.count as count,
                Td.daycount as daycount,
                1000.0*CAST( count as REAL )/CAST( daycount as REAL  ) as freq
            FROM ( SELECT date, ngram, count(*) count
                    FROM occurences
                    GROUP BY ngram, date
                ) Tdn
            JOIN ( SELECT  ngram, count(*) globcount
                    FROM occurences
                    GROUP BY ngram
                    HAVING globcount > 35
                ) Tn
            ON Tn.ngram = Tdn.ngram
            JOIN ( SELECT date, count(*) daycount
                    FROM occurences
                    GROUP BY date
                    HAVING daycount > 500
                ) Td
            ON Td.date = Tdn.date
            ORDER BY date(Tdn.date) DESC ''')


# --- Averages ---
from datetime import datetime

# Calcul le nombre de jours total:

cursor.execute( '''select count(*)
        from (SELECT date FROM frequences GROUP BY date)''')
nbr_joursDB = cursor.fetchone()[0]
print( 'nbr jour DB: %i'%nbr_joursDB )

cursor.execute( ''' SELECT MIN(date) FROM frequences ''')
first_date_txt = cursor.fetchone()[0]
first_date = datetime.strptime(first_date_txt, '%Y-%m-%d' )

cursor.execute( ''' SELECT MAX(date) FROM frequences ''')
last_date_txt = cursor.fetchone()[0]
last_date = datetime.strptime(last_date_txt, '%Y-%m-%d' )

print( first_date, last_date )

delta = last_date - first_date
nbr_jours = delta.days+1

print('\t Nombre de jours: %i' % nbr_jours )
print('\t 1er jour: %s, dernier: %s'%(first_date_txt, last_date_txt))

# moyennes pour chaque ngram:
cursor.execute('''DROP TABLE IF EXISTS moyennes''')
cursor.execute( '''CREATE TABLE moyennes AS
                    SELECT ngram, SUM(freq)/? as avg
                    FROM frequences
                    GROUP BY ngram
                    ORDER By avg DESC
                    ''', (float( nbr_jours ), ) )


# --- SCORE ---
print( '\n---- score ----')
cursor.execute('''DROP TABLE IF EXISTS scores''')
cursor.execute( '''CREATE TABLE scores AS
                SELECT Tf.date as date, Tf.ngram as ngram,
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
                    ''' )
# 
# # --- stats ---
# # merge table scores and frequences
# print( '\n---- stats ----')
# cursor.execute('''DROP TABLE IF EXISTS stats''')
# cursor.execute( '''CREATE TABLE stats AS
#                 SELECT Tfreq.date as date, Tfreq.ngram as ngram,
#                 Tfreq.freq as freq,  Tscore.score as score, Tfreq.count as count
#                     FROM  (
#                         SELECT date, ngram, freq, count
#                         FROM frequences
#                         ) Tfreq
#                     JOIN (
#                         SELECT date, ngram, score
#                         FROM scores
#                         ) Tscore
#                     ON Tfreq.ngram = Tscore.ngram and Tfreq.date = Tscore.date
#                     ''' )
#

# # freq par jour et par un mot:
# cursor.execute('''DROP TABLE IF EXISTS frequences''')
# cursor.execute( '''CREATE TABLE frequences AS
#                     SELECT Ttot.date, Tmot.ngram, cMot as count, cTot,
#             1000.0*CAST(cMot as real)/CAST(cTot as real) as freq \
#                     FROM (
#                         SELECT date, ngram, COUNT(*) as cMot\
#                         FROM occurences\
#                         /*WHERE (SELECT count(*) as c FROM occurences WHERE  )*/
#                         GROUP BY date, ngram \
#                         ) Tmot \
#                     JOIN (
#                         SELECT date, COUNT(*) as cTot \
#                         FROM occurences\
#                         GROUP BY date \
#                         HAVING cTot > 100 \
#                         ) Ttot \
#                     ON Ttot.date = Tmot.date ''')


## freq. Timeline
# ngram = 'France'
#
# cursor.execute( ''' SELECT Tall.date, IFNULL(Tngram.freq, 0)
#                     FROM (
#                         SELECT DISTINCT date \
#                         FROM frequences\
#                         ) Tall \
#                     LEFT JOIN (
#                         SELECT date, freq \
#                         FROM frequences \
#                         WHERE ngram = ? \
#                         ) Tngram \
#                     ON Tall.date = Tngram.date ''', (ngram, ) )
# print('data for ngram=%s :'%ngram)
#
# for line in cursor.fetchall():
#     print( line )
#
# # Count par jour
# print( '\n---- Count par jour ----')
# cursor.execute( '''SELECT date, Count(*)
#                     FROM frequences
#                     GROUP BY date
#                     ORDER By -Date(date)
#                     ''' )
#
# for line in cursor.fetchall():
#     print( line )



# cursor.execute('''DROP TABLE IF EXISTS scores''')
# cursor.execute('''DROP TABLE IF EXISTS frequences''')

# print('data for ngram=%s :'%ngram)
# for line in cursor.fetchall():
#     print( line )
# IFNULL(cMot, 0)

# for line in cursor.fetchall():
#     print(line)

# We can also close the connection if we are done with it.
database_connection.close()

print( '%s closed '% database_filename)
