"""CLI Script for NIU API
"""

from niuApi.arg import get_args
from niuApi.config import NIUConfig

def run():

    args = get_args()
    config = NIUConfig()
