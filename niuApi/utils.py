def filter_list(array, filter):
    """Filter dict by another dict

    Args:
        array (list): input list
        filter (dict): filter dict

    Returns:
        list: filtered list
    """
    
    if filter is None:
        return array
    
    ret = []
    for entry in array:
        for key, value in entry.items():
            if filter.get(key) == value:
                ret.append(entry)

    return ret
