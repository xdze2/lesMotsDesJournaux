# coding: utf-8

import json

import re
import os
import sqlite3
from dateutil import parser


# -- Remove HTML Tags --
removeTags = re.compile(r'<.*?>')
def strip_tags(data):
    return removeTags.sub('', data)


matchSourceName = { \
'courrierinternational':'courrierinternational', \
'leMonde':'leMonde_laUne',\
'lesechos':'lesEchos_journaldujour',\
'LeFigaro': 'leFigaro_laUne',\
'lepoint':'lePoint_24hinfo',\
'Liberation':'Liberation_laUne' }

# ---
data_dir = './dataRssAvant6avril/'

filelist = os.listdir(data_dir)

journaux = []
for filename in filelist:
    m = re.findall( r'rss_save_([a-zA-Z]+).json', filename )
    if m:
        journaux.append(m[0])

## -- load DB --
database_filename = './data/data_lmdjx.db'


database_connection = sqlite3.connect(database_filename)
database = database_connection.cursor()

# -------------------------------------
print(' --- Parse the Data ---')


for name in journaux:

    # load
    filename = data_dir + 'rss_save_' + name + '.json'

    print(  filename )
    loaded_data = json.loads(open(filename).read())

    for post in loaded_data.values():

        if 'date' in post:
            datetime_txt = post['date']
        elif 'pubDate' in post:
            datetime_txt = post['pubDate']
        elif 'updated' in post:
            datetime_txt = post['updated']

        dt = parser.parse( datetime_txt )
        date = dt.date().isoformat()  # on oublie l'heure

        source = matchSourceName[name]
        title = post['title']

        if not title: title = 'noTitle'
        if 'description' in post:
            summary_html = post['description']
        elif 'summary' in post and u'#text' in post['summary']:
            summary_html =  post['summary'][u'#text']
        else:
            summary_html = ''

        if summary_html:
            summary = strip_tags( summary_html )
        else:
            summary = ''


        link = None

        # Insert a row of data
        database.execute("INSERT INTO posts VALUES \
            (?, ?, ?, ?, ?)", (date, title, summary, link, source))

# Save (commit) the changes
database_connection.commit()

database.execute('SELECT COUNT(*) FROM posts')
print( 'rows in DB: %i '% database.fetchone()[0])

# We can also close the connection if we are done with it.
database_connection.close()

print( '  // %s closed '% database_filename)
