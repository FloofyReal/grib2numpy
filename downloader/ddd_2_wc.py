#!/usr/bin/env python

import calendar
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()

name_of_file = '64x64'
# name_of_file = '32x32'
# name_of_file = 'BIG'

name_of_grb = 'wc'
# temperature, humidity, cloud coverage

def retrieve_era5():
    """
    """
    yearStart = 2011
    yearEnd = 2013
    monthStart = 1
    monthEnd = 12
    for year in list(range(yearStart, yearEnd + 1)):
        for month in list(range(monthStart, monthEnd + 1)):
            # basic
            startDate = '%04d%02d%02d' % (year, month, 1)
            numberOfDays = calendar.monthrange(year, month)[1]
            lastDate = '%04d%02d%02d' % (year, month, numberOfDays)
            target = "./ECMWF/%s/europe_%s_%04d%02d.grb" % (name_of_file, name_of_grb, year, month)
            requestDates = (startDate + "/TO/" + lastDate)

            print('--- Request START ---')
            print(requestDates)
            print(target)
            print('--- Request END ---')
            era5_request(requestDates, target)

def era5_request(requestDates, target):
    """
    """
    
    server.retrieve({
        "class": "ea",
        "dataset": "era5",
        "date": requestDates,
        "expver": "1",
        "levelist": "137",
        "levtype": "ml",
        "param": "75",
        "stream": "oper",
        "grid": "0.3/0.3",
        "area": "58.8/8.1/40/27",
        "time": "00:00:00/01:00:00/02:00:00/03:00:00/04:00:00/05:00:00/06:00:00/07:00:00/08:00:00/09:00:00/10:00:00/11:00:00/12:00:00/13:00:00/14:00:00/15:00:00/16:00:00/17:00:00/18:00:00/19:00:00/20:00:00/21:00:00/22:00:00/23:00:00",
        "type": "an",
        "target": target,
    })


if __name__ == '__main__':
    retrieve_era5()

# NORTH, WEST, SOUTH, EAST
# BIG 
        # "area": "70/-15/30/30",
# 64x64
        # "area": "58.8/8.1/40/27",
# 32x32
        # "area": "54.3/13/45/22",

# PARAMETERS
# 75 - water content
# 76 - ice content
# 129 - geopotential
# 130 - temperature
# 131 - U component of wind
# 132 - V component of wind
# 133 - humidity
# 152 - log of surface pressure
# 164 - total cloud cover
# 248 - fraction of cloud cover
# 246 - specific cloud liquid water content
# 247 - specific cloud ice water content

# 24 STEPS OF TIME
# "time": "00:00:00/01:00:00/02:00:00/03:00:00/04:00:00/05:00:00/06:00:00/07:00:00/08:00:00/09:00:00/10:00:00/11:00:00/12:00:00/13:00:00/14:00:00/15:00:00/16:00:00/17:00:00/18:00:00/19:00:00/20:00:00/21:00:00/22:00:00/23:00:00",
