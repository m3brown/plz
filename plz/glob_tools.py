import glob
from os.path import join, normpath
from functools import partial


def safe_glob(cmd):
    """
    For any item that is not globabble, leave the value as-is.
    """
    result = glob.glob(cmd)
    if result:
        return (True, result)
    else:
        return (False, [cmd])


def trim_prefix(file_path, prefix):
    if prefix and file_path.startswith(prefix):
        file_path = file_path[len(prefix)+1:]
    return file_path


def absolute_glob(cmd, cwd):
    """
    Glob string from a provided root path
    """

    match, result = safe_glob(join(cwd, cmd))
    if match:
        return map(partial(trim_prefix, prefix=cwd), result)
    else:
        return [cmd]


def relative_glob(cmd, post_adjust_path=None):
    """
    Glob string from the current working directory. If post_adjust_path
    is provided, prepend that path in front of any glob results.
    """

    match, result = safe_glob(cmd)
    if match and post_adjust_path:
        return map(lambda x: normpath(join(post_adjust_path, x)), result)
    else:
        return result


def process_absolute_glob(cmd_list, cwd):
    for cmd in cmd_list:
        for result in absolute_glob(cmd, cwd):
            yield result


def process_relative_glob(cmd_list, post_adjust_path=None):
    for cmd in cmd_list:
        for result in relative_glob(cmd, post_adjust_path):
            yield result
