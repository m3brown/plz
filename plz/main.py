from .runner import gather_and_run_commands
from .config import git_root, plz_config
from colorama import Fore, Style
import argparse
import sys


def execute_from_config(cmd, args):
    (config, cwd) = plz_config()

    for task in config:
        if 'id' in task and task['id'] == cmd:
            if 'cmd' in task:
                rc = gather_and_run_commands(task['cmd'], cwd=cwd, args=args)
                sys.exit(rc)
    print(Fore.RED + "Could not find command with id '{}', review the available options in the config file.".format(cmd))
    print(Style.RESET_ALL)
    sys.exit(1)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('passthrough_args', nargs=argparse.REMAINDER)

    args = parser.parse_args(args)

    execute_from_config(args.cmd, args.passthrough_args)
