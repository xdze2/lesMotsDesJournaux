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
                    HAVING globcount > 5 /*filtre sur le nbre min occurences d'un ngram*/
                ) Tn
            ON Tn.ngram = Tdn.ngram
            JOIN ( SELECT date, count(*) daycount
                    FROM occurences
                    GROUP BY date
                    HAVING daycount > 400 /*filtre sur le nbre min. de mots par jour*/
                ) Td
            ON Td.date = Tdn.date
            ORDER BY date(Tdn.date) DESC ''')



# Cherche le nombre de jours total:

cursor.execute( '''select count(*)
        from (SELECT date FROM frequences GROUP BY date)''')
nbr_joursDB = cursor.fetchone()[0]


print('\t Nombre de jours: %i' % nbr_joursDB )


# moyennes pour chaque ngram:
cursor.execute('''DROP TABLE IF EXISTS moyennes''')
cursor.execute( '''CREATE TABLE moyennes AS
                    SELECT ngram, SUM(freq)/? as avg
                    FROM frequences
                    GROUP BY ngram
                    ORDER By avg DESC
                    ''', (float( nbr_joursDB ), ) )


# --- SCORE ---
# CAST(Tf.freq as real)/CAST(Tm.avg as real)-1.0 as score
print( '---- score ----')
cursor.execute('''DROP TABLE IF EXISTS scores''')
cursor.execute( '''CREATE TABLE scores AS
                SELECT Tf.date as date, Tf.ngram as ngram,
            CAST(Tf.freq as real) - CAST(Tm.avg as real) as score
                    FROM  (
                        SELECT date, ngram, freq
                        FROM frequences
                        ) Tf
                    LEFT JOIN (
                        SELECT ngram, avg
                        FROM moyennes
                        ) Tm
                    ON Tf.ngram = Tm.ngram
                    ORDER BY DATE( Tf.date ) DESC, score DESC
                    ''' )

# --- stats ---
# merge table scores and frequences
print( '---- stats ----')
cursor.execute('''DROP TABLE IF EXISTS stats''')
cursor.execute( '''CREATE TABLE stats AS
                SELECT Tfreq.date as date, Tfreq.ngram as ngram,
                Tfreq.freq as freq,  Tscore.score as score, Tfreq.count as count
                    FROM  (
                        SELECT date, ngram, freq, count
                        FROM frequences
                        ) Tfreq
                    JOIN (
                        SELECT date, ngram, score
                        FROM scores
                        ) Tscore
                    ON Tfreq.ngram = Tscore.ngram and Tfreq.date = Tscore.date
                    ''' )

print( '- remove tables scores & frequences')
cursor.execute('''DROP TABLE IF EXISTS scores''')
cursor.execute('''DROP TABLE IF EXISTS frequences''')

cursor.execute( '''select count(*) FROM stats''')
nbr_ngrams = cursor.fetchone()[0]

print( '\t %s rows in table Stats'% '{:,}'.format(nbr_ngrams)  )

database_connection.close()
print( '%s closed '% database_filename)


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
