import niuApi.apicommands as apicommands

def list(print: list = ['sn_id'], **kwargs) -> dict:
    """Get all scooters conntected with the desired accout

    Args:
        print (list, optional): Set the options to print. Defaults to ['sn_id'].

    Returns:
        dict: key: serial number, values: values in print option
    """

    scooters = apicommands.v5.scooter_list()

    out = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')

        out[sn] = []
        for info in print:
            if scooter.get(info):
                out[sn].append(scooter.get(info))

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

        if serial is not None:
            if sn != serial:
                continue

        total_mileage = apicommands.other.motoinfo_overallTally(sn)
        scooter['totalMileage'] = int(total_mileage.get('totalMileage'))
        details = apicommands.v5.scooter_detail(sn)
        for detail, value in details.items():
            if detail in possible_prints:
                scooter[detail] = value
        
        out[sn] = []

        for info in print:
            if scooter.get(info):
                out[sn].append(scooter.get(info))
    
    return out
