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


if __name__ == '__main__':
    app.run(debug=True)
