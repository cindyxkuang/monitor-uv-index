import requests
import json
import client
from sys import argv
from twython import Twython
from datetime import datetime
import time

with open('creds-twitter.json') as f:
    creds = json.load(f)

def periodic(scheduler, interval, action, actionargs=()):
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))

def make_story(zipcode, username):
    now = datetime.strftime(datetime.now(), '%-I:%M:%S %p, %a %b %-d, %Y')
    location_result = client.get_city(zipcode)
    username = username
    try:
        index_result = client.get_index(zipcode)
        parsed_result = parse_index(int(index_result['current']), int(index_result['prev']))
        twit_client = Twython(creds['consumer_key'], creds['consumer_secret'], creds['access_token'], creds['access_token_secret'])
        twit_client.update_status(status='''@{} It is {}. The UV index in {}, {} is now {}. This is a {}% {} from the most recent previous update.'''
                                            .format(username, now, location_result['city'], location_result['state_abbrev'], index_result['current'], parsed_result['percentage'], parsed_result['up_down']))  
        time.sleep(3600)
    except:
        pass

def parse_index(current, prev):
    if prev > 0:
        percentage = round((current - prev) / prev * 100, 1)
    else:
        percentage = round(current / 100, 1)

    if percentage >= 0:
        up_down = 'increase'
    else:
        up_down = 'decrease'

    return {'percentage': abs(percentage), 'up_down': up_down}

if __name__ == '__main__':
    if len(argv) < 3:
        print("Need to pass in a 'ZIP CODE' 'USERNAME' as an arguments.")
    else:
        zipcode = argv[1]
        username = argv[2]
        while True:
            make_story(zipcode, username)