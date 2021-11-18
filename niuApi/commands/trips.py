from datetime import date

import niuApi.apicommands as apicommands

today = date.today()

def summary_date(
    serial: str = None,
    print: list = ['everdayMileage'],
    date: list = [today.strftime("%Y%m%d")],
) -> dict:
    """Get trip summary by date (max. 29 days)

    serial
        Serial number of scooter to limit output.
    
    print
        Limit output for keys:
            [AvgSpeed, date, everdayMileage,
            maxSpeed, 'ridingTime]
        Default = [everdayMileage]

    CLI Examples:
        niu-api trips.summary_date serial=S3R1ALOFSC00T3R print=maxSpeed,everdayMileage
        niu-api trips.summary_date print=everdayMileage date=20211117
        niu-api trips.summary_date print=AvgSpeed,maxSpeed date=20211117,20211116,20211115
    """

    possible_prints = [
        'AvgSpeed', 'date', 'everdayMileage',
        'maxSpeed', 'ridingTime'
    ]

    if not isinstance(date, list): date = [ date ] # TODO

    scooters = apicommands.v5.scooter_list()

    out = {}
    trip_info = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')

        if serial is not None:
            if sn != serial:
                continue

        trips = apicommands.v3.motor_data_cycling_statistics(sn).get('items')
        for trip in trips:

            if trip.get('date') not in date: continue

            trip_info[trip.get('date')] = {}
            for arg in print:
                try:
                    if arg in possible_prints: trip_info[trip.get('date')][arg] = trip[arg]
                except KeyError:
                    pass

        # sort dict
        index_map = {v: i for i, v in enumerate(date)}
        out[sn] = {}
        for index in sorted(trip_info.items(), key=lambda pair: index_map[pair[0]]):
            for key in index:
                out[sn][index[0]] = key

    return out
