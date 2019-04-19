#!#! /usr/bin/python

import calendar

def test_cal():

    cal = calendar.Calendar(6)
    print(cal.monthdayscalendar(2019, 3))
    print(len(cal.monthdayscalendar(2019, 3)))

test_cal()
