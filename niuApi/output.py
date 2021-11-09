"""NUIApi output module
"""

from typing import Type
from niuApi.arg import get_args

def out(msg):

    args = get_args()
    out = args.out

    if isinstance(msg, dict):
        if out == 'uf':
            for infos in msg.values():
                if not isinstance(infos, dict):
                    raise TypeError(f'{infos} is not a dict')
                
                skip = False
                for value in infos.values():
                    if isinstance(value, dict):
                        skip = True
                        print(*value.values())
                
                if not skip: print(*infos.values())
        else:
            print(msg)
    else:
        raise TypeError('Error in output type')
