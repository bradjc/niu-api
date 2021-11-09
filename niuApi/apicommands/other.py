"""Niu API commands: other
"""

from niuApi.requests import do_request
from niuApi.exceptions import NIURequestError

def motoinfo_overallTally(serial):

    json_response = do_request(
        'motoinfo/overallTally',
        method='post',
        add_data={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No information returned')
    
    return json_response
