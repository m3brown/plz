import os
import shlex
import textwrap

import sh

from .colorize import print_error
from .colorize import print_error_dim
from .colorize import print_info_dim
from .glob_tools import process_absolute_glob
from .glob_tools import process_relative_glob


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
        print_info_dim(
            textwrap.dedent(
                """
                ===============================================================================
                Running command: {}
                ===============================================================================
                """.format(
                    " ".join([cmd] + args)
                )
            )
        )
        rc = run_command(cmd, cwd=cwd, args=args)
        print()
        if rc > 0:
            print_error("Process failed", prefix=True)
        else:
            print_info_dim("Process complete", prefix=True)
    elif type(cmd) == list:
        rc = 0
        for item in cmd:
            if rc > 0:
                print_error_dim(
                    textwrap.dedent(
                        """
                        ===============================================================================
                        Skipping command due to previous errors: '{}'
                        ===============================================================================
                        """.format(
                            " ".join([item] + args)
                        )
                    )
                )
            else:
                rc = gather_and_run_commands(item, cwd=cwd, args=args)
    else:
        raise Exception("Unrecognized cmd type: {}".format(type(cmd)))
    return rc
