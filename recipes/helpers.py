# Import recipe scraper https://pypi.org/project/recipe-scrapers/
from recipe_scrapers import scrape_me

# Import ingredient parser https://github.com/MichielMag/parse-ingredients
from parse_ingredients import parse_ingredient

import re

# scrapes recipe into a dictionary for uploading recipes to db 
def recipe_to_dict(site):

    try:
        recipe = scrape_me(site)
    except:
        try:
            recipe = scrape_me(site, wild_mode=True)
        except:
            return

    d = {}
    d['recipe_name'] = recipe.title()
    d['url'] = site

    try:
        d['total_time'] = recipe.total_time()
    except:
        pass

    try:
        d['yields'] = recipe.yields()
    except:
        pass
    
    d['instructions'] = recipe.instructions()

    try:
        d['image'] = recipe.image()
    except:
        pass

    try:
        d['host'] = recipe.host()
    except:
        pass

    # create list of ingredient dictionaries
    ingredient_list = []
    for ingredient in recipe.ingredients():
        i = parse_ingredient(ingredient)
        i_dict = {}
        name = i.name
        # clean ingredient name
        # remove non-alphabetic characters
        name = re.sub("[^a-zA-Z\s]+", "", name)
        # all lowercase
        name=name.lower()
        # remove whitespace 
        name = name.strip()
        i_dict['ingredient_name'] = name

        try:
            i_dict['quantity'] = i.quantity
        except:
            pass
        try:
            i_dict['unit'] = i.unit
        except:
            pass
        try:
            i_dict['comment'] = i.comment
        except:
            pass
        i_dict['original_string'] = i.original_string
        ingredient_list.append(i_dict)
    d["ingredients"] = ingredient_list
    return d

# for testing
#site = 'https://thewoksoflife.com/chinese-chicken-broccoli-brown-sauce/'
#result = recipe_to_dict(site)
#print(result)


# converts imperial units to metric (and standardizes metric to ml and g for easy addition) (approximation)
def metric_converter(quantity, unit):
    if unit == 'tsp':
        quantity *= 5
        u = 'ml'
    elif unit =='tbsp':
        quantity *= 15
        u = 'ml'
    elif unit == 'cup':
        quantity *= 240
        u = 'ml'
    elif unit == 'pint':
        quantity *= 473
        u = 'ml'
    elif unit == 'gal':
        quantity *= 3785.4
        u = 'ml'
    elif unit == 'fl':
        quantity *= 29.57
        u = 'ml'
    elif unit == 'l':
        quantity *= 1000
        unit = 'ml'
    elif unit == 'oz':
        quantity *= 28.35
        u = 'g'
    elif unit == 'lb':
        quantity *= 454
        u = 'g'
    elif unit =='mg':
        quantity *= .001
        u = 'g'
    elif unit == 'kg':
        quantity *= 1000
        u = 'g'
    # don't change other measurements
    else:
        u = unit
    return quantity, u

#print(metric_converter(.25, 'lb'))
