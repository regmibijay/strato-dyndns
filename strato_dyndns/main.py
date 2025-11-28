import sys
from argparse import ArgumentParser

from .clients import DynDNSClient, DynDNSClientStatusException
from .lib.args_validator import ArgsValidator


def main(argv: list[str] | None = None) -> None:
    """Main entry point for the strato-dyndns CLI."""
    if argv is None:
        argv = sys.argv[1:]

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
        help="IP Addresses separated by space, use -v4 -v6 to determine automatically",
        nargs="+",
    )
    parser.add_argument(
        "-v4", help="Whether IPv4 should be updated", nargs="?", const=True
    )
    parser.add_argument(
        "-v6", help="Whether IPv6 should be updated", nargs="?", const=True
    )
    args = parser.parse_args(argv)

    config = ArgsValidator(arg=args).config_in_dict()
    dyndns = DynDNSClient(provider=args.provider)
    dyndns.init_data(data=config)

    try:
        print(f"Username: {config['username']}")
        print(f"Domain: {config['domain']}")
        print("IP(s):", *config["ip_addresses"])
        print("Trying to update records...")
        dyndns.update_record()
        print("Update request successful.")
    except DynDNSClientStatusException as e:
        print("=" * 40)
        print(f"Error updating record: {e}")
        print("=" * 40)
    finally:
        print(
            "\nFor any errors you encountered or suggestions, please report at:"
            "\nhttps://github.com/regmibijay/strato-dyndns/"
            "\nThank you!"
        )


if __name__ == "__main__":
    main()
