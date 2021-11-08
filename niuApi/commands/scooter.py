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
