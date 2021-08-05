import sys

from velox import Velox


if __name__ == '__main__':
    _, *args = sys.argv

    if len(args) > 1:
        print('Usage: velox [script]')
        sys.exit(64)
    elif len(args) == 1:
        Velox.run_file(args[0])
    else:
        Velox.run_prompt()
