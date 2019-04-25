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

def main():
    list_x = (i * 100 + 78 for i in range(1, 9))
    list_y = (i * 100 + 42 for i in range(1, 5))
    print(list_x)
    print(list_y)
    print(179 in list_x)


sett = Settings()
str1 = 'bing'
count = -1

for qz in sett.pieces_list_red:
    count += 1
    if str1 == qz:
        break

print(count)

