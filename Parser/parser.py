import re;

apps = ["yelp", "maps"]
yelpArgsStageOne = ["distance:", "location:", "category:"]

def parseYelp(phrase):
    return
    
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
            locDict[key] = args[pos]
            pos+=1
    print locDict
    
    
def getColonLoc(phrase):
    locs = {}
    while ":" in phrase:
        loc = phrase.index(":")
        locs.append(loc)
        phrase =  phrase[(loc+1):]
        print phrase
    return locs
    

def findApp(phrase):
    app = phrase.split(' ', 1)[0]
    if app in apps:
        print app

parseYelpStateOne("location: Mountain View distance: 10 category: restaurants")
