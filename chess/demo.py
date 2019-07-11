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
import re

blacklist = ['pao1', 'xiang1', 'ma2', 'ju1', 'zu1']
for i in range(len(blacklist)):
    if blacklist[i] in ['shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2']:
        print('in')
    else:
        print('out')