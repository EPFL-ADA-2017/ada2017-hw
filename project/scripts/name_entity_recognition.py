'''
Title: Name Entity Recognition with Spacy

This notebook is used to perform **NER** on Tweets. The main goal is to infer which *country* a certain Tweet is referring to.

Methodology: We opted for Spacy because it had built-in models trained with [OntoNotes5](https://catalog.ldc.upenn.edu/ldc2013t19), which gave a [wide range of labels](https://spacy.io/usage/linguistic-features#entity-types) for entity recognition. The ones that matter the most to us are:

* **GPE**
* **NORP**
* **MONEY**

Since we decided to enrich our data with relationships between countries, cities, nationalities, religions, religious affiliations and currencies we can make full use of the above labels and more accurately find Tweets that talk about a specific country.
'''

# Refer to 'https://spacy.io/usage/linguistic-features' for more info
import spacy
import re
import math
import pandas as pd

# Load English language for Spacy analysis
nlp = spacy.load('en')

# Compile alpha regex expression
alpha_regex = re.compile('[^a-zA-Z]')

# Paths for the matching countries, nationalities, religions and currencies
parsed_country_nationality_file = 'data/parsed/parsed_country_nationality.csv'
parsed_currency_country_file = 'data/parsed/parsed_currency_country.csv'
parsed_country_religion_file = 'data/parsed/country_religion_files/parsed_country_religion.csv'
parsed_country_cities_file = 'data/parsed/parsed_country_cities_grouped.csv'

# Load the necessary datasets
country_nationality_df = None
currency_country_df = None
country_religion_df = None
country_cities_df = None

def load_data(data_directory_prefix='.'):
    
    # Set the scope to global for the following variables
    global country_nationality_df
    global currency_country_df
    global country_religion_df
    global country_cities_df
    
    # Update the file path
    new_parsed_country_nationality_file = '{}/{}'.format(data_directory_prefix, parsed_country_nationality_file)
    new_parsed_currency_country_file = '{}/{}'.format(data_directory_prefix, parsed_currency_country_file)
    new_parsed_country_religion_file = '{}/{}'.format(data_directory_prefix, parsed_country_religion_file)
    new_parsed_country_cities_file = '{}/{}'.format(data_directory_prefix, parsed_country_cities_file)
    
    # Load the necessary datasets
    country_nationality_df = pd.read_csv(new_parsed_country_nationality_file, encoding='utf-8', compression='gzip',index_col=False)
    currency_country_df = pd.read_csv(new_parsed_currency_country_file, encoding='utf-8', compression='gzip', index_col=False)
    country_religion_df = pd.read_csv(new_parsed_country_religion_file, encoding='utf-8', compression='gzip', index_col=False)
    country_cities_df = pd.read_csv(new_parsed_country_cities_file, encoding='utf-8', compression='gzip', index_col=False)

    # Fix currency and city columns
    currency_country_df['Countries'] = currency_country_df['Countries'].apply(lambda x: x.strip('[]').replace('\'', '').replace(' ', '').split(',')).astype(list)
    country_cities_df['Countries'] = country_cities_df['Countries'].apply(lambda x: x.strip('[]').replace('\'', '').replace(' ', '').split(',')).astype(list)

def get_result_country_probability_dict(result_row, result_label):
    '''
    Auxiliary method for `get_likely_results`. For
    a given row it outputs a dictionary containing
    the estimated probability for referencing a 
    country.
    '''
    country_probability_dict = {}
    
    # Interpret country results
    if result_label == 'Country':
        country_code = result_row['ID']
        country_probability_dict[country_code] = 1.0
        
    # Interpret city results
    elif result_label == 'City':
        for country_code in result_row['Countries']:
            country_probability_dict[country_code] = 1 / len(result_row['Countries'])
    
    # Interpret nationality results
    elif result_label == 'Nationality':
        country_code = result_row['ID']
        country_probability_dict[country_code] = 1.0
        
    # Interpret religion results
    elif result_label == 'Religion':
        for country_code, country_prob in result_row.drop(['Religion', 'Affiliation']).iteritems():
            if country_prob is not float('NaN'):
                country_probability_dict[country_code] = float(country_prob)
    
    # Interpret currency results
    elif result_label == 'Currency':
        for country_code in result_row['Countries']:
            country_probability_dict[country_code] = 1 / len(result_row['Countries'])
    
    return country_probability_dict

