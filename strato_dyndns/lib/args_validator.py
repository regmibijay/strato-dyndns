from typing import DefaultDict

from ..clients import ConnectionHandler
from .file_operations import read_config, write_config


class ArgsValidator:
    """
    Validates CLI args in `main.py`,
    expects `arg` which is a set of arguments from
    `ArgumentParser`.
    """

    ARG: dict
    CONFIG: dict = DefaultDict()
    CNH: ConnectionHandler

    def __init__(self, arg) -> None:
        self.ARG = arg
        self.CNH = ConnectionHandler()
        try:
            self.config()
        except Exception as e:
            print("Could not process your parameters, reason:", str(e))
            exit()

    def is_valid_string(self, object) -> bool:
        if object is None:
            return False
        if type(object) == bool:
            return False
        if isinstance(object, list):
            if not all([self.is_valid_string(x) for x in object]):
                return False
        if object.replace(" ", "") == "":
            return False
        return True

    def validate_config(self, config: dict) -> dict:
        valid_keys = ["username", "password", "domain"]
        if not all([key in config.keys() for key in valid_keys]):
            print("Config file did not contain some required fields.")
            exit()
        return config

    def config(self):
        if self.ARG.config:
            self.CONFIG = self.validate_config(read_config(self.ARG.config))
            if self.ARG.username and self.is_valid_string(self.ARG.username):
                self.CONFIG["username"] = self.ARG.username
            if self.ARG.password and self.is_valid_string(self.ARG.password):
                self.CONFIG["password"] = self.ARG.password
            if self.ARG.domain and self.is_valid_string(self.ARG.domain):
                self.CONFIG["domain"] = self.ARG.domain
            if self.ARG.ip:
                self.CONFIG["ip_addresses"] = self.ARG.ip
            if not self.ARG.ip:
                if self.ARG.v4 is True:
                    self.CONFIG["ip_addresses"].append(self.CNH.get_ip_v4())
                if self.ARG.v4 and self.ARG.v4 is not True:
                    self.CONFIG["ip_addresses"].append(self.ARG.v4)
                if self.ARG.v6 is True:
                    self.CONFIG["ip_addresses"].append(self.CNH.get_ip_v6())
                if self.ARG.v6 and self.ARG.v6 is not True:
                    self.CONFIG["ip_addresses"].append(self.ARG.v6)
                if self.ARG.v4 is None and self.ARG.v6 is None:
                    print(
                        """
                    No IP Adressses provided and no -v4 or -v6 flag set. 
                    Script will not determine interfaces automatically. Please
                    specify either interface.
                    """
                    )
                    exit()
        else:
            if not self.ARG.username or not self.ARG.password or not self.ARG.domain:
                print(
                    """
                Neither config nor proper authentication details were provided. Please provide
                either with -c or -u, -p, -d.
                """
                )
                exit()

            self.CONFIG["username"] = self.ARG.username
            self.CONFIG["password"] = self.ARG.password
            self.CONFIG["domain"] = self.ARG.domain
            self.CONFIG["ip_addresses"] = []
            if not self.ARG.ip:
                if self.ARG.v4 is True:
                    print("Determining external ipv4")
                    self.CONFIG["ip_addresses"].append(self.CNH.get_ip_v4())
                if self.ARG.v4 and self.ARG.v4 is not True:
                    self.CONFIG["ip_addresses"].append(self.ARG.v4)
                if self.ARG.v6 is True:
                    print("Determining external ipv6")
                    self.CONFIG["ip_addresses"].append(self.CNH.get_ip_v6())
                if self.ARG.v6 and self.ARG.v6 is not True:
                    self.CONFIG["ip_addresses"].append(self.ARG.v6)
                if self.ARG.v4 is None and self.ARG.v6 is None:
                    print(
                        """
                    No IP Adressses provided and no -v4 or -v6 flag set. 
                    Script will not determine interfaces automatically. Please
                    specify either interface.
                    """
                    )
                    exit()

    def config_in_dict(self):
        return dict(self.CONFIG)
