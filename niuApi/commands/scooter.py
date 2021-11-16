import niuApi.apicommands as apicommands

def list(print: list = ['sn_id'], **kwargs) -> dict:
    """Get all scooters conntected with the desired accout

    print
        Limit output for keys:
            [sn_id, scooter_name]
        Default = [sn_id]

    CLI Examples:
        niu-api scooter.list
        niu-api scooter.list print=sn_id,scooter_name
        niu-api scooter.list print=scooter_name
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
    """Get scooter information

    serial
        Serial number of scooter to limit output.
    
    print
        Limit output for keys:
            [scooter_name, totalMileage, sn_id, scooter_type,
            scooter_version, soft_version, mileage, engine_num, battery]
        Default = [scooter_name, totalMileage]

    CLI Examples:
        niu-api scooter.info
        niu-api scooter.info print=sn_id,scooter_name
        niu-api scooter.info serial=S3R1ALOFSC00T3R print=engine_num
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
