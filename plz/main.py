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
    options = sorted([task["id"] for task in config["commands"]])
    print("Available commands from config:")
    for cmd in options:
        print(" - {cmd}".format(cmd=cmd))
    print()


def compile_environment(cmd_env: Optional[dict], global_env: Optional[dict]) -> dict:
    if cmd_env or global_env:
        return {**os.environ.copy(), **global_env, **cmd_env}
    else:
        return {}


def command_detail(command):
    print()
    id = command.pop("id")
    print("id: {}".format(id))
    print(yaml.dump(command))


def execute_from_config(cmd, args):
    (config, cwd) = plz_config()

    for task in config["commands"]:
        if "id" in task and task["id"] == cmd:
            if "cmd" in task:
                if "dir" in task:
                    cwd = os.path.join(cwd or "", task["dir"])
                kwargs = {
                    "cwd": cwd,
                    "args": args,
                }
                env = compile_environment(
                    task.get("env", {}), global_env=config.get("global_env", {})
                )
                if env:
                    kwargs["env"] = env
                rc = gather_and_run_commands(task["cmd"], **kwargs)
                sys.exit(rc)
    if cmd and cmd.lower() == "help":
        if len(args) == 1:
            for task in config["commands"]:
                if "id" in task and task["id"] == args[0]:
                    command_detail(task)
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
