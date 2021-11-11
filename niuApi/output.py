"""NUIApi output module
"""

import json

from niuApi.arg import get_args

def out(msg):

    args = get_args()
    out = args.out

    if isinstance(msg, dict):
        if out == 'uf':
            for sn, infos in msg.items():
                if not isinstance(infos, dict):
                    raise TypeError(f'{infos} is not a dict')

                if args.print_serial: print(sn)
                skip = False
                for value in infos.values():
                    if isinstance(value, dict):
                        skip = True
                        if args.print_serial:
                            print('\t {0}'.format(*value.values()))
                        else:
                            print(*value.values())

                if not skip:
                    if args.print_serial:
                        print('\t {0}'.format(*infos.values()))
                    else:
                        print(*infos.values())

        elif out == 'json':
            print(json.dumps(msg))
        else:
            print(msg)
    else:
        raise TypeError('Error in output type')
