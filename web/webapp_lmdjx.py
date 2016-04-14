# coding: utf-8
from flask import Flask, jsonify, render_template, request, g
import sqlite3

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

@app.route('/data/<ngram>')
def data_ngram(ngram='mardi'):

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

    data_ngram = []
    for line in cursor.fetchall():
        date = line[0]
        freq = line[1]
        data_ngram.append( {'date':date, 'freq':freq  })


    return jsonify(data=data_ngram, ngram=ngram)

@app.route('/post/')
def post():
    return render_template('post.html')

@app.route('/post/_getposts')
def getPosts():
    ngram = request.args.get('ngram', '', type=str)
    date = '2016-04-02'

    cursor = get_db().cursor()
    cursor.execute( '''SELECT Toc.date, Tp.title, Tp.summary, Tp.source FROM
                        ( SELECT date, ngram, postid
                            FROM occurences
                            WHERE ngram = ?
                            GROUP BY postid
                            ORDER BY date( date ) DESC ) Toc
                        JOIN ( SELECT ROWID, title, summary, source FROM posts ) Tp
                        ON Tp.rowid = Toc.postid
                        LIMIT 30
                        ''', ( ngram, ) )
    print('Hello')
    data = []
    for line in cursor.fetchall():
        print(line)
        data.append( {'date':line[0], 'title':line[1], 'summary':line[2].replace('\n' ,''), 'source':line[3]} )

    return jsonify(posts=data)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
