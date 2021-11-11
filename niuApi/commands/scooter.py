import niuApi.apicommands as apicommands

def list(print: list = ['sn_id'], **kwargs) -> dict:
    """Get all scooters conntected with the desired accout

    Args:
        print (list, optional): Set the options to print. Defaults to ['sn_id'].

    Returns:
        dict: key: serial number, values: values in print option
    """

    possible_prints = ['sn_id', 'scooter_name']

    scooters = apicommands.v5.scooter_list()

    out = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        out[sn] = {}

        for arg in print:
            try:
                if arg in possible_prints: out[sn][arg] = scooter[arg]
            except KeyError:
                pass
                
    return out

def info(serial: str = None, print: list = ['scooter_name', 'totalMileage'], **kwargs) -> dict:
    """Return info of scooter

    Args:
        serial (str, optional): Serial number of given scooter. Defaults to None.
        print (list, optional): Print following options. Defaults to ['scooter_name', 'totalMileage'].

    Returns:
        dict: key: serial number, values: values in print option
    """

    possible_prints = [
        'scooter_name', 'totalMileage', 'sn_id',
        'scooter_type', 'scooter_version', 'soft_version',
        'mileage', 'engine_num', 'battery'
    ]

    scooters = apicommands.v5.scooter_list()

    out = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        out[sn] = {}

        if serial is not None:
            if sn != serial:
                continue

        total_mileage = apicommands.other.motoinfo_overallTally(sn)
        details = apicommands.v5.scooter_detail(sn)
        details['totalMileage'] = int(total_mileage.get('totalMileage'))    
        for arg in print:
            try:
                if arg in possible_prints: out[sn][arg] = details[arg]
            except KeyError:
                pass
    
    return out
