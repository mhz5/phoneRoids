import sample

def main(location, radius=50, category='restaurant'):
    print 'Arguments: ' + category + " | " + location
    return sample.query_api(category, location, radius)

#output = main('4790 Canberra Court, San Jose, CA', 8.0, 'restaurant')

