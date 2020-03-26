import argparse
import os
import sys

from plz.colorize import print_error
from plz.colorize import print_info

from .config import plz_config
from .runner import gather_and_run_commands


def usage():
    print_info("Usage:\nplz <command> [<additional arguments> ...]")


def list_options(config):
    options = sorted([task["id"] for task in config])
    print("Available commands from config:")
    for cmd in options:
        print(" - {cmd}".format(cmd=cmd))
    print()


def execute_from_config(cmd, args):
    (config, cwd) = plz_config()

    for task in config:
        if "id" in task and task["id"] == cmd:
            if "cmd" in task:
                if "dir" in task:
                    cwd = os.path.join(cwd or "", task["dir"])
                rc = gather_and_run_commands(task["cmd"], cwd=cwd, args=args)
                sys.exit(rc)
    if cmd and cmd.lower() == "help":
        usage()
        list_options(config)
    else:
        print_error("Could not find command with id '{}'".format(cmd))
        list_options(config)
    sys.exit(1)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("cmd", nargs="?", default="help")
    parser.add_argument("passthrough_args", nargs=argparse.REMAINDER)

    if len(args) < 1:
        (config, _) = plz_config()
        print()
        usage()
        list_options(config)
        sys.exit(1)

    args = parser.parse_args(args)

    execute_from_config(args.cmd, args.passthrough_args)
