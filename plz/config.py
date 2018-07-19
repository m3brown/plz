import yaml
import sys
from colorama import Fore, Style
from .runner import run_command


def git_root():
    rc, output = run_command('git rev-parse --show-toplevel', std_output=False)
    if rc == 0:
        return output[0]
    else:
        print(Fore.RED + 'Could not find root of git repository' + Style.RESET_ALL)
        sys.exit(1)


def plz_config():
    root = git_root().rstrip('/')
    config_file = '{}/.plz.yaml'.format(root)
    print(Fore.CYAN)
    print("[INFO] Using config: {}".format(config_file))
    print(Style.RESET_ALL)
    return yaml.load(open(config_file))
