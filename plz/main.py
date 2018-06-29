from .util import execute_from_config
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')

    args = parser.parse_args()

    execute_from_config(args.cmd)


if __name__ == '__main__':
    main()
