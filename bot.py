import requests
import json
from twython import Twython

with open('creds-twitter.json') as f:
    creds = json.loads(f)

client = Twython(creds['consumer_key'], creds['consumer_secret'], 
                    creds['access_token'], creds['access_token_secret'])

