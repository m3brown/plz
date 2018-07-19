import glob
from os.path import join


def prepare_potential_glob(arg, path=None):
    if path:
        return join(path, arg)
    return arg


def deconstruct_glob(arg_list, path=None):
    if path:
        for idx, val in enumerate(arg_list):
            arg_list[idx] = val[len(path)+1:]


def safe_glob(cmd_list, cwd=None):
    """
    Glob each string provided in a list, returning a flat list of globbed results.

    For any item in the list that is not globabble, leave the value as-is.

    For example, ['a', '*.py', 'test'] could return:
    ['a', 'main.py', 'sample.py', 'test]
    """

    new_list = []
    for item in cmd_list:
        fullpath = prepare_potential_glob(item, cwd)
        g = glob.glob(fullpath)
        if g:
            deconstruct_glob(g, cwd)
            new_list.extend(g)
        else:
            new_list.append(item)
    return new_list
