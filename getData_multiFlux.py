# coding: utf-8

# Download rss feed
# and archive it


import xmltodict
import requests
import json
import os
import collections
import re

print(' --- Get Data ---')



import config_flux
# ------------------------


def update( flux ):
    url = flux['url']
    name = flux['name']
    filename = config_flux.getFilename( name )
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
        if 'guid' in d:
            if isinstance(d['guid'], collections.Hashable):
                key = d['guid']
            else:
                key = d['guid']['#text']
        elif 'id' in d:
            key = d['id']
        else:
            key = d['title']
        new_dict[ key ] = d

    loaded_data.update( new_dict )

    delta = len( loaded_data )-n_avant
    print(  '%s : %i added , %i total' % (name, delta, len( loaded_data ) ) )

    # save
    with open(filename, 'w') as outfile:
        json.dump(loaded_data, outfile)
        print( '  data saved in %s'%filename )



#  -- GO --

Journaux = config_flux.getJournaux()

for journal in Journaux:
    update( journal )

print('\n ')
