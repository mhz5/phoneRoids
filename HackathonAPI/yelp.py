import sample

def query(location, radius, category='restaurant'):
    print 'Arguments: ' + category + " | " + location
    return sample.query_api(category, location, radius, False, 1)

#output = main('4790 Canberra Court, San Jose, CA', 8.0, 'restaurant')

def verbose(location, radius, index, category='restaurant'):
    return sample.query_api(category, location, radius, True, index)

#verboseOutput = verbose('4790 Canberra Court, San Jose, CA', 8.0, 2, 'restaurant')
