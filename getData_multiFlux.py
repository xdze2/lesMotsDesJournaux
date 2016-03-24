
# coding: utf-8

# download rss feed
# and archive it

# In[167]:

import xmltodict
import requests
import json
import os
import collections

# In[168]:

data_dir = './data_rss/'

Journaux = []

name = 'leMonde'
url = 'http://www.lemonde.fr/rss/une.xml'
getEntry = lambda x:x['rss']['channel']['item']
Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

name = 'Liberation'
url = 'http://rss.liberation.fr/rss/latest/'
getEntry = lambda x:x['feed']['entry']
Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

name = 'LeFigaro'
url = 'http://rss.lefigaro.fr/lefigaro/laune?format=xml'
getEntry = lambda x:x['rss']['channel']['item']
Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

name = 'courrierinternational'
url = 'http://www.courrierinternational.com/feed/category/6260/rss.xml'
getEntry = lambda x:x['rss']['channel']['item']
Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

name = 'lesechos'
url = 'http://www.lesechos.fr/rss/rss_articles_journal.xml'
getEntry = lambda x:x['rss']['channel']['item']
Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )


name = 'lepoint'
url = 'http://www.lepoint.fr/24h-infos/rss.xml'
getEntry = lambda x:x['rss']['channel']['item']
Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

def getFilename(name):

    filename = data_dir + 'rss_save_' + name + '.json'
    return filename

def update( flux ):
    url = flux['url']
    name = flux['name']
    filename = getFilename( name )
    getEntry = flux['getEntry']

    # load
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            loaded_data = json.load(file)
    else:
        loaded_data = {}
        
    n_avant = len( loaded_data )

    # query
    data = requests.get( url )

    parsed_data =  xmltodict.parse( data.content )
    parsed_data = getEntry(parsed_data)

    new_dict = {}
    for d in parsed_data:
        if d.has_key('guid'):
            if isinstance(d['guid'], collections.Hashable):
                key = d['guid']
            else:
                key = d['guid']['#text']
        elif d.has_key('id'):
            key = d['id']
        else:
            key = d['title']
        new_dict[ key ] = d

    loaded_data.update( new_dict )

    print name, -n_avant+len( loaded_data ), ' added, ', len( loaded_data ), ' total'

    # save
    with open(filename, 'w') as outfile:
        json.dump(loaded_data, outfile)

# -- to parse the desciption --
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# ---



def getdata(filename, src):
    #filename = './data_rss/rss_save_leMonde.json'

    print filename
    loaded_data = json.loads(open(filename).read())

    mydata = []
    for post in loaded_data.itervalues():
        
        mypost = {}
        if 'date' in post:
            mypost['date'] = post['pubDate']
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


#  -- GO --
for journal in Journaux:
    update( journal )

# -- parse and save --
print '\n Consolide:'
d = []
for journal in Journaux:
    filename = getFilename( journal['name'] )
    d.extend( getdata(filename, journal['name'])  )
    
print len( d) 

# save JSON
json_file = data_dir + 'all_title.json'
with open(json_file, 'w') as outfile:
    json.dump(d, outfile)



