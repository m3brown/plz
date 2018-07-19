from .runner import gather_and_run_commands
from .config import git_root, plz_config
import argparse
import sys


def execute_from_config(cmd):
    (config, cwd) = plz_config()

    for task in config:
        if 'id' in task and task['id'] == cmd:
            if 'cmd' in task:
                rc = gather_and_run_commands(task['cmd'], cwd)
                sys.exit(rc)
    print(Fore.RED + "Could not find command with id '{}', review the available options in the config file.".format(cmd))
    print(Style.RESET_ALL)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')

    args = parser.parse_args()

    execute_from_config(args.cmd)


if __name__ == '__main__':
    main()
