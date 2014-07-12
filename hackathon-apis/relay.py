import sample

def main(location, radius, category='restaurant'):
    print category + " | " + location
    sample.query_api(category, location, radius)


main('4790 Canberra Court, San Jose, CA', 8.0, 'comedy')