"""NUIApi output module
"""

from typing import Type
from niuApi.arg import get_args

def out(msg):

    args = get_args()
    out = args.out

    if isinstance(msg, dict):
        if out == 'uf':
            for value in msg.values():
                print(*value)
        else:
            print(msg)
    else:
        raise TypeError('Error in output type')
