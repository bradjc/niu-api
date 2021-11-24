import niuApi.apicommands as apicommands
import niuApi.utils as utils

def detection(
    serial: str = None,
    print: list = ['score', 'gradeTitle'],
    **kwargs
) -> dict:
    """Get basiscs of detection

    serial
        Serial number of scooter to limit output.
    
    print
        Limit output for keys:
            [faultsCount, gradeDesc, gradeTitle, id, score]
        Default = [score, gradeTitle]

    CLI Examples:
        niu-api service.detection
        niu-api service.detection serial=S3R1ALOFSC00T3R
        niu-api service.detection print=faultsCount
    """

    possible_prints = [
        'faultsCount', 'gradeDesc', 'gradeTitle', 'id',
        'score'
    ]

    if not isinstance(print, list): print = [ print ] # TODO

    scooters = apicommands.v5.scooter_list()

    out = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        out[sn] = {}

        if serial is not None:
            if sn != serial:
                continue

        detection = apicommands.v3.service_intelligent_detection(sn)

        for arg in print:
            try:
                if arg in possible_prints: out[sn][arg] = detection[arg]
            except KeyError:
                pass


    return out

def detailed_detection(
    serial: str = None,
    print: list = ['title', 'statusDesc'],
    filter: dict = None,
    **kwargs
) -> dict:
    """Get elements of detailed detection

    serial
        Serial number of scooter to limit output.

    print
        Limit output for keys:
            [faultDesc, graded, isFaults, statusDesc, system, title]
        Default = [title, statusDesc]

    filter
        Filter output for keys:
            [chargeNum, code, faultDesc, feature, graded, isFaults,
            statusDesc, system, title]

    CLI Examples:
        niu-api service.detailed_detection filter=system:electronicSystem
        niu-api service.detailed_detection serial=S3R1ALOFSC00T3R
        niu-api service.detailed_detection print=title,isFaults filter=isFaults:false
    """

    possible_prints = [
        'faultDesc', 'graded', 'isFaults', 'statusDesc',
        'system', 'title'
    ]

    scooters = apicommands.v5.scooter_list()

    out = {}
    for scooter in scooters:
        sn = scooter.get('sn_id')
        out[sn] = {}

        if serial is not None:
            if sn != serial:
                continue

        detection = utils.filter_list(apicommands.v3.service_intelligent_detection(sn).get('items'), filter)

        for part in detection:
            code = part.get('code')
            out[sn][code] = {}

            for arg in print:
                try:
                    if arg in possible_prints: out[sn][code][arg] = part[arg]
                except KeyError:
                    pass

    return out
