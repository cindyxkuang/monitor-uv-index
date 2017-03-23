import requests
import json

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
    request_url = EPA_BASE_URL + '/' + zipcode + '/json'
    response = requests.get(request_url)
    content = response.json()
    
    current = content[-1]['UV_VALUE']
    prev = content[-2]['UV_VALUE']

    return {'current': current, 'prev': prev}