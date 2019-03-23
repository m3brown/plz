import yaml
import sys
import os
from colorama import Fore, Style
from .runner import run_command
import sh


def git_root():
    output = sh.Command('git')('rev-parse', '--show-toplevel')
    if output.exit_code == 0:
        return str(output).strip()
    else:
        print(Fore.RED + 'Could not find root of git repository' + Style.RESET_ALL)
        sys.exit(1)


def load_config(filename):
    print(Fore.CYAN)
    print("[INFO] Using config: {}".format(filename))
    print(Style.RESET_ALL)
    return yaml.load(open(filename), Loader=yaml.SafeLoader)


def plz_config():
    filename = '.plz.yaml'
    if os.path.isfile(filename):
        return (load_config(filename), None)
    else:
        root = git_root().rstrip('/')
        config_file = '{}/{}'.format(root, filename)
        return (load_config(config_file), root)
