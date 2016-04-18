# -*- coding: utf-8 -*-


import feedparser
import json
import os


import time   # besoin pour time_obj->json
# see https://docs.python.org/2/library/time.html#time.struct_time

# def json_serial(obj):
#     """JSON serializer for objects not serializable by default json code"""
#     print('hello')
#     if isinstance(obj, time.struct_time):
#         serial = tuple( obj )
#         print(serial)
#         return serial
#     raise TypeError ("Type not serializable")

import sys
if sys.version_info[0] < 3:
    raise "Must be using Python 3"
    
print( '... update rss feeds ...' )
print(" " + time.strftime("%x %X") )

feedsToFetch = { \
    'Liberation_laUne': 'http://rss.liberation.fr/rss/latest/',\
    'Liberation_chroniques': 'http://rss.liberation.fr/rss/44/',\
    'leMonde_laUne': 'http://www.lemonde.fr/rss/une.xml',\
    'leMonde_Actu': 'http://www.lemonde.fr/m-actu/rss_full.xml',\
    'leMonde_Idees': 'http://rss.lemonde.fr/c/205/f/3051/index.rss',\
    'lesEchos_journaldujour': 'http://www.lesechos.fr/rss/rss_articles_journal.xml' ,\
    'humanite':'http://www.humanite.fr/rss/actu.rss',\
    'mediapart':'https://www.mediapart.fr/articles/feed',\
    'rue89':'http://api.rue89.nouvelobs.com/feed',\
    'leFigaro_laUne':'http://rss.lefigaro.fr/lefigaro/laune?format=xml',\
    'lePoint_24hinfo':'http://www.lepoint.fr/24h-infos/rss.xml',\
    'lePoint_chroniques':'http://www.lepoint.fr/chroniques/rss.xml',\
    'FranceSoir': 'http://www.francesoir.fr/rss.xml' ,\
    'leParisien': 'http://www.leparisien.fr/actualites-a-la-une.rss.xml#xtor=RSS-1481423633',\
    'courrierinternational':'http://www.courrierinternational.com/feed/all/rss.xml'    }

## load allfeeds_info
dir_rssData = './data/'
feedinfo_filename = dir_rssData + 'allfeeds_info.json'

if not os.path.exists(dir_rssData):
    os.makedirs(dir_rssData)

allfeeds_info = {}
if os.path.isfile(feedinfo_filename):
    with open(feedinfo_filename, 'r') as file:
        allfeeds_info = json.load(file)

    fluxoubliees = [ key for key in allfeeds_info.keys() if key not in feedsToFetch]
    if fluxoubliees:
        print( u'flux oublié(s): '+' '.join(fluxoubliees) )

# Ajoute les nouveaux flux:
for name, url in feedsToFetch.items():
    if name not in allfeeds_info:
        allfeeds_info[name] = {'name':name, 'url':url}

## ---
for name, feed_info in allfeeds_info.items():

    #print('// Request for %s ...' % feed_info['name'])

    ##  --- Query  ---
    if 'etag' in feed_info:
        data = feedparser.parse( feed_info['url'], etag=feed_info['etag'] )
    elif 'modified' in feed_info:
        data = feedparser.parse( feed_info['url'], modified=feed_info['modified'] )
    else:
        data = feedparser.parse( feed_info['url'] )

    ##  --- Tell Status ---
    if 'status' not in data:
        print( name+'_Warning_ : no status, %s' %  data['bozo_exception']   )
    elif data['status'] == 304:
        print( '{:>24s}: pas de nouveaux post (etag or modified)'.format(name) )
    elif data['status'] == 301:
        print( name+'_Warning!_  The feed has permanently moved to a new location. URL updated.' )
        feed_info['url'] = data.href
    elif data['status'] == 410:
        print( name+'_Warning!_  the feed is gone. URL removed. '  )
        feed_info['url'] = None
    elif data['status'] == 200:
        #print( '_no problem!  :) _ '  )
        pass
    else:
        print( name+'_nop_ status: %i '% data['status'])

    ##  --- Tell Bozo ---
    if data['bozo']:
        print( name+'_Warning_ : erreur bozo, %s' %  data['bozo_exception']   )

    ##  --- Go for Entries ---
    if 'entries' in data and len(data['entries'])>0 :

        # print( '_yep_  get %i posts' % len(data['entries'])  )

        # load rss_data file
        filename = dir_rssData + 'rss_data_%s.json' % feed_info['name']
        feed_info['filename'] = filename

        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                rss_data = json.load(file)
        else: rss_data = {}
        nEntriesBefore = len( rss_data )

        # update dico
        nRejected = 0
        nAdded = 0
        for post in data['entries']:
            if 'id' in post:
                key = post['id']
            elif 'link' in post:
                key = post['link']

            if key in rss_data:
                nRejected += 1
            else:
                rss_data[ key ] = post
                nAdded += 1

        print( '{:>24s}: {:>3d} added, {:>3d} rejected, {:>5d} total'.format( \
            name, nAdded, nRejected, len(rss_data) ) )

        # save rss_data file
        with open(filename, 'w') as outfile:
            json.dump(rss_data, outfile )# , default=json_serial)


    ##  --- update FeedInfo ---
    if 'etag' in data:
        feed_info['etag'] = data['etag']
    elif 'modified' in data:
        feed_info['modified'] = data['modified']

    if 'feed' in data and data['feed']:
        feed_info['feed'] = data['feed']
    if 'updated' in data:
        feed_info['updated'] = data['updated']
    if 'updated_parsed' in data:
        feed_info['updated_parsed'] = data['updated_parsed']


# save allfeeds_info
allfeeds_info[ feed_info['name'] ] = feed_info
with open(feedinfo_filename, 'w') as outfile:
    json.dump(allfeeds_info, outfile )#, default=json_serial)
