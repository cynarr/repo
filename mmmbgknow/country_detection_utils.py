import tldextract
import pandas as pd
from textblob import TextBlob
import pycountry


tld_df = pd.read_csv("data/country-codes-tlds.csv")

language_to_country_dict = { # Replace with some ready-made list
    'Finnish': 'Finland',
    'Swedish': 'Sweden'
}

def get_country_from_url(url: str):
    url_parts = tldextract.extract(url)
    suffix = "." + url_parts.suffix

    locations = tld_df[tld_df['tld'] == suffix]['country'].tolist()

    if len(locations) == 1: # TLD is not always unique
        return locations[0]
    elif len(locations) > 1: # TODO: something smart
        return locations[0]
    
    # TODO: use some online source for determining the country of origin

    return "none"

def get_language_from_text(text: str):
    language_code = TextBlob(text).detect_language()
    language_info = pycountry.languages.get(alpha_2=language_code)
    return language_info.name

def get_country_from_language(language: str):
    if language in language_to_country_dict:
        return language_to_country_dict[language]

    return "none"

if __name__ == "__main__":
    print(get_country_from_url('https://www.cwi.fi:80/%7Eguido/Python.html'))
    print(get_country_from_language(get_language_from_text("Tämä on kirjoitettu suomeksi.")))
    print(get_country_from_language(get_language_from_text("And this is in English.")))