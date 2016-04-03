# coding: utf-8

# note:
#  http://www.humanite.fr/rss/actu.rss
# http://www.francesoir.fr/rss.xml
# http://www.leparisien.fr/actualites-a-la-une.rss.xml#xtor=RSS-1481423633

def getJournaux():

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

    # name = 'courrierinternational'
    # url = 'http://www.courrierinternational.com/feed/category/6260/rss.xml'
    # getEntry = lambda x:x['rss']['channel']['item']
    # Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

    name = 'lesechos'
    url = 'http://www.lesechos.fr/rss/rss_articles_journal.xml'
    getEntry = lambda x:x['rss']['channel']['item']
    Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )


    name = 'lepoint'
    url = 'http://www.lepoint.fr/24h-infos/rss.xml'
    getEntry = lambda x:x['rss']['channel']['item']
    Journaux.append( {'name':name, 'url':url, 'getEntry':getEntry} )

    return Journaux


def getFilename(name):
    data_dir = './data_rss/'

    filename = data_dir + 'rss_save_' + name + '.json'
    return filename
