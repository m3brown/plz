import os
import shlex
import subprocess
import textwrap

from .colorize import print_error, print_error_dim, print_info_dim, print_warning
from .glob_tools import process_absolute_glob, process_relative_glob


def inject_shortcuts(command, shortcuts={}):
    for k, v in shortcuts.items():
        command = command.replace("${{{}}}".format(k), v)
    return command


def run_command(command, cwd=None, args=[], env=None):
    pwd = os.getcwd()
    if not cwd:
        cwd = pwd
    cleaned_cmd = list(process_absolute_glob(shlex.split(command), cwd=cwd))
    if args:
        relpath = os.path.relpath(pwd, cwd)
        args = list(process_relative_glob(args, post_adjust_path=relpath))
    executable = cleaned_cmd[0]
    try:
        subprocess.check_call(cleaned_cmd + args, cwd=cwd, env=env)
    except subprocess.CalledProcessError:
        return 1
    except KeyboardInterrupt:
        print_warning("\nProcess aborted")
        return 1
    return 0


def gather_and_run_commands(cmd, **kwargs):
    """
    The cmd argument can either be a string or list

    - If it's a string, execute the command.
    - If it's a list, recursively run each item in the list.
    """
    if type(cmd) == str:
        shortcuts = kwargs.pop("shortcuts", [])
        if shortcuts:
            cmd = inject_shortcuts(cmd, shortcuts)

        print_info_dim(
            textwrap.dedent(
                """
                ===============================================================================
                Running command: {}
                ===============================================================================
                """.format(
                    " ".join([cmd] + kwargs.get("args", []))
                )
            )
        )
        rc = run_command(cmd, **kwargs)
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
                            " ".join([item] + kwargs.get("args", []))
                        )
                    )
                )
            else:
                rc = gather_and_run_commands(item, **kwargs)
    else:
        raise Exception("Unrecognized cmd type: {}".format(type(cmd)))
    return rc
