#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@contact:
@file:  demo.py
@time:  2018/12/5 21:11
"""

import pygame, sys, time
from pygame.locals import *
from settings import Settings
import datetime

time1 = datetime.datetime.now()

time2 = time1 + datetime.timedelta(days=0, hours=0, minutes=5, seconds=2)

howlongdays = (time2 - time1).days
howlongseconds = (time2 - time1).seconds
print(time1)
print(time2)
print(type(howlongdays))
print(type(howlongseconds))