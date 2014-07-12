import re

apps = ['yelp', 'maps', 'venmo']
yelpArgsStageOne = ['distance:', 'location:', 'category:']
mapsArgs = []
venmoArgs = ['pay:', 'request:', 'to:', 'from:', 'for:']

def parseRequest(phrase, curState = 'None'):
    parseFuncs = {'yelp': parseYelp, 'maps': parseMaps, 'venmo': parseVenmo}
    newState = 'None'
    requestedApp = ''
    response = {}
    firstToken = getFirstToken(phrase)
    if firstToken in apps:
        requestedApp = firstToken
        response = parseFuncs[requestedApp](phrase)
        if firstToken == 'yelp':
            newState = 'yelp_1'
    else if curState != 'None':
        #currentApp, currentStage = curState.split('_', 1)
        requestedApp = 'yelp'
        if isInteger(phrase):
            response['choice'] = phrase
        else if phrase == 'More' or phrase == 'more':
            response['choice'] = 'more'
            newState = 'yelp_1'
        else:
            response['error'] = 'invalid request format'
            newState = 'yelp_1'
    else:
        response['error'] = 'invalid request format'
    
    return (requestedApp, response, newState)


def parseYelp(phrase):
    return parseArgsStage0(phrase, yelpArgsStageOne)


def parseMaps(phrase):
    return parseArgsStage0(phrase, mapsArgs)


def parseVenmo(phrase):
    return parseArgsStage0(phrase, venmoArgs)


def parseArgsStage0(phrase, keywords):
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
        else:
            locDict[key] = defaults[key]
    return locDict


def findOrderedKeyList(phrase):
    parts = phrase.split(':')
    return [term.split()[-1] for i, term in enumerate(parts) if i != (len(parts) - 1)]

    
def getFirstToken(phrase):
    return phrase.split(' ', 1)[0]


def isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#print parseRequest('venmo pay:$15.00 to:Mike Zhao for:being AWESOME')
#print parseRequest('yelp location:mountain view')

