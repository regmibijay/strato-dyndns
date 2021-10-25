import sys
from argparse import ArgumentParser

from .clients import DynDNSClient, DynDNSClientStatusException
from .lib.args_validator import ArgsValidator


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
        "-ip",
        "--ip",
        help="IP Addresses separated by space, use -v4 -v6 if IP should be determined automatically",
        nargs="+",
    )
    parser.add_argument(
        "-v4", help="Whether IPV4 should be updated.", nargs="?", const=True
    )
    parser.add_argument(
        "-v6", help="Whether IPV6 should be updated", nargs="?", const=True
    )
    args = parser.parse_args()
    CONFIG = ArgsValidator(arg=args).config_in_dict()
    dyndns = DynDNSClient(provider=args.provider)
    dyndns.init_data(data=CONFIG)
    try:
        print("Username:", CONFIG["username"])
        print("Domain:", CONFIG["domain"])
        print("IP(s):")
        print(*CONFIG["ip_addresses"])
        print("\rTrying to update records", sep="")
        dyndns.update_record()
        print("Update request successful.")
    except DynDNSClientStatusException as e:
        print(f"Error updating record: {str(e)}")
    finally:
        print(
            """
        For any errors you encountered or suggestion that came to your mind
        during usage of this script, please report it to 
        \nhttps://github.com/regmibijay/strato-dyndns/\n
        Thank you!"""
        )


if __name__ == "__main__":
    main()