def get_matching_row(text, df, col_labels):
    '''
    Tries to find matches between the provided
    text and the content of a certain dataframes'
    columns. It then returns the first row of the
    results as a safety measure (since there should
    only be one match for any given instance).
    '''
    upper_text = alpha_regex.sub('', text).upper()
    for col_label in col_labels:
        upper_series = df[col_label].astype(str).apply(lambda x: x.upper())
        matching_df = df[upper_series.str.contains(upper_text)]
        if (len(matching_df) > 0):
            return matching_df.iloc[0]
    return None

def get_matching_results(label, text):
    '''
    From a provided identity's label and text,
    this method returns a tuple (x, y) with
    x being the entity text and y the specific
    label (Country, City, etc) associated to such text.
    '''
    
    # Check if it is a country/city
    if label == 'GPE':
        # Country check
        result = get_matching_row(text, country_nationality_df, ['ID', 'Official Name', 'Common Name'])
        if result is not None:
            return (result, 'Country')
        
        # City check
        result = get_matching_row(text, country_cities_df, ['City'])
        if result is not None:
            return (result, 'City')
    
    # Check if it is a nationality/religion
    elif label == 'NORP':
        # Nationality check
        result = get_matching_row(text, country_nationality_df, ['Nationality'])
        if result is not None:
            return (result, 'Nationality')
        
        # Religion check
        result = get_matching_row(text, country_religion_df, ['Religion', 'Affiliation'])
        if result is not None:
            return (result, 'Religion')
    
    # Check if it is a known currency
    elif label == 'MONEY':
        result = get_matching_row(text, currency_country_df, ['ID'])
        if result is not None:
            return (result, 'Currency')
        
    return (None, None)
    

def get_likely_results(label, text):
    '''
    From a provided identity's label and text,
    this method returns a dictionary representing
    the possible countries it might be referencing.
    Its keys are the country codes and its values
    their corresponding probabilities.
    '''
    
    result, specific_label = get_matching_results(label, text)
    
    if (result is not None) and (specific_label is not None):
        return get_result_country_probability_dict(result, specific_label)
    
    return None

def get_interesting_text_entities(text):
    '''
    Creates a list of tuples, each containing 
    an identified entity's label and its text.
    '''
    # TODO create as many texts as necessary, with differently formatted
    # text, in order to more accurately find countries.
    target_entities = ['GPE', 'NORP', 'MONEY']
    document = nlp(text)
    return [(entity.label_, entity.text) for entity in document.ents if (entity.label_ in target_entities)]

def merge_probability_dicts(dict_l, dict_r):
    '''
    Creates a new dictionary containing all
    keys from both dictionaries. In case a
    key exists in both dictionaries, its
    value becomes the sum of both previously
    existing values.
    '''
    for country, probability in dict_r.items():
        dict_l[country] = dict_l.get(country, 0) + probability
    return dict_l

def normalize_probability_dict(probability_dict):
    '''
    This method normalizes all the probabilities
    in the provided dictionary (to values between
    0.0 and 1.0).
    '''
    value_list = list(probability_dict.values())
    sum_value = sum(value_list)
    
    normalized_dict = {}
    for country, probability in probability_dict.items():
        normalized_dict[country] = probability_dict[country] / sum_value
    return normalized_dict
        
def get_countries_from_content(text):
    '''
    This method analyses the input text and
    extracts the countries referenced in it.
    The ouput is in the form of a dictionary
    with the country codes as keys and their
    respective probability as values.
    '''
    interesting_entities = get_interesting_text_entities(text)
    country_probability_dict = {}
    for ent_label, ent_text in interesting_entities:
        results = get_likely_results(ent_label, ent_text)
        if results is not None:
            country_probability_dict = merge_probability_dicts(country_probability_dict, results)
    
    return normalize_probability_dict(country_probability_dict)

def get_most_likely_countries(country_probability_dict):
    '''
    Returns a list of the countries with 
    the highest probabilty in a dictionary.
    '''
    max_prob = max(list(country_probability_dict.values()))
    return [country for country, probability in country_probability_dict.items() if math.isclose(probability, max_prob)]

def is_tweet_about_country(tweet_text, country_code):
    '''
    Returns whether or not a Tweet is talking
    about a specific country.
    '''
    # TODO solve multi-worded countries and nationalities (by searching on every word separately in text.split())
    country_probability_dict = get_countries_from_content(tweet_text)
    most_likely_references = get_most_likely_countries(country_probability_dict)
    if country_code in most_likely_references:
        return True
    return False