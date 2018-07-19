import glob


def safe_glob(cmd_list):
    """
    Glob each string provided in a list, returning a flat list of globbed results.

    For any item in the list that is not globabble, leave the value as-is.

    For example, ['a', '*.py', 'test'] could return:
    ['a', 'main.py', 'sample.py', 'test]
    """

    new_list = []
    for item in cmd_list:
        g = glob.glob(item)
        if g:
            new_list.extend(g)
        else:
            new_list.append(item)
    return new_list
