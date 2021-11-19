from niuApi.requests import do_request
from niuApi.exceptions import NIURequestError

def scooter_list():

    json_response = do_request('v5/scooter/list')

    if len(json_response.get('data').get('items')) == 0:
        raise NIURequestError('No scooter found')

    scooters = []
    for scooter in json_response.get('data').get('items'):
        scooters.append(scooter)
    
    return scooters

def scooter_detail(serial):

    json_response = do_request(
        f'v5/scooter/detail/{serial}',
        add_headers={
            'user-agent': 'manager/4.6.44 (nuiAPI);lang=en-US;clientIdentifier=Overseas'
        }
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No scooter details returned')
    
    return json_response

def scooter_motor_data_index_info(serial):

    json_response = do_request(
        'v5/scooter/motor_data/index_info',
        add_headers={
            'user-agent': 'manager/4.6.44 (nuiAPI);lang=en-US;clientIdentifier=Overseas'
        },
        add_params={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No motor_data returned')

    return json_response

def tire_gauge_realtime(serial):

    json_response = do_request(
        'v5/tire_gauge/realtime',
        add_params={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No tire data returned')

    return json_response

def tire_gauge_status(serial):

    json_response = do_request(
        'v5/tire_gauge/status',
        add_params={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No tire data returned')

    return json_response

def track_list_v2(serial, pagesize=10, index=0):

    json_response = do_request(
        'v5/track/list/v2',
        method='post',
        add_data={
            'index': str(index),
            'pagesize': pagesize,
            'sn': serial
        },
        add_headers={
            'user-agent': 'manager/4.6.44 (nuiAPI);lang=en-US;clientIdentifier=Overseas'
        }
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No track data returned')

    return json_response
