import os
import sys
from argparse import ArgumentParser

from .clients import ConnectionHandler, DynDNSClient, DynDNSClientStatusException
from .lib.file_operations import read_config


def check_if_not_empty(string: str) -> bool:
    """
    Checks if provided string is empty
    """
    if type(string) == bool:
        return False

    if string is None:
        return False

    if not string.replace(" ", "") == "":
        return True

    return False


def handle_config(path: str):
    """
    Handles config
    """
    if not os.path.exists(path):
        print(f"Config file not found under {path}")
        exit()

    config = read_config(path)
    req_fields = ["username", "password", "domain", "ip_addresses"]
    for field in req_fields:
        if not field in config.keys():
            print(f"`{path}` does not match config file format.")
            exit()
    return config


def main(argv=sys.argv[1:]):
    parser = ArgumentParser(description="Main executable")
    parser.add_argument(
        "-c",
        "--config",
        help="Config file containing parameters",
        nargs="?",
        const="",
    )
    parser.add_argument("provider", help="Provider", default="strato")
    parser.add_argument("-u", "--username", help="Username", nargs="?", const=True)
    parser.add_argument("-p", "--password", help="Password", nargs="?", const=True)
    parser.add_argument("-d", "--domain", help="Domain", nargs="?", const=True)
    parser.add_argument(
        "-ip", "--ip", help="IP Addresses separated by space", nargs="+"
    )
    parser.add_argument(
        "-v4", help="Whether IPV4 should be updated", nargs="?", const=True
    )
    parser.add_argument(
        "-v6", help="Whether IPV6 should be updated", nargs="?", const=True
    )
    args = parser.parse_args()

    # checking for CLI flags
    if args.config is None:
        args.config = False
        CONFIG = False

    if (not args.config) and not (args.username or args.password or args.domain):
        print(
            """
            Neither config file nor authentication details were provided.
            Please provide either.
            """
        )
        exit()

    if (args.config) and (args.username or args.password or args.domain):
        print(
            """
        Both config file and authentication details were provided.
        Please provide either.
        """
        )
        exit()

    if not args.provider or not check_if_not_empty(args.provider):
        args.provider = "strato"

    if args.config and check_if_not_empty(args.config):
        CONFIG = handle_config(args.config)

    if not (args.config) and (args.username or args.password or args.domain):
        CONFIG = {
            "username": args.username,
            "password": args.password,
            "domain": args.domain,
            "ip_addresses": [],
        }

    if not check_if_not_empty(args.config) and not CONFIG:
        print(f"`{args.config}` is not valid file path.")
        print("Please specify proper config file path")
        exit()

    cnh = ConnectionHandler()
    if not (args.config) and not (args.ip):
        if args.v4:
            CONFIG["ip_addresses"].append(cnh.get_ip_v4())
        if args.v6:
            CONFIG["ip_addresses"].append(cnh.get_ip_v6())

    if args.v4:
        ipv4 = cnh.get_ip_v4()
        print(f"Obtained IPV4: `{ipv4}`")
        CONFIG["ip_addresses"].append(ipv4)
    if args.v6:
        ipv6 = cnh.get_ip_v6()
        print(f"Obtained IPV6: `{ipv6}`")
        CONFIG["ip_addresses"].append()

    if (args.v4 is None) and (args.v6 is None):
        print(
            """
        You did not explicitly specify a V4 or V6 address.
        Both will be automatically determined.
        """
        )
        ipv4 = cnh.get_ip_v4()
        print(f"Obtained IPV4: `{ipv4}`")
        CONFIG["ip_addresses"].append(ipv4)
        ipv6 = cnh.get_ip_v6()
        print(f"Obtained IPV6: `{ipv6}`")
        CONFIG["ip_addresses"].append(ipv6)

    dyndns = DynDNSClient(provider=args.provider)
    dyndns.init_data(data=CONFIG)
    try:
        dyndns.update_record()
    except DynDNSClientStatusException as e:
        print(f"Error updating record: {str(e)}")


if __name__ == "__main__":
    main()
