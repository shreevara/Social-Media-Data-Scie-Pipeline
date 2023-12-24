CLIENT_ID = 'VfPD7bTFYafYDCRwoDroaA'
SECRET_KEY = 'JkEYf1f0Cfa6_YMVotMVBU5bKWqVFA'

import requests
from log_config import setup_logging
logger = setup_logging()
try:
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type' : 'password',
        'username' : 'Embarrassed_Tap_9498',
        'password' : 'phoenix12345'
    }
    headers = {'User-Agent' : 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', 
                        auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']
    print(TOKEN)
    headers['Authorization'] = f'bearer {TOKEN}'
except Exception as e:
    logger.exception(f"Error while connecting to the reddit API: {e}")