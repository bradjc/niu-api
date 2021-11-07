from niuApi.requests import get_request
from niuApi.exceptions import NIURequestError

def list(show_all: bool = False, **kwargs) -> list:
        """Get all scooters conntected with the desired accout

        Args:
            show_all (bool, optional): Set true if all details should be returned.
                                       Otherwise, the serial number is returned

        Raises:
            NIURequestError: Raises when no scooter is found

        Returns:
            list: serial numbers of all scooters (if show_all is false)
                  detailed response, including the serial number(s) (if show_all is true)
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

def details(sn: str = None, **kwargs) -> dict:
    """Get scooter details

    Args:
        sn (str, optional): Serial Number of scooter. Defaults to None.

    Raises:
        NIURequestError: Raise error, when no scooter details returned

    Returns:
        dict: key: scooter serial, value: details
    """

    scooters = []
    if sn is None:
        scooters = list()
    else:
        scooters.append(sn)

    datasets = {}
    for serial in scooters:
        datasets[serial] = get_request(f'scooter/detail/{serial}').get('data')
    
    if len(datasets.keys()) == 0:
        raise NIURequestError('No scooter details returned')
    
    return datasets
