from .runner import gather_and_run_commands
from .config import git_root, plz_config
from colorama import Fore, Style
import argparse
import sys


def usage():
    print(Fore.BLUE + "Usage:\nplz <command> [<additional arguments> ...]")
    print(Style.RESET_ALL)


def list_options(config):
    options = sorted([task['id'] for task in config])
    print('Available commands from config:')
    for cmd in options:
        print(' - {cmd}'.format(cmd=cmd))


def execute_from_config(cmd, args):
    (config, cwd) = plz_config()

    for task in config:
        if 'id' in task and task['id'] == cmd:
            if 'cmd' in task:
                rc = gather_and_run_commands(task['cmd'], cwd=cwd, args=args)
                sys.exit(rc)
    if cmd and cmd.lower() == 'help':
        usage()
        list_options(config)
    else:
        print(Fore.RED + "Could not find command with id '{}'".format(cmd))
        print(Style.RESET_ALL)
        list_options(config)
    sys.exit(1)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('cmd', nargs='?', default='help')
    parser.add_argument('passthrough_args', nargs=argparse.REMAINDER)

    if len(args) < 1:
        (config, cwd) = plz_config()
        print()
        usage()
        list_options(config)
        sys.exit(1)

    args = parser.parse_args(args)

    execute_from_config(args.cmd, args.passthrough_args)
