import os
import subprocess
import shlex
from itertools import chain
from colorama import Fore, Style
from .glob_tools import process_absolute_glob, process_relative_glob

env = dict(os.environ, **{'PYTHONUNBUFFERED': '1'})


def run_command(command, std_output=True, cwd=None, args=[]):
    pwd = os.getcwd()
    if not cwd:
        cwd = pwd
    cleaned_cmd = process_absolute_glob(shlex.split(command), cwd=cwd)
    if args:
        relpath = os.path.relpath(pwd, cwd)
        args = process_relative_glob(args, post_adjust_path=relpath)
    process = subprocess.Popen(
        chain(cleaned_cmd, args), stdout=subprocess.PIPE, cwd=cwd, env=env)
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


def gather_and_run_commands(cmd, cwd=None, args=[]):
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
        rc, _ = run_command(cmd, cwd=cwd, args=args)
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
                rc = gather_and_run_commands(item, cwd=cwd, args=args)
    else:
        raise Exception("Unrecognized cmd type: {}".format(type(cmd)))
    return rc
