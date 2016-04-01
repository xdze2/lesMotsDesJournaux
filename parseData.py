# coding: utf-8


# -- parse and save --

import xmltodict
import requests
import json
import os
import collections
import re
from datetime import datetime

# -- Remove HTML Tags --

def strip_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
# ---


def getdata(filename, src):

    print(  filename )
    loaded_data = json.loads(open(filename).read())

    mydata = []
    for post in loaded_data.values():

        mypost = {}
        if 'date' in post:
            mypost['date'] = post['date']
        elif 'pubDate' in post:
            mypost['date'] = post['pubDate']
        elif 'updated' in post:
            mypost['date'] = post['updated']



        mypost['source'] = src
        mypost['title'] = post['title']

        if 'description' in post:
            if post['description']:
                mypost['description'] = strip_tags( post['description'] )
        elif 'summary' in post:
            if u'#text' in post['summary']:
                mypost['description'] = strip_tags( post['summary'][u'#text'] )

        mydata.append( mypost )

    return mydata



# -------------------------------------
print(' --- Parse the Data ---')



import config_flux
Journaux = config_flux.getJournaux()

alldata = []
for journal in Journaux:
    filename = config_flux.getFilename( journal['name'] )
    alldata.extend( getdata(filename, journal['name'])  )

print(  '  nombre de posts: %i'%len( alldata ) )


# Work with DATE

for post in alldata:
    txt_date = post['date']
    txt_date = txt_date.replace(u'GMT', u'')
    txt_date = re.sub('\+[0-9]{4}', u'', txt_date) # !! not the real hour ..
    txt_date = txt_date.strip()

    try:
        date = datetime.strptime(txt_date, '%a,  %d %b %Y %H:%M:%S')
    except:
        txt_date = re.sub('\+0[0-9]:00$', u'', txt_date) # !! not the real hour ..
        try:
            date = datetime.strptime(txt_date, '%Y-%m-%dT%H:%M:%S')
        except:
            print(  txt_date )
    post['date'] = date.isoformat()

    date_str = post['date']
    date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    day_tuple = ( date.day, date.month, date.year )
    post['day'] = day_tuple

# save JSON
json_file = './data_rss/all_title.json'
with open(json_file, 'w') as outfile:
    json.dump(alldata, outfile)
    print( ' Parsed data saved in %s'%json_file )
