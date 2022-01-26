import sys

from workflow import Workflow3


def main(wf):
    pass


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
