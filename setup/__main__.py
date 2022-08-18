import sys
from lib import Install, Update, Deploy, Project


def run():
    for arg in sys.argv:
        if arg == "--deploy":
            Deploy()
        if arg == "--install":
            Install()
        if arg == "--update":
            Update()
        if arg == "--project":
            Project().details()
    exit()


if __name__ == '__main__':
    run()
