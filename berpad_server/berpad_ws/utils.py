import sys
import json
import datetime

class Utilities(object):

    us_states_dict = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
    }

    us_state2timezone = {
        'AK': 'US/Alaska',
        'AL': 'US/Central',
        'AR': 'US/Central',
        'AS': 'US/Samoa',
        'AZ': 'US/Mountain',
        'CA': 'US/Pacific',
        'CO': 'US/Mountain',
        'CT': 'US/Eastern',
        'DC': 'US/Eastern',
        'DE': 'US/Eastern',
        'FL': 'US/Eastern',
        'GA': 'US/Eastern',
        'GU': 'Pacific/Guam',
        'HI': 'US/Hawaii',
        'IA': 'US/Central',
        'ID': 'US/Mountain',
        'IL': 'US/Central',
        'IN': 'US/Eastern',
        'KS': 'US/Central',
        'KY': 'US/Eastern',
        'LA': 'US/Central',
        'MA': 'US/Eastern',
        'MD': 'US/Eastern',
        'ME': 'US/Eastern',
        'MI': 'US/Eastern',
        'MN': 'US/Central',
        'MO': 'US/Central',
        'MP': 'Pacific/Guam',
        'MS': 'US/Central',
        'MT': 'US/Mountain',
        'NC': 'US/Eastern',
        'ND': 'US/Central',
        'NE': 'US/Central',
        'NH': 'US/Eastern',
        'NJ': 'US/Eastern',
        'NM': 'US/Mountain',
        'NV': 'US/Pacific',
        'NY': 'US/Eastern',
        'OH': 'US/Eastern',
        'OK': 'US/Central',
        'OR': 'US/Pacific',
        'PA': 'US/Eastern',
        'PR': 'America/Puerto_Rico',
        'RI': 'US/Eastern',
        'SC': 'US/Eastern',
        'SD': 'US/Central',
        'TN': 'US/Central',
        'TX': 'US/Central',
        'UT': 'US/Mountain',
        'VA': 'US/Eastern',
        'VI': 'America/Virgin',
        'VT': 'US/Eastern',
        'WA': 'US/Pacific',
        'WI': 'US/Central',
        'WV': 'US/Eastern',
        'WY': 'US/Mountain',
        '' : 'US/Pacific',
        '--': 'US/Pacific' }

    ca_prov_terr = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NT': 'Northwest Territories',
    'NS': 'Nova Scotia',
    'NU': 'Nunavut',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan',
    'YT': 'Yukon'
    }

    ca_provinces = {
    'AB': 'Alberta',
    'BC': 'British Columbia',
    'MB': 'Manitoba',
    'NB': 'New Brunswick',
    'NL': 'Newfoundland and Labrador',
    'NS': 'Nova Scotia',
    'ON': 'Ontario',
    'PE': 'Prince Edward Island',
    'QC': 'Quebec',
    'SK': 'Saskatchewan'
    }

    ca_territories = {
    'NT': 'Northwest Territories',
    'NU': 'Nunavut',
    'YT': 'Yukon'
    }

    def __init__(self):
        pass

    def calculate_averages(self, data):
        mean = -1
        median = -1
        if len(data) == 0:
            return mean, median

        sorted_data = sorted(data, key=lambda rec:rec['val'])
        d_len = len(sorted_data)
        median = sorted_data[int(d_len/2)]['val']
        total = 0
        for d in data:
            total += d['val']
        mean = total / float(d_len)

        return mean, median

    def calculate_history_averages(self, data):
        mean = 0
        median = 0
        if len(data) == 0:
            return mean, median

        sorted_data = sorted(data, key=lambda rec:rec['val'])
        d_len = len(sorted_data)
        median = float(sorted_data[int(d_len/2)]['val'])
        total = 0
        for d in data:
            total += float(d['val'])
        mean = total / float(d_len)

        return mean, median

    def us_states(self):
        return self.us_states_dict

    def last_day_of_month(any_day):
        next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
        return next_month - datetime.timedelta(days=next_month.day)
