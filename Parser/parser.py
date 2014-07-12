import re

apps = ["yelp", "maps", "venmo"]
yelpArgsStageOne = ["distance:", "location:", "category:"]
venmoArgs = ["pay:", "request", "to:", "from:", "for:"]

def parseRequest(phrase):
    parseFuncs = {"yelp": parseYelp, "maps": parseMaps, "venmo": parseVenmo}
    requestedApp = findApp(phrase)
    return (requestedApp, parseFuncs[requestedApp](phrase))


def parseYelp(phrase):
    return parseArgs(phrase, yelpArgsStageOne)


def parseMaps(phrase):
    print 'maps'


def parseVenmo(phrase):
    return parseArgs(phrase, venmoArgs)


def parseArgs(phrase, keywords):
    locDict = {}
    temp = phrase
    for key in keywords:
        if key in temp:
            temp = temp.replace(key,":")
            #locDict[key] = phraseLoc
    args = temp.split(":")
    pos = 1
    for key in keywords:
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

#print parseRequest("venmo pay:$15.00 to:Mike Zhao for:being AWESOME")
#print parseRequest("yelp distance:10 miles location:mountain view category:restaurants")
