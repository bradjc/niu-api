import niuApi.apicommands as apicommands

def list(serial: str = None, print: list = ['bmsId'], **kwargs) -> dict:
    """Lists Batteries connected to the scooter

    serial
        Serial number of scooter to limit output.
    
    print
        Limit output for keys:
            [bmsId]
        Default = [bmsId]

    CLI Examples:
        niu-api battery.list
        niu-api battery.list serial=S3R1ALOFSC00T3R
        niu-api battery.list print=bmsId
    """

    possible_prints = ['bmsId']

    scooters = apicommands.v5.scooter_list()

    out = {}
    battery_info = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        
        if serial is not None:
            if sn != serial:
                continue
        
        batteries = apicommands.v3.motor_data_battery_info(sn).get('batteries')
        i = 1
        for values in batteries.values():

            bmsid = values.get('bmsId')
            if not bmsid:
                battery_info[i] = {}
                battery_info[i]['info'] = f'Battery {i}: not connected'
                i += 1
                continue
            
            battery_info[bmsid] = {}

            for arg in print:
                try:
                    if arg in possible_prints: battery_info[bmsid][arg] = values[arg]
                except KeyError:
                    pass
            
    out[sn] = battery_info

    return out

def info(serial: str = None, bmsid: str = None, print: list = ['bmsId', 'batteryCharging'], **kwargs) -> dict:
    """Get info of the batteries conntected to the scooter

    serial
        Serial number of scooter to limit output.

    bmsid
        Battery ID to limit output.

    print
        Limit output for keys: 
            [bmsId, batteryCharging, chargedTimes, energyConsumedToday,  
            gradeBattery, isConnected, temperature, temperatureDesc]
        Default = [bmsId, batteryCharging]

    CLI Examples:
        niu-api battery.info serial=S3R1ALOFSC00T3R bmsid=BATT3RY1D
        niu-api battery.info bmsid=BATT3RY1D print=bmsId,batteryCharging
        niu-api battery.info serial=S3R1ALOFSC00T3R print=bmsId,batteryCharging,gradeBattery
    """

    possible_prints = [
        'bmsId', 'batteryCharging', 'chargedTimes',
        'energyConsumedToday', 'gradeBattery', 'isConnected',
        'temperature', 'temperatureDesc'
    ]

    scooters = apicommands.v5.scooter_list()

    out = {}
    battery_info = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        
        if serial is not None:
            if sn != serial:
                continue
        
        batteries = apicommands.v3.motor_data_battery_info(sn).get('batteries')
        i = 1
        for values in batteries.values():

            id = values.get('bmsId')
            if not id:
                battery_info[i] = {}
                battery_info[i]['info'] = f'Battery {i}: not connected'
                i += 1
                continue
            
            if bmsid is not None and bmsid != id: continue

            battery_info[id] = {}

            for arg in print:
                try:
                    if arg in possible_prints: battery_info[id][arg] = values[arg]
                except KeyError:
                    pass
            
    out[sn] = battery_info

    return out

def ecu(serial: str = None, print: list = ['centreCtrlBattery']) -> dict:
    """Get info of ecu battery

    serial
        Serial number of scooter to limit output.

    print
        Limit output for keys:
            [centreCtrlBattery]
        Default = [centreCtrlBattery]

    CLI Examples:
        niu-api battery.ecu serial=S3R1ALOFSC00T3R
        niu-api battery.ecu print=centreCtrlBattery
        niu-api battery.ecu
    """

    possible_prints = ['centreCtrlBattery']

    scooters = apicommands.v5.scooter_list()

    out = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        out[sn] = {}

        if serial is not None:
            if sn != serial:
                continue

        info = apicommands.v5.scooter_motor_data_index_info(sn)

        for arg in print:
            try:
                if arg in possible_prints: out[sn][arg] = info[arg]
            except KeyError:
                pass

    return out
