"""Request functions
"""

import os
import requests
import json
import hashlib
import datetime

from niuApi.exceptions import NIURequestError

class NIURequests():

    APIURL = 'https://app-api-fk.niu.com/v5/'
    LOGINURL = 'https://account-fk.niu.com/v3/api/oauth2/token'
    TOKENFILE = os.environ.get('HOME') + '/.nui-token'

    def __init__(self, config) -> None:
        
        self.token = self.__get_token(config)

    def __get_token(self, config):
        
        email = config['niuapi']['email']
        password = config['niuapi']['password']

        # generate token file if not exists
        if not os.path.isfile(self.TOKENFILE):
            login_data = self.__login(email, password)
            self.__generate_token_file(login_data)

        tokenfile = open(self.TOKENFILE)
        tokens = json.loads(tokenfile.read())
        tokenfile.close()

        # generate new token, if expired
        now = datetime.datetime.now().timestamp()
        if (now > tokens.get('access_token').get('expires') or
                now > tokens.get('refresh_token').get('expires')):
            login_data = self.__login(email, password)
            self.__generate_token_file(login_data)
        
            tokenfile = open(self.TOKENFILE)
            tokens = json.loads(tokenfile.read())
            tokenfile.close()
        
        return tokens.get('access_token').get('token')

    def __generate_token_file(self, login_data):

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

        with open(self.TOKENFILE, 'w') as tokenfile:
            json.dump(write_data, tokenfile)
   
        return 
            
    def __login(self, email, password):

        response = requests.post(
            self.LOGINURL,
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