#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

class Settings(object):
    """
    配置文档
    """
    def __init__(self):
        # 初始化屏幕设置
        self.screen_width = 1000
        self.screen_height = 680
        self.bg_color = (239, 215, 189)
        self.game_title = '中国象棋'
        # 设置棋子大小和位置
        self.pieces_size = 100
        self.piece_first_x = 78
        self.piece_first_y = 77
        # 设置棋子的移动速度
        self.piece_move_speed = 30
        # 设置棋盘背景图（2选1），大小和位置
        self.chess_board = 'images/chessboard2.png'
        self.chess_board_size = (900, 500)
        self.chess_board_localxy = (50, 45)
        # 关联红黑棋子的棋面显示
        self.images_noun = '.png'
        self.pieces_color_red = 'images/pieces_front_red_'
        self.pieces_list_red = ('shuai', 'shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5')
        self.pieces_color_black = 'images/pieces_front_black_'
        self.pieces_list_black = ('jiang', 'shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5')
        # 设置棋子背面的图案
        self.pieces_back = 'images/pieces_back.png'
        # 设置屏幕刷新率
        self.FPS = 60
        # 设置颜色
        #                 R    G    B
        self.GRAY =     (100, 100, 100)
        self.NAVYBLUE = ( 60,  60, 100)
        self.WHITE =    (255, 255, 255)
        self.BLACK =    (  0,   0,   0)
        self.RED =      (255,   0,   0)
        self.GREEN =    (  0, 255,   0)
        self.BLUE =     (  0,   0, 255)
        self.YELLOW =   (255, 255,   0)
        self.ORANGE =   (255, 128,   0)
        self.PURPLE =   (255,   0, 255)
        self.CYAN =     (  0, 255, 255)
        # 设置玩家文字、字体和字号
        self.player1_name = '玩家1'
        self.player2_name = '玩家2'
        self.font_style = 'fonts/fanti_maokai.ttf'
        self.font_player_size = 40
        self.font_info_size = 26
        # 设置游戏结束图片和大小
        self.wonimage = 'images/win.gif'
        self.font_win_size = 50
        # 设置走棋步骤记录的文件名称
        self.infofilename = 'logs/chess.info'
        # 设置日志文件记录位置和名称
        self.logfilename = 'logs/chess_log.log'
        # 设置日志记录的格式、日志等级等信息
        self.sysoutformat = '%(name)s:%(funcName)s() - %(levelname)s --> %(message)s'
        self.filewriteformat = '%(asctime)s - %(name)s:%(funcName)s() - %(levelname)s --> %(message)s'
        self.sysoutlevel = logging.DEBUG
        self.filewritelevel = logging.INFO
        # 设置文件的游戏开头语
        self.beginstr = "本轮游戏开始！！！当前第1局！"
        # 设置文件的游戏结束语(总结游戏内容)
        self.endstr = ""
        # 设置背景音乐的音乐列表开头
        self.bgmusiclist = ['101.mid', '102.mid', '103.mid', '104.mid', '105.mid', '106.mid', '107.mid', '108.mid', '109.mid', '111.mid', '112.mid', '113.mid', '114.mid', '115.mid', '116.mid', '117.mid']
        # 设置各种动作音效
        self.cq = 'mids/chiqi.wav'
        self.cw = 'mids/cuowu.wav'
        self.hq = 'mids/huiqi.wav'
        self.xz = 'mids/xuanzhong.wav'
        self.zqwc = 'mids/zouqiwancheng.wav'
        # 设置帮助文档位置和名称
        self.helppdffile = 'help/教你如何玩.pdf'
