import pycountry
from pycountry_convert.convert_country_alpha2_to_continent_code import country_alpha2_to_continent_code


europe = []


for c in pycountry.countries:
    try:
        continent = country_alpha2_to_continent_code(c.alpha_2)
    except KeyError:
        continue
    if continent != "EU":
        continue
    europe.append(c.alpha_2)


# Not sure why Vatican City is left out
europe.append("VA")
# Let's put in Cyrpus too
europe.append("CY")


print("cc2")
for cc2 in sorted(europe):
    print(cc2)
