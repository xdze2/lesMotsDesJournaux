# Load "liste des mots"
import codecs
import re

def getDicoFr():
    filename = './data_dico/liste_mots_utf8.txt'
    # cf: http://www.lexique.org/listes/liste_mots.txt
    # load
    with codecs.open(filename, encoding='utf-8') as f:
        listemots = f.readlines()

    for i, mot in enumerate( listemots ):
        a = mot.split('\t')
        freq = float(a[1])
        word = a[0]
        listemots[i] = (word, freq)

    dicoFr = { x[0]:x[1] for x in listemots }

    return dicoFr




def getBlacklistBeforeEleve():
    blacklist = [u'LE SCAN SPORT', u'EN IMAGES', u'LE SCAN POLITIQUE', u'LE SCAN TÉLÉ', u'LIRE AUSSI' ]
    blacklist.extend( [u'LE SCAN TÉLÉ', u'LE SCAN ÉCO', u'LE SCAN ECO' , u"Toute l'actualité", u"Le Point", u'INFO LE FIGARO'] )
    blacklist.extend( ['Le Monde', 'EN DIRECT', 'CARTE INTERACTIVE', 'FIGAROVOX TRIBUNE', u'VIDÉOS'] )
    blacklist.extend( ['MILLIONS DE DOLLARS', 'INTERVIEW', 'ENTRETIEN', u'VIDÉO', 'INFOGRAPHIE'] )
    blacklist.extend( ['FIGAROVOX', 'TRIBUNE', 'REPORTAGE'] )
    blacklist.extend( ['entre eux', 'Top 14', 'Zapping du Point'] )

    return blacklist

def getBlacklistAfterEleve():
    # en minuscule
    blacklist = ['etat', 'etats', 'euros', u'est-il', 'actu', u'a-t-il', 'ont-ils', 'a-t-on', 'va-t-il', u'elle-même']
    blacklist.extend( ['axa', u'après-midi', 'a-t-elle', 'faut-il', u'peut-être', 'the', 'sont-elles'] )
    blacklist.extend(['week-end', u'lui-même', u"qu'on", 'celle-ci', 'celui-ci', u'au-delà', 'est-elle', 'sont-ils'])
    blacklist.extend([u'Libé', u'œil', u'œuvre', 'zapping', 'editorial'])
    # stopwords
    #blacklist.extend(['les', 'des', u'est', u"été", 'pour', 'contre', u'pas', 'dans', 'qui', 'que', 'lui', 'ses', 'une'])
    #blacklist.extend(['avait', 'sur', 'voici', 'avec', 'comme', 'cela', 'aux', 'cette', 'par', 'selon', u'après', 'fait', 'faire'])
    #blacklist.extend(['nous', 'vous', 'ils', 'elle', 'elles', 'eux', 'ont', 'avez', 'avons','plus', 'ainsi', 'leur', u'être'])
    #blacklist.extend(['tout', 'tous', 'toutes', 'depuis', 'moins', 'plus', 'sont', 'vers', 'mme', u'ème'])
    #blacklist.extend(['son', u'très', 'était', 'veut', 'alors', 'avoir', 'lors', 'ces', 'entre'])

    blacklist.extend( getStopWords() )

    for mot in blacklist:
        mot = mot.lower()

    return blacklist


def getStopWords():
    filename = './data_dico/stop_words_fr.txt'
    with codecs.open(filename, encoding='utf-8') as f:
        listemots = f.readlines()

    stopwords = []
    for line in listemots:
        m = re.match(u'([^\s|]*)', line )
        if m and m.group():
            if m.group() not in stopwords:
                stopwords.append( m.group() )

    return stopwords


def printSorted(dico, n = 200 ):
    myDico_sorted = sorted(dico.items(), key = lambda x:x[1], reverse=True)

    sList = [ '%s (%i) ' % (m, c) for m, c in myDico_sorted[:n] ]

    print( ' '.join( sList ) )
