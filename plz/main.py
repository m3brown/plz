import argparse
import os
import sys
from typing import Optional

import yaml

from plz.colorize import print_error, print_info

from .config import plz_config
from .runner import gather_and_run_commands


def usage():
    print_info("Usage:\nplz <command> [<additional arguments> ...]")


def list_options(config):
    options = config["commands"].keys()
    print("Available commands from config:")
    for cmd in options:
        print(" - {}".format(cmd))
    print()


def compile_environment(cmd_env: Optional[dict], global_env: Optional[dict]) -> dict:
    if cmd_env or global_env:
        return {**os.environ.copy(), **global_env, **cmd_env}
    else:
        return {}


def command_detail(key, data):
    print()
    print(yaml.dump({key: data}))


def execute_from_config(cmd, args):
    (config, cwd) = plz_config()

    data = config["commands"].get(cmd, None)
    if data:
        if type(data) in [str, list]:
            data = {"cmd": data}
        if data.get("cmd"):
            if data.get("dir"):
                cwd = os.path.join(cwd or "", data["dir"])
            kwargs = {
                "cwd": cwd,
                "args": args,
                "shortcuts": config.get("shortcuts", {}),
            }
            env = compile_environment(
                data.get("env", {}), global_env=config.get("global_env", {})
            )
            if env:
                kwargs["env"] = env
            if data.get("description"):
                print_info("\nDescription: {}".format(data["description"]))
            rc = gather_and_run_commands(data["cmd"], **kwargs)
            sys.exit(rc)
    elif cmd and cmd.lower() == "help":
        if len(args) == 1:
            data = config["commands"].get(args[0], None)
            if data:
                command_detail(args[0], data)
                sys.exit(0)

        usage()
        list_options(config)
        sys.exit(0)
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
