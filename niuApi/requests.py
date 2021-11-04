"""Request functions
"""

import os
import requests
import json
import hashlib
import datetime

from requests.models import Response

from niuApi.exceptions import NIURequestError

class NIURequests():

    APIURL = 'https://app-api-fk.niu.com/v5'
    LOGINURL = 'https://account-fk.niu.com/v3/api/oauth2/token'
    TOKENFILE = os.environ.get('HOME') + '/.nui-token'
    TIMESTAMP = int(datetime.datetime.now().timestamp())

    def __init__(self, config) -> None:
        """Initialize NIURequests

        Args:
            config (dict): config object of the yaml file
        """
        
        self.token = self.__get_token(config)
        self.scooters = self.get_scooters()

    def __get_token(self, config):
        """Return the access_token for further requests

        Args:
            config (dict): config object of the yaml file

        Returns:
            str: valid access_key
        """
        
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
        now = int(datetime.datetime.now().timestamp())
        if (now > tokens.get('access_token').get('expires') or
                now > tokens.get('refresh_token').get('expires')):
            login_data = self.__login(email, password)
            self.__generate_token_file(login_data)
        
            tokenfile = open(self.TOKENFILE)
            tokens = json.loads(tokenfile.read())
            tokenfile.close()
        
        return tokens.get('access_token').get('token')

    def __generate_token_file(self, login_data):
        """Generate token file as json

        Args:
            login_data (dict): login data from json response after login
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

        with open(self.TOKENFILE, 'w') as tokenfile:
            json.dump(write_data, tokenfile)
   
        return 
            
    def __login(self, email, password):
        """Login into NUI API and get the login details, e.g. tokens

        Args:
            email (str): get the email for login
            password (str): get the password of the account

        Raises:
            NIURequestError: Raise errir, if login fails. The status must be greater 0 to raise the error.

        Returns:
            dict: JSON response of successfull login process
        """

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

    def __get_request(self, slug):
        """Perform get requests with token (after login)

        Args:
            slug (str): slug of the base api url

        Raises:
            NIURequestError: raise when request status code greater than 0

        Returns:
            dict: response as dict
        """

        response = requests.get(
            f'{self.APIURL}/{slug}',
            params={'_': self.TIMESTAMP},
            headers={
                'token': self.token,
                'accept': 'application/json',
                'user-agent': 'manager/4.6.44 (nuiAPI);lang=en-US;clientIdentifier=Overseas'
            }
        )

        if response.status_code == 200:
            json_response = json.loads(response.text)
            if json_response.get('status') > 0:
                raise NIURequestError(json_response.get('desc'))
        else:
            raise NIURequestError(f'{self.APIURL}/{slug}: {response.status_code}')

        return json_response

    def get_scooters(self):
        """Get all scooters conntected with the desired accout

        Raises:
            NIURequestError: Raises if response status is greater than 0
            NIURequestError: Raises when no scooter is found

        Returns:
            list: a list with serial numbers of all scooters
        """

        response = requests.get(
            f'{self.APIURL}/scooter/list',
            params={'_': self.TIMESTAMP},
            headers={'token': self.token}
        )

        json_response = json.loads(response.text)
        if json_response.get('status') > 0:
            raise NIURequestError(json_response.get('desc'))

        if len(json_response.get('data').get('items')) == 0:
            raise NIURequestError('No scooter found')
        
        scooters = []
        for scooter in json_response.get('data').get('items'):
            scooters.append(scooter.get('sn_id'))
        
        return scooters

    def get_scooter_detail(self, serial=None):
        """Return scooter details as list

        Args:
            serial (str): serial number of scooter

        Raises:
            NIURequestError: when specified serial is not present
            NIURequestError: raise if no scooter details returned

        Returns:
            dict: serial as key and response data as value
        """

        scooters = []
        if serial is not None:
            if serial in self.scooters:
                scooters.append(serial)
            else:
                raise NIURequestError(f'Serial "{serial}" is not present')
        else:
            scooters = self.scooters

        datasets = {}
        for serial in scooters:
            datasets[serial] = self.__get_request(f'scooter/detail/{serial}')
        
        if len(datasets.keys()) == 0:
            raise NIURequestError('No scooter details returned')

        return datasets
