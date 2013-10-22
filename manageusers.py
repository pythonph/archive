import argparse
import cmd

from app_mailreg import db
from app_mailreg.models import *

parser = argparse.ArgumentParser(description="Manages users")
parser.add_argument(
    "-i", "--interactive",
    action="store_const", const=True,
    help="run in interactive mode")
parser.add_argument(
    "-u", "--user",
    action="store", nargs=1,
    help="user for authorization")
parser.add_argument(
    "-p", "--password",
    action="store", nargs=1,
    help="password for authorization")
parser.add_argument(
    "action", choices=("add", "remove", "activate", "deactivate", "addrole",
                       "removerole", "purgeroles", "resetpassword"))

if __name__ == "__main__":
    args = parser.parse_args()
    print args.action
    if args.interactive:
        pass
