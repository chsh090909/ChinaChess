#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@contact:
@file:  demo.py
@time:  2018/12/5 21:11
"""

import socket
import uuid
import pygame
import sys
from pygame.locals import *
from settings import Settings

# print(socket.gethostname())
# print(socket.gethostbyname(socket.gethostname()))


def main():
    try:
        pygame.init()
        all_settings = Settings()
        displaySurf = pygame.display.set_mode((400, 400))
        pygame.display.set_caption(all_settings.game_title)
        displaySurf.fill(all_settings.bg_color)

        mouse_x, mouse_y = 0, 0
        mouse_clecked = False

        while True:
            for events in pygame.event.get():  # event handling loop
                if events.type == QUIT or (events.type == KEYUP and events.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if events.type == MOUSEBUTTONUP:
                    mouse_clecked = True
                    mouse_x, mouse_y = events.pos

            ## 画一个菜单栏
            # 设置顶级菜单字体和大小
            font_menu0 = pygame.font.Font(all_settings.font_style, 20)
            # 设置顶级菜单的文字内容和样式（默认是没有选中的时候）
            memu0_youxi = font_menu0.render("游戏", True, all_settings.BLACK, all_settings.bg_color)
            menu0_caozuo = font_menu0.render("操作", True, all_settings.BLACK, all_settings.bg_color)
            menu0_guanyu = font_menu0.render("关于", True, all_settings.BLACK, all_settings.bg_color)
            # "游戏"的二级菜单文字内容和样式
            youxi_server = font_menu0.render("服务器设置", True, all_settings.BLACK, all_settings.bg_color)
            youxi_client = font_menu0.render("连接其他服务器", True, all_settings.BLACK, all_settings.bg_color)
            youxi_start = font_menu0.render("游戏开始", True, all_settings.BLACK, all_settings.bg_color)
            youxi_quit = font_menu0.render("游戏结束", True, all_settings.BLACK, all_settings.bg_color)
            # 顶级菜单被选中
            if mouse_clecked:
                # print(mouse_x, mouse_y)
                if 5 < mouse_x < 50 and 5 < mouse_y < 25:
                    memu0_youxi = font_menu0.render("游戏", True, all_settings.RED, all_settings.GREEN)
                    pygame.draw.rect(displaySurf, all_settings.CYAN, (5, 26, 200, 105), 1)
                    displaySurf.blit(youxi_server, (8, 30))
                    displaySurf.blit(youxi_client, (8, 55))
                    displaySurf.blit(youxi_start, (8, 80))
                    displaySurf.blit(youxi_quit, (8, 105))

                elif 55 < mouse_x < 100 and 5 < mouse_y < 25:
                    menu0_caozuo = font_menu0.render("操作", True, all_settings.RED, all_settings.GREEN)
                    pygame.draw.rect(displaySurf, all_settings.CYAN, (55, 26, 200, 100), 1)

                elif 105 < mouse_x < 150 and 5 < mouse_y < 25:
                    menu0_guanyu = font_menu0.render("关于", True, all_settings.RED, all_settings.GREEN)

            # 设置顶级菜单的放置位置
            displaySurf.blit(memu0_youxi, (5, 5), (0, 0, 50, 25))
            displaySurf.blit(menu0_caozuo, (55, 5))
            displaySurf.blit(menu0_guanyu, (105, 5))

            pygame.display.update()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
