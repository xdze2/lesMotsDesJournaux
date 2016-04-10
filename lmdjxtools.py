# coding: utf-8
import os
import re

blacklist_beforeEleve =  [u'LE SCAN SPORT', u'EN IMAGES', u'LE SCAN POLITIQUE',\
    u'LE SCAN TÉLÉ', u'LIRE AUSSI' , u'LE SCAN TÉLÉ', u'LE SCAN ÉCO', u'LE SCAN ECO',\
    u"Toute l'actualité", u"Le Point", u'INFO LE FIGARO', 'Le Monde', \
    'EN DIRECT', 'CARTE INTERACTIVE', 'FIGAROVOX TRIBUNE', u'VIDÉOS', \
    'MILLIONS DE DOLLARS', 'INTERVIEW', 'ENTRETIEN', u'VIDÉO', 'INFOGRAPHIE', \
    'FIGAROVOX', 'TRIBUNE', 'REPORTAGE', 'FOCUS', \
    'entre eux', 'Top 14', 'Zapping du Point', 'noTitle']


def format( texte ):
    """ Formate le texte title+description pour ELeVE (DB.posts)
    """

    # Rq: l'ordre est important ...

    #texte = texte.replace(u'\xa0', u' ') # espace insécable

    # Ponctuation:
    myRe = u"""[,;:«»"?!\n\r…©“”()]"""
    texte = re.sub(myRe, u' ', texte)

    # enleve les points en gardant ceux des initials:
    texte = re.sub(r'(?<![A-Z0])\.', u'', texte)

    # espace des milliers 10_000->10000:
    texte = re.sub(r'([0-9]+)\s([0-9]+)', r'\1\2', texte)
    texte = re.sub(u'([0-9.,]+)\s([%€])', r'\1\2', texte)  # pourcentage...etc

    for mot in blacklist_beforeEleve:
        texte = texte.replace( mot, u'')

    texte = re.sub(r'\s[.\-]\s', u' ', texte) # point ou tiret solo
    texte = re.sub(r'\s', u' ', texte) # remove tab and other strange space
    texte = re.sub(r'\s+', u' ', texte) # remove double space
    texte = texte.strip()

    return texte


import codecs

def getDicoFr():
    filename = './listesMots_fr/liste_mots_utf8.txt'
    # cf: http://www.lexique.org/listes/liste_mots.txt

    with codecs.open(filename, encoding='utf-8') as f:
        listemots = f.readlines()

    for i, mot in enumerate( listemots ):
        a = mot.split('\t')
        freq = float(a[1])
        word = a[0]
        listemots[i] = (word, freq)

    dicoFr = { x[0]:x[1] for x in listemots }

    return dicoFr

def blacklist_afterEleve():
    # en minuscule
    blacklist = ['etat', 'etats', 'euros', u'est-il', 'actu', u'a-t-il', 'ont-ils', 'a-t-on', 'va-t-il', u'elle-même']
    blacklist.extend( ['axa', u'après-midi', 'a-t-elle', 'faut-il', u'peut-être', 'the', 'sont-elles'] )
    blacklist.extend(['week-end', u'lui-même', u"qu'on", 'celle-ci', 'celui-ci', u'au-delà', 'est-elle', 'sont-ils'])
    blacklist.extend([u'Libé', u'œil', u'œuvre', 'zapping', 'editorial', 'aura-t-il'])

    blacklist.extend( getStopWords() )

    for mot in blacklist:
        mot = mot.lower()

    return blacklist

def getStopWords():
    filename = './listesMots_fr/stop_words_fr.txt'
    with codecs.open(filename, encoding='utf-8') as f:
        listemots = f.readlines()

    stopwords = []
    for line in listemots:
        m = re.match(u'([^\s|]*)', line )
        if m and m.group():
            if m.group() not in stopwords:
                stopwords.append( m.group() )

    return stopwords


# Print iterations progress
# http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
import  sys
def progressbar (iteration, total, prefix = '', suffix = '', decimals = 0, barLength = 50):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterations  - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('%s [%s] %s%s %s\r' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration > total-2:
        print(" ")

def log2file( texte, filename ):
    log_filename = './log/' + filename
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    with open(log_filename, "w") as log_file:
        print( texte, file=log_file )
    print('... log created in %s'%log_filename)
