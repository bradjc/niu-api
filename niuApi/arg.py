"""Argument functions
"""

import argparse
import json

from niuApi import NAME, VERSION

def get_args():

    parse = argparse.ArgumentParser(prog=NAME)

    parse.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{NAME}: {VERSION}'
    )

    parse.add_argument(
        '-c',
        '--config',
        dest='config_file',
        help='Set config file (default: /etc/niu-api/config.yaml)',
        default='/etc/niu-api/config.yaml'
    )

    parse.add_argument(
        'action',
        help='Execute command'
    )

    parse.add_argument(
        'options',
        nargs='*',
        action=StoreDictKeyPair
    )

    return parse.parse_args()

class StoreDictKeyPair(argparse.Action):

     def __call__(self, parser, namespace, values, option_string=None):

        setattr(namespace, self.dest, dict())

        for value in values:
            key, value = value.split('=')

            if value.lower() == 'true':
                value = json.loads(value.lower())

            getattr(namespace, self.dest)[key] = value