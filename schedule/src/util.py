__author__ = 'Vaibhav Kollipara'
__doc__ = """
Utility methods
"""

import datetime


def getDateFromString(str_date):
    # converts string date to date object
    (year, month, date) = str_date.split('-')
    (year, month, date) = (int(year), int(month), int(date))
    return datetime.date(year, month, date)


def getTimeFromString(str_time):
    # converts string time to time object
    (hours, mins, secs) = str_time.split(':')
    (hours, mins, secs) = (int(hours), int(mins), int(secs))
    return datetime.time(hours, mins, secs, 0)


def getTimeDifferenceInMinutes(startTime, endTime):
    # calculate total minutes between time interval
    return (datetime.datetime.combine(datetime.date.today(), endTime) - datetime.datetime.combine(datetime.date.today(), startTime)).total_seconds() / 60.0


def getDurationInMinutes(value, desc):
    # parse duration information in string to minutes(int)
    if desc == 'hour':
        if value == '1/2':
            return 0.5 * 60
        return float(value) * 60
    elif desc == 'minutes':
        return float(value)
