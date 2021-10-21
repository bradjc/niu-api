"""Argument functions
"""

import argparse

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

    return parse.parse_args()