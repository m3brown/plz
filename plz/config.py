import os
import sys
import textwrap

import sh
import yaml

from .colorize import print_error
from .colorize import print_info

DOC_URL = "https://github.com/m3brown/plz"


class NoFileException(Exception):
    pass


class InvalidYamlException(Exception):
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            setattr(self, "filename", args[0])
        return super(InvalidYamlException, self).__init__(*args, **kwargs)


def invalid_directory():
    print(
        textwrap.dedent(
            """
            plz must be run from:
              a) a directory that has a valid plz.yaml file or
              b) within a git repo that contains a plz.yaml in the repo root path.

            For more information, visit {}
            """
        ).format(DOC_URL)
    )
    sys.exit(1)


def invalid_yaml(filename):
    print_error(
        textwrap.dedent(
            """
            Error parsing yaml config: {}

            For more information on .plz.yaml formatting, visit {}
            """.format(
                filename, DOC_URL
            )
        )
    )
    sys.exit(1)


def git_root():
    try:
        output = sh.Command("git")("rev-parse", "--show-toplevel")
        return str(output).strip()
    except sh.ErrorReturnCode_128:
        raise NoFileException()


def load_config(filename):
    try:
        config = yaml.load(open(filename), Loader=yaml.SafeLoader)
        print_info("Using config: {}".format(filename), prefix=True)
        return config
    except yaml.YAMLError as e:
        raise InvalidYamlException(filename)


def plz_config():
    filename = ".plz.yaml"
    try:
        if os.path.isfile(filename):
            return (load_config(filename), None)
        else:
            root = git_root().rstrip("/")
            full_path = os.path.join(root, filename)
            if os.path.isfile(full_path):
                return (load_config(full_path), root)
            raise NoFileException
    except NoFileException:
        invalid_directory()
    except InvalidYamlException as e:
        invalid_yaml(e.filename)
