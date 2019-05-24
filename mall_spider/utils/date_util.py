# coding: utf-8
import datetime


def today():
    today = datetime.date.today()
    return today


def yesterday():
    today = datetime.date.today()
    return today - datetime.timedelta(days=1)


def day_before_yesterday():
    today = datetime.date.today()
    return today - datetime.timedelta(days=2)
