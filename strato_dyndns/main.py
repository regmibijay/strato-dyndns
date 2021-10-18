import sys
from argparse import ArgumentParser

from .clients import ConnectionHandler, DynDNSClient


def main(argv=sys.argv[1:]):
    parser = ArgumentParser(description="Main executable")
    parser.add_argument("-c", "--config", help="Config file", nargs="?", const=False)
    parser.add_argument("-u", "--username", help="Username", nargs="?", const=False)
    parser.add_argument("-p", "--password", help="Password", nargs="?", const=False)
    parser.add_argument("-d", "--domain", help="Domain", nargs="?", const=False)
    parser.add_argument(
        "-ip", "--ip", help="IP Addresses separated by comma", nargs="?", const=False
    )
    args = parser.parse_args()
    return True


if __name__ == "__main__":
    main()
