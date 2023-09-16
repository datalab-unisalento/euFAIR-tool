import datetime

from utility import constants, bcolors
import importlib
from log import log


def myprint(text, color=bcolors.bcolors.ENDC, to_log=1):
    if to_log:
        log.log(str(datetime.datetime.now()) + ': ' + text)
    lun = len(text)
    border = int((constants.constants.STR_LUN - lun) / 2)

    print(color + '-' * border + text + '-' * border + bcolors.bcolors.ENDC)


def aline(color=bcolors.bcolors.ENDC):
    print(color + "-" * constants.constants.STR_LUN)


def astar(color=bcolors.bcolors.ENDC):
    print(color + "*" * constants.constants.STR_LUN)
