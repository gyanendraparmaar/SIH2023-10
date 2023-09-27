#!/usr/bin/python3
from sites import *

def sendRequest(jsonObject):
    api = ""
    pass


if __name__ == '__main__':
    toBeChecked = [EconomicTimes, DainikBhaskar]
    for site in toBeChecked:
        # objects = site.run()
        # map(sendRequest, objects)
        site().run()