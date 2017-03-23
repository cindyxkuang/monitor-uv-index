import requests
import json
from datetime import datetime

MAPZEN_KEY = 'mapzen-zk4XwPv'
MAPZEN_BASE_URL = 'https://search.mapzen.com/v1/search'

EPA_BASE_URL = 'https://iaspub.epa.gov/enviro/efservice/getEnvirofactsUVHOURLY/ZIP'

def get_city(zipcode):
    response = requests.get(MAPZEN_BASE_URL, params={'api_key': MAPZEN_KEY, 'size': 1, 'text': zipcode})
    content = response.json()
    
    city = content['features'][0]['properties']['locality']
    state_abbrev = content['features'][0]['properties']['region_a']

    return {'city': city, 'state_abbrev': state_abbrev}

def get_index(zipcode):
    now = datetime.strftime(datetime.now(), '%b/%d/%Y %I %p').upper()

    request_url = EPA_BASE_URL + '/' + zipcode + '/json'
    response = requests.get(request_url)
    content = response.json()
    
    prev = content[-1]['UV_VALUE']
    for index in content:
        current = index['UV_VALUE']
        if index['DATE_TIME'] == now:
            break
        prev = current
    return {'current': current, 'prev': prev}