import subprocess
import shlex
from colorama import Fore, Style
from .glob_tools import safe_glob


def run_command(command, std_output=True, cwd=None):
    cleaned_cmd = safe_glob(shlex.split(command), cwd=cwd)
    process = subprocess.Popen(cleaned_cmd, stdout=subprocess.PIPE, cwd=cwd)
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


def gather_and_run_commands(cmd, cwd=None):
    """
    The cmd argument can either be a string or list

    - If it's a string, execute the command.
    - If it's a list, recursively run each item in the list.
    """
    if type(cmd) == str:
        print(Fore.CYAN + Style.DIM +
              "===============================================================================")
        print("Running command: {}".format(cmd))
        print("===============================================================================")
        print(Style.RESET_ALL)
        rc, _ = run_command(cmd, cwd=cwd)
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
                rc = gather_and_run_commands(item, cwd=cwd)
    else:
        raise Exception("Unrecognized cmd type: {}".format(type(cmd)))
    return rc
