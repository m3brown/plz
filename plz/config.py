import yaml
import sys
from os.path import isfile
from colorama import Fore, Style
from .runner import run_command


def git_root():
    rc, output = run_command('git rev-parse --show-toplevel', std_output=False)
    if rc == 0:
        return output[0]
    else:
        print(Fore.RED + 'Could not find root of git repository' + Style.RESET_ALL)
        sys.exit(1)


def load_config(filename):
    print(Fore.CYAN)
    print("[INFO] Using config: {}".format(filename))
    print(Style.RESET_ALL)
    return yaml.load(open(filename))


def plz_config():
    filename = '.plz.yaml'
    if isfile(filename):
        return (load_config(filename), None)
    else:
        root = git_root().rstrip('/')
        config_file = '{}/{}'.format(root, filename)
        return (load_config(config_file), root)
