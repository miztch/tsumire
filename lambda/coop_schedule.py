from datetime import datetime
import requests
import json

def format_time(timestamp_str):
    '''
    convert timestamp to pronounce.
    '''
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S%z')
    time_to_pronounce = datetime.strftime(timestamp, '%#m月%#d日%p%#I時')
    
    time_in_jp = time_to_pronounce.replace('AM', '午前').replace('PM', '午後')

    return time_in_jp

def is_json(json_str):
    '''
    judge if json_str is valid.
    '''
    result = False
    try:
        json.loads(json_str)
        result = True
    except json.JSONDecodeError as jde:
        logger.info('got invalid response json, retrying.')

    return result

def get(rotation_code):
    uri = 'https://spla3.yuu26.com/api/coop-grouping/{}'.format(rotation_code)
    headers = {'Content-Type': 'application/json'}

    schedule = ''
    while True:
        schedule = requests.get(uri, headers=headers)
        valid_json = is_json(schedule.text)

        if valid_json:
            break

    schedule = schedule.json()
    map_detail = schedule['results'][0]

    result = {
        'stage': map_detail['stage']['name'],
        'start_time': map_detail['start_time'],
        'end_time': map_detail['end_time'],
        'weapons': [ weapon['name'] for weapon in map_detail['weapons']],
        'big_run': map_detail['is_big_run']
    }

    return result