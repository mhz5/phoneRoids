import re

apps = ["yelp", "maps", "venmo"]
yelpArgsStageOne = ["distance:", "location:", "category:"]

def parseRequest(phrase):
    parseFuncs = {"yelp": parseYelp, "maps": parseMaps, "venmo": parseVenmo}
    requestedApp = findApp(phrase)
    return (requestedApp, parseFuncs[requestedApp](phrase))


def parseYelp(phrase):
    return parseYelpStateOne(phrase)


def parseMaps(phrase):
    print 'maps'


def parseVenmo(phrase):
    m = re.search('venmo (pay $[0-9][0-9]?[0-9]?.[0-9][0-9] to \w+ \w+ for .*|request $[0-9][0-9]?[0-9]?.[0-9][0-9] from \w+ \w+ for .*)', phrase)
    if m:
        return {'request type': m.group(0), 'entity': person, 'amount': m.group(1)}
    else:
        return 'parsing error. please try again'


def parseYelpStateOne(phrase):
    locDict = {}
    temp = phrase
    for key in yelpArgsStageOne:
        if key in temp:
            temp = temp.replace(key,":")
            #locDict[key] = phraseLoc
    args = temp.split(":")
    pos = 0
    for key in yelpArgsStageOne:
        if key in phrase:
            locDict[key[:-1]] = args[pos].strip()
            pos += 1
    return locDict
    
    
def getColonLoc(phrase):
    locs = {}
    while ":" in phrase:
        loc = phrase.index(":")
        locs.append(loc)
        phrase = phrase[(loc+1):]
        #print phrase
    return locs
    

def findApp(phrase):
    app = phrase.split(' ', 1)[0]
    if app in apps:
        return app
    return null

#print parseRequest("venmo pay $15.00 to Michael Zhao for being AWESOME")
