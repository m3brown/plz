import os
import subprocess
import sys
import textwrap

import yaml
from jsonschema.exceptions import ValidationError

from .colorize import print_error, print_info, print_warning
from .schema import validate_configuration_data

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

            For more information on plz.yaml formatting, visit {}
            """.format(
                filename, DOC_URL
            )
        )
    )
    sys.exit(1)


def git_root():
    try:
        output = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
        return str(output).strip()
    except subprocess.CalledProcessError as e:
        if e.returncode == 128:
            raise NoFileException()
        else:
            raise e


def load_config(filename):
    try:
        config = yaml.load(open(filename), Loader=yaml.SafeLoader)
        try:
            validate_configuration_data(config)
        except ValidationError as e:
            print_warning("\n" + str(e))
            raise InvalidYamlException(filename)
        print_info("Using config: {}".format(filename), prefix=True)
        return config
    except yaml.YAMLError as e:
        raise InvalidYamlException(filename)


def find_file(filename):
    if os.path.isfile(filename):
        return (filename, None)
    else:
        root = git_root().rstrip("/")
        full_path = os.path.join(root, filename)
        if os.path.isfile(full_path):
            return (full_path, root)


def plz_config():
    try:
        match = find_file("plz.yaml")
        if not match:
            match = find_file(".plz.yaml")
            if match:
                print_warning(
                    "DEPRECATION WARNING: Please rename '.plz.yaml' to 'plz.yaml'"
                )
            else:
                raise NoFileException
        return (load_config(match[0]), match[1])
    except NoFileException:
        invalid_directory()
    except InvalidYamlException as e:
        invalid_yaml(e.filename)
