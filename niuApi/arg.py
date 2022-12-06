"""Argument functions
"""

import argparse
import json

from niuApi import NAME, VERSION


def get_args():

    parse = argparse.ArgumentParser(prog=NAME)

    parse.add_argument(
        "-v", "--version", action="version", version=f"{NAME}: {VERSION}"
    )

    parse.add_argument(
        "-c",
        "--config",
        dest="config_file",
        help="Set config file (default: /etc/niu-api/config.yaml)",
        default="/etc/niu-api/config.yaml",
    )

    parse.add_argument(
        "-o",
        "--out",
        dest="out",
        help="Set output type (default: uf (userfriendly))",
        choices=["raw", "uf", "json"],
        default="uf",
    )

    parse.add_argument(
        "--no_serial",
        dest="print_serial",
        help="Dont print serial number of scooter",
        action="store_false",
    )

    parse.add_argument("action", help="Execute command", nargs="?")

    parse.add_argument("options", nargs="*", action=StoreDictKeyPair, default={})

    return parse.parse_args()


class StoreDictKeyPair(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        setattr(namespace, self.dest, dict())

        for value in values:
            key, value = value.split("=")

            if value.lower() == "true" or value.lower() == "false":
                value = json.loads(value.lower())
            elif "," in value and not ":" in value:
                value = value.split(",")
            elif "," in value and ":" in value or ":" in value:
                value = value.split(",")
                for idx, val in enumerate(value):
                    if not ":" in val:
                        value.pop(idx)

                value = dict(map(lambda s: s.split(":"), value))
                # value = dict(map(lambda k, x: [k, json.loads(x.lower()) if x.lower() == 'true' or x.lower() == 'false' else x], value.keys(), value.values()))

                for subkey, subvalue in value.items():

                    if subvalue.lower() == "true" or subvalue.lower() == "false":
                        value[subkey] = json.loads(subvalue.lower())

                    try:
                        value[subkey] = int(subvalue)
                    except ValueError:
                        pass

            getattr(namespace, self.dest)[key] = value
