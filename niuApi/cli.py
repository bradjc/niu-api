"""CLI Script for NIU API
"""

from niuApi.arg import get_args
from niuApi.config import NIUConfig
from niuApi.requests import NIURequests
from niuApi.exceptions import NIURequestError

def run():

    args = get_args()
    config = NIUConfig()
    
    try:
        NIURequests(config)
    except NIURequestError as exc:
        print(exc)
        return 2

    return 0
