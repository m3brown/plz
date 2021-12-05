## plz-cmd

[![Build Status](https://travis-ci.org/m3brown/plz.svg?branch=master)](https://travis-ci.org/m3brown/plz)
[![Coverage Status](https://coveralls.io/repos/github/m3brown/plz/badge.svg?branch=master)](https://coveralls.io/github/m3brown/plz?branch=master)

A shell command to execute standard/repeatable commands in a git repo

### Installation

Install plz at the system level so that it only has to be installed once.

```bash
pip install plz-cmd

# sudo may be required on your machine
sudo pip install plz-cmd
```

It can also be installed inside a virtualenv.  However, this means you'll have
to install plz-cmd for each each virtualenv in use.

```bash
virtualenv venv
. venv/bin/activate

pip install plz-cmd
```

### Example

plz looks for a `plz.yaml` file either in the current directory or in the root
of the git repo you're currently in. This file can (and should) be checked into
version control.

For a plz.yaml file located in the git root directory, commands run will be
executed relative to that directory, not the current directory.

Suppose we have the following `plz.yaml` file:

```yaml
commands:
  run:
    cmd: ./manage.py runserver
  test:
    cmd:
    - ./manage.py test
    - yarn test
  setup:
    cmd:
    - poetry install
    - poetry run ./manage.py migrate
    - yarn install
  ls:
    cmd: ls
```

The following commands would be available:

```bash
plz run
plz test
plz setup
```

### Getting help

List all the available commands with:

```bash
plz
# or
plz help
```

Print the yaml schema for any defined command with `plz help <command>`:

```
> plz help test
[INFO] Using config: plz.yaml

test:
  cmd:
  - poetry run python -m pytest
```

### Environment variables

Environment variables can be set for an individual command or globally for all commands.

```yaml
# env variable for an individual command
commands:
  run:
    cmd: ./manage.py runserver
  test:
    cmd: ./manage.py test
    env:
      DJANGO_SETTINGS_MODULE: myapp.settings.test
```

```yaml
global_env:
  ACCESS_TOKEN: 12345
commands:
  run:
    cmd: ./manage.py runserver
```

### Globbing

plz supports asterisk expansion.  For example, the cmd `ls *.py` will work as expected.

### Runtime arguments

plz supports passing custom arguments when running the plz command. For example:

```
# bind to port 8001 instead of the default 8000
plz run 127.0.0.1:8001
```

Any passed arguments will be tested to see if they are file paths relative to
the current directory when running the command. Using this repo as an example:

```
bash$ ls .*.yaml
plz.yaml               .pre-commit-config.yaml

bash$ cd plz

bash$ plz ls ../.*.yaml

[INFO] Using config: /path/plz/plz.yaml

===============================================================================
Running command: ls
===============================================================================

plz.yaml
.pre-commit-config.yaml

[INFO] Process complete, return code: 0

bash$ plz ls __*.py

[INFO] Using config: /path/plz/plz.yaml

===============================================================================
Running command: ls
===============================================================================

plz/__init__.py

[INFO] Process complete, return code: 0
```

### Development

Setting up for development is easy when plz is already installed!

```
git clone https://github.com/m3brown/plz
cd plz
plz setup
plz test
```
