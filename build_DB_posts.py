# coding: utf-8
import os
import json
import sqlite3
import re
import dateutil

# -- Remove HTML Tags --
removeTags = re.compile(r'<.*?>')
def strip_tags(data):
    return removeTags.sub('', data)

## -- create DB --
database_filename = './data/data_lmdjx.db'

# remove if exist DB ...
if os.path.isfile( database_filename ):
    os.remove( database_filename )
    print( '  // %s removed'% database_filename)

database_connection = sqlite3.connect(database_filename)
database = database_connection.cursor()

# Create table
database.execute('''CREATE TABLE posts
             (date text, title text, summary text, link text, source text)''')

## -- load allfeeds_info --
dir_rssData = './data/'
feedinfo_filename = dir_rssData + 'allfeeds_info.json'

allfeeds_info = {}

with open(feedinfo_filename, 'r') as file:
    allfeeds_info = json.load(file)

for name, feed_info in allfeeds_info.items():

    # load rss data
    dataRss_filename = feed_info['filename']
    with open(dataRss_filename, 'r') as file:
        dataRss = json.load(file)

    for datapost in dataRss.values():

        source = name
        title = strip_tags(  datapost['title'] )
        if 'summary' in datapost:
            summary = strip_tags( datapost['summary'] )
        else:
            summary = None
        link = datapost['link']
        if 'published' in datapost:
            datetime_txt = datapost['published']
        elif 'updated' in datapost:
            datetime_txt = datapost['updated']

        dt = dateutil.parser.parse( datetime_txt )
        date = dt.date().isoformat()  # on oublie l'heure

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
