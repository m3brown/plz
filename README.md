## plz

[![Build Status](https://travis-ci.org/m3brown/plz.svg?branch=master)](https://travis-ci.org/m3brown/plz)
[![Coverage Status](https://coveralls.io/repos/github/m3brown/plz/badge.svg?branch=master)](https://coveralls.io/github/m3brown/plz?branch=master)

A shell command to execute standard/repeatable commands in a git repo

### Installation

Install plz at the system level so that it only has to be installed once.

```bash
pip install plz

# sudo may be required on your machine
sudo pip install plz
```

It can also be installed inside a virtualenv.  However, this means you'll have to install
plz for each each virtualenv in use.

```bash
virtualenv venv
. venv/bin/activate

pip install plz
```

### Example

plz looks for a `plz.config` YAML file in the root of the git repo you're currently in.
This file can (and should) be checked into version control.

Note: this app does not currently support running plz.config files that are not inside a
git repo directory.

Suppose we have a `plz.config` file in the root of a git repo:

```yaml
- id: run
  name: runserver
  cmd: ./manage.py runserver
- id: test
  name: test code
  cmd:
  - ./manage.py test
  - yarn test
- id: setup
  name: setup apps
  cmd:
  - pipenv install
  - pipenv run ./manage.py migrate
  - yarn install
```

The following commands would be available:

```bash
plz run
plz test
plz setup
```
