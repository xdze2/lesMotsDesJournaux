# coding: utf-8
from flask import Flask, jsonify, render_template, request, g
import sqlite3

import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"

app = Flask(__name__)

DATABASE = '../data/data_lmdjx.db'


def connect_to_database():
    return sqlite3.connect(DATABASE)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    return db


# --------- pages ---------



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot/<ngram>')
def plot_ngram(ngram='lundi'):

    return render_template('plot.html', ngram=ngram)

@app.route('/freqs/')
@app.route('/freqs/<ngram>')
def freqs(ngram=None):

    return render_template('ngramviewer.html', ngram=ngram)

@app.route('/getFreqs',  methods=['GET'])
def getFreqs():
    ngram = request.args.get('ngram', '', type=str)

    print( 'get ngram: %s'%ngram )
    cursor = get_db().cursor()
    cursor.execute( '''SELECT Td.date, IFNULL(Tf.freq, 0 )
                        FROM
                        ( SELECT  date
                        from stats
                        GROUP BY date
                        ) Td
                        LEFT JOIN
                        ( SELECT date, freq
                          FROM stats
                          WHERE ngram = ?
                        ) Tf
                        ON Td.date = Tf.date
                        ORDER BY date(Tf.date)
                        ''', (ngram, ) )


    data = []

    for line in cursor.fetchall():
        data.append( {'date':line[0], 'freq':line[1]  } )


    return jsonify(data=data, ngram=ngram)

@app.route('/post/')
@app.route('/post/<ngram>')
def post(ngram=None):
    return render_template('post.html', ngram=ngram)

@app.route('/post/getPosts')
def getPosts():
    ngram = request.args.get('ngram', '', type=str)
    date = '2016-04-02'

    cursor = get_db().cursor()
    cursor.execute( '''SELECT Toc.date, Tp.title, Tp.summary, Tp.source, Tp.link FROM
                        ( SELECT date, ngram, postid
                            FROM occurences
                            WHERE ngram = ?
                            GROUP BY postid
                            ORDER BY date( date ) DESC ) Toc
                        JOIN ( SELECT ROWID, title, summary, source, link FROM posts ) Tp
                        ON Tp.rowid = Toc.postid
                        LIMIT 100
                        ''', ( ngram, ) )

    data = []
    for line in cursor.fetchall():
        data.append( {'date':line[0], 'title':line[1], \
            'summary':line[2].replace('\n' ,''), 'source':line[3], 'link':line[4] })

    print('request posts for %s'%ngram)
    return jsonify(posts=data, ngram=ngram)


@app.route('/ngrams/search')
def getNgrams():
    """ retourne la liste des nGrams pour l'auto completion
    """
    q = request.args.get('q', '', type=str)

    cursor = get_db().cursor()
    cursor.execute( '''SELECT ngram, sum(freq) c
                        FROM stats
                        WHERE ngram like  ? || '%'
                        GROUP BY ngram
                        ORDER BY c DESC
                        LIMIT 20
                        ''', ( q, ) )

    data = []
    for line in cursor.fetchall():
        data.append( {'ngram':line[0]} )

    return jsonify(data=data)



@app.route('/freqs/getSomePosts')
def getSomePosts():
    ngrams = request.args.get('ngrams', '', type=str)
    date = request.args.get('date', '', type=str)
    ngrams = ngrams.split(',')

    queryparams = [date] + ngrams
    print(queryparams)
    cursor = get_db().cursor()
    cursor.execute( '''SELECT Toc.date, Tp.title, Tp.summary, Tp.source, Tp.link FROM
                        ( SELECT date, ngram, postid
                            FROM occurences
                            WHERE date = ? AND ngram IN (%s)
                            GROUP BY postid
                            ORDER BY date( date ) DESC ) Toc
                        JOIN ( SELECT ROWID, title, summary, source, link FROM posts ) Tp
                        ON Tp.rowid = Toc.postid
                        LIMIT 60
                        '''%','.join(['?']*len(ngrams)), tuple(queryparams) )

    data = []
    for line in cursor.fetchall():
        data.append( {'date':line[0], 'title':line[1], \
            'summary':line[2].replace('\n' ,''), 'source':line[3], 'link':line[4] })

    return jsonify(posts=data, ngrams=ngrams,  date=date)


@app.route('/last10days')
def last10days():
    cursor = get_db().cursor()

    # liste des jours
    cursor.execute( '''SELECT distinct date
                        FROM stats
                        ORDER By Date(date) DESC
                        LIMIT 15  ''' )

    all_dates = []
    for line in cursor.fetchall():
        all_dates.append( line[0] )

    all_dates = all_dates[::-1]

    data4web = []
    for date in all_dates:
        cursor.execute( '''SELECT rowid,  ngram, score
                            FROM stats
                            WHERE date=?
                            ORDER BY score DESC
                            LIMIT 30   ''', (date, ) )

        ngrams4today = []
        for line in cursor.fetchall():
            ngram_dict = { 'label':line[1], 'score':line[2], 'id':line[0] }
            ngrams4today.append( ngram_dict )

        day_dict = {'mots':ngrams4today, 'date':date }
        data4web.append( day_dict )

    return jsonify(data=data4web)

@app.route('/week')
def getWeek():
    start = request.args.get('start', '', type=str)

    cursor = get_db().cursor()
    print( start )
    # liste des jours
    cursor.execute( '''SELECT distinct date
                        FROM stats
                        WHERE Date(date)>=Date(?)
                        ORDER By Date(date)
                        LIMIT 7  ''', (start, ))

    all_dates = []
    for line in cursor.fetchall():
        all_dates.append( line[0] )

    # all_dates = all_dates[::-1]
    print( all_dates)
    data4web = []
    for date in all_dates:
        cursor.execute( '''SELECT rowid,  ngram, score
                            FROM stats
                            WHERE date=?
                            ORDER BY score DESC
                            LIMIT 30   ''', (date, ) )

        ngrams4today = []
        for line in cursor.fetchall():
            ngram_dict = { 'label':line[1], 'score':line[2], 'id':line[0] }
            ngrams4today.append( ngram_dict )

        day_dict = {'mots':ngrams4today, 'date':date }
        data4web.append( day_dict )

    return jsonify(data=data4web)

@app.route('/date')
def datepicker():
    return render_template('datepicker.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8890, debug=True)
