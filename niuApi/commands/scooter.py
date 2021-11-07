from niuApi.requests import get_request
from niuApi.exceptions import NIURequestError

def list(show_all: bool = False, **kwargs):
        """Get all scooters conntected with the desired accout

        Raises:
            NIURequestError: Raises if response status is greater than 0
            NIURequestError: Raises when no scooter is found

        Returns:
            list: a list with serial numbers of all scooters
        """

        json_response = get_request('scooter/list')

        if len(json_response.get('data').get('items')) == 0:
            raise NIURequestError('No scooter found')

        scooters = []
        for scooter in json_response.get('data').get('items'):
            if show_all:
                scooters.append(scooter)
            else:
                scooters.append(scooter.get('sn_id'))
        
        return scooters

def details(sn=None):

    scooters = []
    if sn is None:
        scooters = list()
    else:
        scooters.append(sn)

    datasets = {}
    for serial in scooters:
        datasets[serial] = get_request(f'scooter/detail/{serial}')
    
    if len(datasets.keys()) == 0:
        raise NIURequestError('No scooter details returned')
    
    return datasets
