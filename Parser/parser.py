import re

apps = ['yelp', 'maps', 'venmo']
yelpArgsStageOne = ['distance:', 'location:', 'category:']
mapsArgs = []
venmoArgs = ['pay:', 'request:', 'to:', 'from:', 'for:']

def parseRequest(phrase):
    parseFuncs = {'yelp': parseYelp, 'maps': parseMaps, 'venmo': parseVenmo}
    requestedApp = findApp(phrase)
    return (requestedApp, parseFuncs[requestedApp](phrase))


def parseYelp(phrase):
    return parseArgs(phrase, yelpArgsStageOne)


def parseMaps(phrase):
    return parseArgs(phrase, mapsArgs)


def parseVenmo(phrase):
    return parseArgs(phrase, venmoArgs)


def parseArgs(phrase, keywords):
    locDict = {}
    keyList = findOrderedKeyList(phrase)
    temp = phrase
    for key in keywords:
        if key in temp:
            temp = temp.replace(key,':')
    args = temp.split(':')
    pos = 1
    for key in keyList:
        if key in phrase:
            locDict[key] = args[pos].strip()
            pos += 1
    return locDict


def findOrderedKeyList(phrase):
    parts = phrase.split(':')
    return [term.split()[-1] for i, term in enumerate(parts) if i != (len(parts) - 1)]

    
def getColonLoc(phrase):
    locs = {}
    while ':' in phrase:
        loc = phrase.index(':')
        locs.append(loc)
        phrase = phrase[(loc+1):]
    return locs
    

def findApp(phrase):
    app = phrase.split(' ', 1)[0]
    if app in apps:
        return app

#print parseRequest('venmo pay:$15.00 to:Mike Zhao for:being AWESOME')
#print parseRequest('yelp distance:10 miles location:mountain view category:restaurants')
