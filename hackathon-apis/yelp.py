import sample

def main(location, radius, category='restaurant'):
    print category + " | " + location
    return sample.query_api(category, location, radius)

output = main('4790 Canberra Court, San Jose, CA', 8.0, 'restaurant')

print output 