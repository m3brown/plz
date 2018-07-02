import yaml
import subprocess
import shlex
import sys
from colorama import Fore, Style


def run_command(command, std_output=True, cwd=None):
    process = subprocess.Popen(shlex.split(
        command), stdout=subprocess.PIPE, cwd=cwd)
    output_log = []
    while True:
        output = process.stdout.readline().decode('utf-8').strip()
        if output == '' and process.poll() is not None:
            break
        if output:
            output_log.append(output)
            if std_output:
                print(output)
    rc = process.poll()
    return rc, output_log


def git_root():
    rc, output = run_command('git rev-parse --show-toplevel', std_output=False)
    if rc == 0:
        return output[0]
    else:
        print(Fore.RED + 'Could not find root of git repository' + Style.RESET_ALL)
        sys.exit(1)


def plz_config(root):
    root = root.rstrip('/')
    config_file = '{}/plz.config'.format(root)
    print(Fore.CYAN)
    print("[INFO] Using config: {}".format(config_file))
    print(Style.RESET_ALL)
    return yaml.load(open(config_file))


def gather_and_run_commands(cmd):
    """
    The cmd argument can either be a string or a list.

    If it's a list, recursively run each item in the list. If it's a string, execute the command.
    """

    if type(cmd) == str:
        print(Fore.CYAN + Style.DIM +
              "===============================================================================")
        print("Running command: {}".format(cmd))
        print("===============================================================================")
        print(Style.RESET_ALL)
        rc, _ = run_command(cmd)
        if rc > 0:
            print(Fore.RED)
        else:
            print(Fore.CYAN + Style.DIM)
        print("[INFO] Process complete, return code: {}".format(rc))
        print(Style.RESET_ALL)
    elif type(cmd) == list:
        rc = 0
        for item in cmd:
            if rc > 0:
                print(Fore.RED + Style.DIM +
                      "===============================================================================")
                print("Skipping command due to previous errors: '{}'".format(item))
                print(
                    "===============================================================================")
                print(Style.RESET_ALL)
            else:
                rc = gather_and_run_commands(item)
    else:
        raise Exception("Unrecognized cmd type: {}".format(type(cmd)))
    return rc


def execute_from_config(cmd):
    root = git_root()
    config = plz_config(root)

    for task in config:
        if 'id' in task and task['id'] == cmd:
            if 'cmd' in task:
                rc = gather_and_run_commands(task['cmd'])
                sys.exit(rc)
    print(Fore.RED + "Could not find command with id '{}', review the available options in the config file.".format(cmd))
    print(Style.RESET_ALL)
    sys.exit(1)
