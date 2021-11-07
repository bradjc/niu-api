from niuApi.requests import do_request
from niuApi.exceptions import NIURequestError

def motor_data_battery_info(serial):

    json_response = do_request(
        'v3/motor_data/battery_info',
        add_params={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No battery information returned')

    return json_response

def service_intelligent_detection(serial):

    json_response = do_request(
        'v3/service/intelligent_detection',
        add_params={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('Intelligent detection failed')

    return json_response

def motor_data_cycling_statistics(serial):

    json_response = do_request(
        'v3/motor_data/cycling_statistics',
        add_params={'sn': serial}
    ).get('data')

    if len(json_response.keys()) == 0:
        raise NIURequestError('No cycling stats returned')

    return json_response
