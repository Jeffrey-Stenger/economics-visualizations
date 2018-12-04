import csv

import pygal
from pygal.maps.world import World
from pygal.style import RotateStyle as RS, LightColorizedStyle as LCS

from country_codes import get_country_code

filename = 'debt_gdp.csv'

# Load the data.
while True:
    with open(filename) as f:
        debt_data = csv.reader(f)
        header_row = next(debt_data)
    
# Request a year from the user to visualize the data for.

        user_prompt = "Please enter desired year for debt-gdp ratio. "
        user_prompt+= "\nEnter 'q' to quit the program: "
        user_year = input(user_prompt)
        if user_year == 'q':
            break

        requested_year = header_row.index(user_year)
        
# Make a dictionary of the requested year's debt data.
        debt_to_gdps = {}
        missing_countries = []
        for debt_dict in debt_data:
            country_name = debt_dict[0]
            try:
                debt = int(float(debt_dict[requested_year]))
                code = get_country_code(country_name)
                if code:
                    debt_to_gdps[code] = debt
            except ValueError:
                missing_countries.append(country_name)
                print(country_name, "data not available")
    
# Divide the Debt/GDPs into 3 different tiers.
        tier_1, tier_2, tier_3 = {}, {}, {}
        for cc, debt in debt_to_gdps.items():
            if debt < 35:
                tier_1[cc] = debt
            elif debt < 70:
                tier_2[cc] = debt
            else:
                tier_3[cc] = debt
# Print off message informing of countries with no data found for that year.
        print("\nData for {} countries not available for {}.".format(
            len(missing_countries), user_year))
        print("Check the new svg file in same folder as this file" + 
            " to view Debt/GDP map.\n")
        
# Visualize the data.
    wm_style = RS('#ff6633')
    wm = pygal.maps.world.World(style=wm_style)
    wm.title = "Central Govt Debt as a Percentage of GDP for %s" % user_year

    wm.add('Debt/GDP >= 70%', tier_3)
    wm.add('Debt/GDP < 70%', tier_2)
    wm.add('Debt/GDP < 35%', tier_1)

    wm.render_to_file('central_debt_to_gdp.svg')


