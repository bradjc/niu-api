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

def detailed_date(
    serial: str = None,
    print: list = ['avespeed', 'distance'],
    date: list = [today.strftime("%Y%m%d")],
) -> dict:
    """Get all trips by date

    serial
        Serial number of scooter to limit output.
    
    print
        Limit output for keys:
            [avespeeed, date, distance, startTime,
            power_consumption, ridingtime, endTime]
        Default = [avespeed, distance]

    CLI Examples:
        niu-api trips.detailed_date serial=S3R1ALOFSC00T3R print=ridingtime
        niu-api trips.detailed_date print=everdayMileage date=20211117
        niu-api trips.detailed_date print=avespeeed,power_consumption date=20211117,20211116,20211115
    """

    possible_prints = [
        'avespeed', 'date', 'distance',
        'ridingtime', 'startTime', 'endTime',
        'power_consumption'
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

        for day in date:
            loopindex = 0
            date_match = False
            trips_full = {}
            trips_list = []

            if day > today.strftime("%Y%m%d"):
                return out

            while date_match is False:
                trips_full = apicommands.v5.track_list_v2(sn, 100, loopindex)
                trips_list = trips_full.get('track_mileage')
                if len(trips_list) == 0: # break if trips are empty
                    trips_full = {}
                    trips_list = []
                    break

                for trip in trips_list:
                    if str(trip.get('date')) == str(day):
                        date_match = True
                        break

                if not date_match:
                    loopindex += 1
                else:
                    break # break while loop, if date is found
            
            for trip in trips_full.get('items', []):

                if str(trip.get('date')) != day: continue

                if not trip_info.get(trip.get('date')):
                    trip_info[trip.get('date')] = {}
                trip_info[trip.get('date')][trip.get('trackId')] = {}
                for arg in print:
                    try:
                        if arg in possible_prints: trip_info[trip.get('date')][trip.get('trackId')][arg] = trip[arg]
                    except KeyError:
                        pass

        out[sn] = trip_info

    return out
