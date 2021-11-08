"""Request functions
"""

import os
import requests
import json
import hashlib
import datetime

from niuApi.config import NIUConfig
from niuApi.exceptions import NIURequestError

TOKENFILE = os.environ.get('HOME') + '/.nui-token'
APIURL = 'https://app-api-fk.niu.com'
LOGINURL = 'https://account-fk.niu.com/v3/api/oauth2/token'
TIMESTAMP = int(datetime.datetime.now().timestamp())

def get_token():

    def __generate_token_file(login_data):
        """Write token file

        Args:
            login_data (dict): return json of login process
        """

        write_data = {
            'access_token': {
                'token': login_data.get('data').get('token').get('access_token'),
                'expires': login_data.get('data').get('token').get('token_expires_in'),
            },
            'refresh_token': {
                'token': login_data.get('data').get('token').get('refresh_token'),
                'expires': login_data.get('data').get('token').get('refresh_token_expires_in'),
            }
        }

        with open(TOKENFILE, 'w') as tokenfile:
            json.dump(write_data, tokenfile)


    def __login(email, password):
        """Perform login action to get the access token

        Args:
            email (str): login email
            password (str): login password

        Raises:
            NIURequestError: if response status greater than 0

        Returns:
            dict: json response after decoding
        """

        response = requests.post(
            LOGINURL,
            # multipart formdata
            files={
                'account': (None, email),
                'grant_type': (None, 'password'),
                'password': (None, hashlib.md5(password.encode('utf-8')).hexdigest()),
                'app_id': (None, 'niu_fksss2ws'),
                'scope': (None, 'base')
            },
        )
    
        json_response = json.loads(response.text)
        # raise error, if response code is higher than 0
        if json_response.get('status') > 0:
            raise NIURequestError(json_response.get('desc'))
            
        return json_response

    now = int(datetime.datetime.now().timestamp())
    if os.path.isfile(TOKENFILE):
        tokenfile = open(TOKENFILE)
        tokens = json.loads(tokenfile.read())
        tokenfile.close()

        # if tokens aren't expired
        if (now < tokens.get('access_token').get('expires') and
                now < tokens.get('refresh_token').get('expires')):
            
            return tokens.get('access_token').get('token')
    
    # if no tokenfile is present, ot tokens are expired
    config = NIUConfig()
    email = config['niuapi']['email']
    password = config['niuapi']['password']

    login_data = __login(email, password)
    __generate_token_file(login_data)
        
    tokenfile = open(TOKENFILE)
    tokens = json.loads(tokenfile.read())
    tokenfile.close()

    return tokens.get('access_token').get('token')

def do_request(slug, method='get', add_params={}, add_headers={}):
        """Perform get requests with token (after login)

        Args:
            slug (str): slug of the base api url

        Raises:
            NIURequestError: raise when request status code greater than 0

        Returns:
            dict: json response after decoding
        """

        response = getattr(requests, method)(
            f'{APIURL}/{slug}',
            params={
                '_': TIMESTAMP,
                **add_params
            },
            headers={
                'token': get_token(),
                'accept': 'application/json',
                'user-agent': 'manager/4.6.44 (nuiAPI);lang=en-US;clientIdentifier=Overseas',
                **add_headers
            }
        )

        if response.status_code == 200:
            json_response = json.loads(response.text)
            if json_response.get('status') > 0:
                raise NIURequestError(json_response.get('desc'))
        else:
            raise NIURequestError(f'{APIURL}/{slug}: {response.status_code}')

        return json_response