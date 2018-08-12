import os
import subprocess
import sh
import shlex
from itertools import chain
from colorama import Fore, Style
from .glob_tools import process_absolute_glob, process_relative_glob


def run_command(command, cwd=None, args=[]):
    pwd = os.getcwd()
    if not cwd:
        cwd = pwd
    cleaned_cmd = list(process_absolute_glob(shlex.split(command), cwd=cwd))
    if args:
        relpath = os.path.relpath(pwd, cwd)
        args = list(process_relative_glob(args, post_adjust_path=relpath))
    executable = cleaned_cmd[0]
    try:
        if cwd != pwd:
            os.chdir(cwd)
        sh.Command(executable)(*(cleaned_cmd[1:] + args), _fg=True)
    except sh.ErrorReturnCode:
        return 1
    return 0


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
        rc = run_command(cmd, cwd=cwd, args=args)
        if rc > 0:
            print(Fore.RED)
            print("[ERROR] Process failed")
        else:
            print(Fore.CYAN + Style.DIM)
            print("[INFO] Process complete")
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
