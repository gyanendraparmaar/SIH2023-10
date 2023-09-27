from sites import *
import time

MIN = 10
toBeChecked = [EconomicTimes, DainikBhaskar]

def sendRequest(jsonObject):
    api = ""
    pass


if __name__ == '__main__':
    while True:
        for site in toBeChecked:
            print(site().run())
        time.sleep(MIN * 60)