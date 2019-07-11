#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame
import random
import time
import os
from math import fabs

class GameFunctions(object):
    def __init__(self, all_settings):
        self.all_settings = all_settings

    def getRandomAllPieces(self):
        #获取所有的棋子位置，并随机打乱棋子分布，并返回
        pieces = []
        allPieces = []
        for piece_red in self.all_settings.pieces_list_red:
            pieces.append(['red_' + piece_red, self.all_settings.pieces_color_red + piece_red + self.all_settings.images_noun])
        for piece_black in self.all_settings.pieces_list_black:
            pieces.append(['black_' + piece_black, self.all_settings.pieces_color_black + piece_black + self.all_settings.images_noun])
        random.shuffle(pieces)

        for x in range(8):
            column = []
            for y in range(4):
                column.append(pieces[0])
                del pieces[0]
            allPieces.append(column)
        print('allPieces: %s' % allPieces)
        return allPieces

    def loadPieceBoard(self, displaySurf):
        #加载棋盘图片
        piece_board = pygame.image.load(self.all_settings.chess_board).convert_alpha()
        #piece_board = pygame.transform.smoothscale(piece_board, self.all_settings.chess_board_size)
        displaySurf.blit(piece_board, self.all_settings.chess_board_localxy)

    def loadPlayerMain(self, displaySurf, playerinfo):
        #加载玩家信息模块内容
        nowPlayer = playerinfo['nowPlayer']
        pieceColor = playerinfo['pieceColor']
        totalCount = playerinfo['totalCount']
        wonCount = playerinfo['wonCount']
        tieCount = playerinfo['tieCount']

        pygame.draw.rect(displaySurf, self.all_settings.RED, (0, 520, self.all_settings.screen_width, 1), 1)
        pygame.draw.rect(displaySurf, self.all_settings.RED, (499, 520, 1, self.all_settings.screen_height - 520), 1)

        font_player = pygame.font.Font(self.all_settings.font_style, self.all_settings.font_player_size)
        font_info = pygame.font.Font(self.all_settings.font_style, self.all_settings.font_info_size)
        font_player.set_underline(True)

        if nowPlayer == self.all_settings.player1_name:
            font_player1_status = font_info.render('状态: 正在走棋...', True, self.all_settings.GREEN)
            font_player2_status = font_info.render('状态: 走棋完毕!', True, self.all_settings.GRAY)
            font_player1 = font_player.render(self.all_settings.player1_name, True, self.all_settings.BLACK, self.all_settings.GREEN)
            font_player2 = font_player.render(self.all_settings.player2_name, True, self.all_settings.BLACK)
        else:
            font_player1_status = font_info.render('状态: 走棋完毕!', True, self.all_settings.GRAY)
            font_player2_status = font_info.render('状态: 正在走棋...', True, self.all_settings.GREEN)
            font_player1 = font_player.render(self.all_settings.player1_name, True, self.all_settings.BLACK)
            font_player2 = font_player.render(self.all_settings.player2_name, True, self.all_settings.BLACK, self.all_settings.GREEN)
        if pieceColor == 'red':
            font_player1_rOb = font_info.render('执方: 红方', True, self.all_settings.RED)
            font_player2_rOb = font_info.render('执方: 黑方', True, self.all_settings.BLACK)
        elif pieceColor == 'black':
            font_player1_rOb = font_info.render('执方: 黑方', True, self.all_settings.BLACK)
            font_player2_rOb = font_info.render('执方: 红方', True, self.all_settings.RED)
        else:
            font_player1_rOb = font_info.render('执方:  ', True, self.all_settings.GRAY)
            font_player2_rOb = font_info.render('执方:  ', True, self.all_settings.GRAY)

        blit_y = (self.all_settings.screen_height - 520 - self.all_settings.font_player_size) / 2 + 520
        displaySurf.blit(font_player1, (50, blit_y))
        displaySurf.blit(font_player2, (550, blit_y))

        font_player1_winCount = font_info.render('胜利: ' + str(wonCount) + ' 局', True, self.all_settings.GRAY)
        font_player1_tieCount = font_info.render('打平: ' + str(tieCount) + ' 局', True, self.all_settings.GRAY)
        font_player2_winCount = font_info.render('胜利: ' + str(totalCount-wonCount-tieCount) + ' 局', True, self.all_settings.GRAY)
        font_player2_tieCount = font_info.render('打平: ' + str(tieCount) + ' 局', True, self.all_settings.GRAY)
        blit_y1 = (self.all_settings.screen_height - 520 - self.all_settings.font_info_size) / 2 + 520
        displaySurf.blit(font_player1_rOb, (230, blit_y1 - self.all_settings.font_info_size * 2 - 10))
        displaySurf.blit(font_player1_status, (230, blit_y1 - self.all_settings.font_info_size))
        displaySurf.blit(font_player1_winCount, (230, blit_y1 + 10))
        displaySurf.blit(font_player1_tieCount, (230, blit_y1 + self.all_settings.font_info_size + 10 + 10))
        displaySurf.blit(font_player2_rOb, (730, blit_y1 - self.all_settings.font_info_size * 2 - 10))
        displaySurf.blit(font_player2_status, (730, blit_y1 - self.all_settings.font_info_size))
        displaySurf.blit(font_player2_winCount, (730, blit_y1 + 10))
        displaySurf.blit(font_player2_tieCount, (730, blit_y1 + self.all_settings.font_info_size + 10 + 10))

    def loadPiecesBack(self, displaySurf, box_x, box_y, revealedBoxes, all_pieces, **kwargs):
        #加载棋子背面的图片，以及鼠标悬停的选中效果
        for x in range(8):
            for y in range(4):
                if revealedBoxes[x][y] == False:
                    image_back = pygame.image.load(self.all_settings.pieces_back).convert_alpha()
                    image_back = pygame.transform.smoothscale(image_back, (self.all_settings.pieces_size, self.all_settings.pieces_size))
                    displaySurf.blit(image_back, (self.all_settings.piece_first_x + x * 100, self.all_settings.piece_first_y + y * 100))
                elif revealedBoxes[x][y] == True:
                    piece_image = all_pieces[x][y][1]
                    image = pygame.image.load(piece_image).convert_alpha()
                    image = pygame.transform.smoothscale(image, (self.all_settings.pieces_size, self.all_settings.pieces_size))
                    displaySurf.blit(image, self.getBoxXYFromNumXY(x, y))
                    firstSelection = kwargs.get('firstSelection', None)
                    if firstSelection != None:
                        box_numX = firstSelection[0]
                        box_numY = firstSelection[1]
                        box1_x, box1_y = self.getBoxXYFromNumXY(box_numX, box_numY)
                        self.drawHighlightPiece(displaySurf, box1_x, box1_y)
                elif revealedBoxes[x][y] == None:
                    pass
                if box_x != None and box_y != None:
                    box_local_X, box_local_Y = self.getBoxNum(box_x, box_y)
                    if box_local_X == x and box_local_Y == y:
                        if revealedBoxes[x][y] != None:
                            self.drawHighlightPiece(displaySurf, box_x, box_y)

    def getPiecesStatus(self, bool):
        # 获取棋盘上每个方格上的内容
        # #bool将会有3种状态，分别是true，false，以及None
        #true表示棋子已打开，false表示棋子未打开，None表示当前格子无棋子
        revealedBoxes = []
        for x in range(8):
            revealedBoxes.append([bool] * 4)
        print('revealedBoxes: %s' % revealedBoxes)
        return revealedBoxes

    def drawHighlightPiece(self, displaySurf, box_x, box_y):
        #画一个高亮的圆，表示鼠标悬停时选中
        pygame.draw.circle(displaySurf, self.all_settings.BLUE, (box_x + 50, box_y + 50), 46, 3)

    def getBoxXY(self, mouse_x, mouse_y):
        #根据鼠标的xy值，获取当前在那个棋子上面，返回棋子所在方格的原点坐标
        min_point_x = self.all_settings.piece_first_x
        max_point_x = self.all_settings.piece_first_x + 8 * 100
        min_point_y = self.all_settings.piece_first_y
        max_point_y = self.all_settings.piece_first_y + 4 * 100
        if (min_point_x < mouse_x < max_point_x) and (min_point_y < mouse_y < max_point_y):
            # mouse_x_not = (178, 278, 378, 478, 578, 678, 778)
            # mouse_y_not = (142, 242, 342)
            mouse_x_not = (i * 100 + min_point_x for i in range(1, 9))
            mouse_y_not = (i * 100 + min_point_y for i in range(1, 5))
            if (mouse_x not in mouse_x_not) and (mouse_y not in mouse_y_not):
                box_x = int((mouse_x - min_point_x) / 100) * 100 + min_point_x
                box_y = int((mouse_y - min_point_y) / 100) * 100 + min_point_y
                return (box_x, box_y)
        return (None, None)

    def getBoxNum(self, box_x, box_y):
        #根据box_x和box_y的值，返回当前box的序号
        box_numX = int((box_x - self.all_settings.piece_first_x) / 100)
        box_numY = int((box_y - self.all_settings.piece_first_y) / 100)
        return (box_numX, box_numY)

    def getBoxXYFromNumXY(self, box_numX, box_numY):
        # 根据box的序号返回box_x和box_y的值
        box_x = int(box_numX) * 100 + self.all_settings.piece_first_x
        box_y = int(box_numY) * 100 + self.all_settings.piece_first_y
        return (box_x, box_y)

    def startGame(self, playerinfo):
        #游戏开始时加载的内容
        all_pieces = self.getRandomAllPieces()
        revealedBoxes = self.getPiecesStatus(False)
        mouse_clecked_count = 0
        player1_checked_count = 0
        player2_checked_count = 0
        playerinfo['nowPlayer'] = self.all_settings.player1_name
        playerinfo['pieceColor'] = 'None'
        print('startGame==>GameOver！游戏重置！')
        return (all_pieces, revealedBoxes, mouse_clecked_count, player1_checked_count, player2_checked_count, playerinfo)

    def hasWon(self, displaySurf, revealedBoxes, all_pieces, playerinfo):
        # 判断游戏结束条件：
        # 全部为一方颜色的棋子，为胜利
        # 棋盘全部清空或者留下不能相互吃掉的棋子，为平局
        noneCount = 0
        redCount = 0
        blackCount = 0
        falseCount = 0

        totalCount = playerinfo['totalCount']
        wonCount = playerinfo['wonCount']
        tieCount = playerinfo['tieCount']

        for x in range(8):
            for y in range(4):
                if revealedBoxes[x][y] == None:
                    noneCount += 1
                elif revealedBoxes[x][y] == True:
                    piece = all_pieces[x][y][0]
                    piecelist = piece.split('_')
                    piece_color = piecelist[0]
                    if 'red' == piece_color:
                        redCount += 1
                    elif 'black' == piece_color:
                        blackCount += 1
                elif revealedBoxes[x][y] == False:
                    falseCount += 1
        print('======================================================')
        print('hasWon==>noneCount: %d' % noneCount)
        print('hasWon==>redCount: %d' % redCount)
        print('hasWon==>blackCount: %d' % blackCount)
        print('hasWon==>falseCount: %d' % falseCount)
        print('======================================================')
        if noneCount == 32:
            self.tieWon(totalCount, tieCount, playerinfo)
            print('hasWon==>noneCount == 32==>playerinfo: %s' % playerinfo)
            self.drawWon(displaySurf, playerinfo, '平局')
            return (True, '平局')
        elif falseCount == 0:
            if noneCount != 32:
                if redCount == 0:
                    if 'red' == playerinfo['pieceColor']:
                        # playerinfo['wonPlayer'] = self.all_settings.player2_name
                        self.player2Won(totalCount, playerinfo)
                        print('hasWon==>redCount == 0(red == playerinfo[pieceColor])==>playerinfo: %s' % playerinfo)
                        self.drawWon(displaySurf, playerinfo, self.all_settings.player2_name + '胜')
                        return (True, self.all_settings.player2_name + '(黑方)胜')
                    elif 'black' == playerinfo['pieceColor']:
                        # playerinfo['wonPlayer'] = self.all_settings.player1_name
                        self.player1Won(totalCount, wonCount, playerinfo)
                        print('hasWon==>redCount == 0(black == playerinfo[pieceColor])==>playerinfo: %s' % playerinfo)
                        self.drawWon(displaySurf, playerinfo, self.all_settings.player1_name + '胜')
                        return (True, self.all_settings.player1_name + '(黑方)胜')
                elif blackCount == 0:
                    if 'red' == playerinfo['pieceColor']:
                        # playerinfo['wonPlayer'] = self.all_settings.player1_name
                        self.player1Won(totalCount, wonCount, playerinfo)
                        print('hasWon==>blackCount == 0(red == playerinfo[pieceColor])==>playerinfo: %s' % playerinfo)
                        self.drawWon(displaySurf, playerinfo, self.all_settings.player1_name + '胜')
                        return (True, self.all_settings.player1_name + '(红方)胜')
                    elif 'black' == playerinfo['pieceColor']:
                        # playerinfo['wonPlayer'] = self.all_settings.player2_name
                        self.player2Won(totalCount, playerinfo)
                        print('hasWon==>blackCount == 0(black == playerinfo[pieceColor])==>playerinfo: %s' % playerinfo)
                        self.drawWon(displaySurf, playerinfo, self.all_settings.player2_name + '胜')
                        return (True, self.all_settings.player2_name + '(红方)胜')
                elif redCount == 1 and blackCount == 1:
                    newlist = []
                    for x in range(8):
                        for y in range(4):
                            if revealedBoxes[x][y] == True:
                                newlist.append([x, y])
                    list1 = all_pieces[newlist[0][0]][newlist[0][1]][0]
                    list2 = all_pieces[newlist[1][0]][newlist[1][1]][0]
                    list1_color = list1.split('_')[0]
                    list1_name = list1.split('_')[1]
                    list2_color = list2.split('_')[0]
                    list2_name = list2.split('_')[1]
                    if (list1_color == 'red' and list1_name == 'shuai') and (list2_color == 'black' and list2_name in ['jiang', 'pao1', 'pao2']):
                        self.tieWon(totalCount, tieCount, playerinfo)
                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                        self.drawWon(displaySurf, playerinfo, '平局')
                        return (True, '平局')
                    elif (list1_color == 'black' and list1_name == 'jiang') and (list2_color == 'red' and list2_name in ['shuai', 'pao1', 'pao2']):
                        self.tieWon(totalCount, tieCount, playerinfo)
                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                        self.drawWon(displaySurf, playerinfo, '平局')
                        return (True, '平局')
                    elif (list1_color == 'red' and list1_name in ['pao1', 'pao2']) and (list2_color == 'black' and list2_name in ['pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5']):
                        self.tieWon(totalCount, tieCount, playerinfo)
                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                        self.drawWon(displaySurf, playerinfo, '平局')
                        return (True, '平局')
                    elif (list1_color == 'black' and list1_name in ['pao1', 'pao2']) and (list2_color == 'red' and list2_name in ['pao1', 'pao2', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']):
                        self.tieWon(totalCount, tieCount, playerinfo)
                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                        self.drawWon(displaySurf, playerinfo, '平局')
                        return (True, '平局')
                    else:
                        if fabs(newlist[0][0] - newlist[1][0]) == 1 and fabs(newlist[0][1] - newlist[1][1]) == 1:
                            nowPlayer = playerinfo['nowPlayer']
                            player1PieceColor = playerinfo['pieceColor']
                            player2PieceColor = 'red' if player1PieceColor == 'black' else 'black'
                            red_index = black_index = -1
                            if list1_color == 'red':
                                for qz in self.all_settings.pieces_list_red:
                                    red_index += 1
                                    if list1_name == qz:
                                        break
                            elif list2_color == 'red':
                                for qz in self.all_settings.pieces_list_red:
                                    red_index += 1
                                    if list2_name == qz:
                                        break
                            if list1_color == 'black':
                                for qz in self.all_settings.pieces_list_black:
                                    black_index += 1
                                    if list1_name == qz:
                                        break
                            elif list2_color == 'black':
                                for qz in self.all_settings.pieces_list_black:
                                    black_index += 1
                                    if list2_name == qz:
                                        break
                            if red_index < black_index:
                                if black_index in [11, 12, 13, 14, 15] and red_index == 0:
                                    if nowPlayer == self.all_settings.player1_name and player1PieceColor == 'black':
                                        self.tieWon(totalCount, tieCount, playerinfo)
                                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                        self.drawWon(displaySurf, playerinfo, '平局')
                                        return (True, '平局')
                                    elif nowPlayer == self.all_settings.player2_name and player2PieceColor == 'black':
                                        self.tieWon(totalCount, tieCount, playerinfo)
                                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                        self.drawWon(displaySurf, playerinfo, '平局')
                                        return (True, '平局')
                                elif nowPlayer == self.all_settings.player1_name and player1PieceColor == 'red':
                                    self.tieWon(totalCount, tieCount, playerinfo)
                                    print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                    self.drawWon(displaySurf, playerinfo, '平局')
                                    return (True, '平局')
                                elif nowPlayer == self.all_settings.player2_name and player2PieceColor == 'red':
                                    self.tieWon(totalCount, tieCount, playerinfo)
                                    print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                    self.drawWon(displaySurf, playerinfo, '平局')
                                    return (True, '平局')
                            elif red_index > black_index:
                                if red_index in [11, 12, 13, 14, 15] and black_index == 0:
                                    if nowPlayer == self.all_settings.player1_name and player1PieceColor == 'red':
                                        self.tieWon(totalCount, tieCount, playerinfo)
                                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                        self.drawWon(displaySurf, playerinfo, '平局')
                                        return (True, '平局')
                                    elif nowPlayer == self.all_settings.player2_name and player2PieceColor == 'red':
                                        self.tieWon(totalCount, tieCount, playerinfo)
                                        print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                        self.drawWon(displaySurf, playerinfo, '平局')
                                        return (True, '平局')
                                elif nowPlayer == self.all_settings.player1_name and player1PieceColor == 'black':
                                    self.tieWon(totalCount, tieCount, playerinfo)
                                    print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                    self.drawWon(displaySurf, playerinfo, '平局')
                                    return (True, '平局')
                                elif nowPlayer == self.all_settings.player2_name and player2PieceColor == 'black':
                                    self.tieWon(totalCount, tieCount, playerinfo)
                                    print('hasWon==>red == %s and black == %s ==>playerinfo: %s' % (list1, list2, playerinfo))
                                    self.drawWon(displaySurf, playerinfo, '平局')
                                    return (True, '平局')
                # 以下为2019-07-11增加的内容
                elif redCount == 1 and blackCount > 1:
                    redlist = []
                    blacklist = []
                    for x in range(8):
                        for y in range(4):
                            if revealedBoxes[x][y] == True:
                                qz = all_pieces[x][y][0]
                                qzlist = qz.split('_')
                                qz_color = qzlist[0]
                                qz_name = qzlist[1]
                                if qz_color == 'red':
                                    redlist.append(qz_name)
                                else:
                                    blacklist.append(qz_name)
                    blacknamecount = 0
                    if redlist[0] == 'shuai':
                        for i in range(len(blacklist)):
                            if blacklist[i] in ['shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2']:
                                blacknamecount += 1
                            else:
                                break
                        if blacknamecount == len(blacklist):
                            return (True, '平局')
                    elif redlist[0] in ['shi1', 'shi2']:
                        for i in range(len(blacklist)):
                            if blacklist[i] in ['xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5']:
                                blacknamecount += 1
                            else:
                                break
                        if blacknamecount == len(blacklist):
                            return (True, '平局')
                    elif redlist[0] in ['xiang1', 'xiang2']:
                        for i in range(len(blacklist)):
                            if blacklist[i] in ['ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5']:
                                blacknamecount += 1
                            else:
                                break
                        if blacknamecount == len(blacklist):
                            return (True, '平局')
                    elif redlist[0] in ['ma1', 'ma2']:
                        for i in range(len(blacklist)):
                            if blacklist[i] in ['ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5']:
                                blacknamecount += 1
                            else:
                                break
                        if blacknamecount == len(blacklist):
                            return (True, '平局')
                    elif redlist[0] in ['ju1', 'ju2']:
                        for i in range(len(blacklist)):
                            if blacklist[i] in ['pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5']:
                                blacknamecount += 1
                            else:
                                break
                        if blacknamecount == len(blacklist):
                            return (True, '平局')
                    elif redlist[0] in ['pao1', 'pao2']:
                        for i in range(len(blacklist)):
                            if blacklist[i] in ['zu1', 'zu2', 'zu3', 'zu4', 'zu5']:
                                blacknamecount += 1
                            else:
                                break
                        if blacknamecount == len(blacklist):
                            return (True, '平局')
                elif blackCount == 1 and redCount > 1:
                    redlist = []
                    blacklist = []
                    for x in range(8):
                        for y in range(4):
                            if revealedBoxes[x][y] == True:
                                qz = all_pieces[x][y][0]
                                qzlist = qz.split('_')
                                qz_color = qzlist[0]
                                qz_name = qzlist[1]
                                if qz_color == 'red':
                                    redlist.append(qz_name)
                                else:
                                    blacklist.append(qz_name)
                    rednamecount = 0
                    if blacklist[0] == 'jiang':
                        for i in range(len(redlist)):
                            if redlist[i] in ['shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2']:
                                rednamecount += 1
                            else:
                                break
                        if rednamecount == len(redlist):
                            return (True, '平局')
                    elif blacklist[0] in ['shi1', 'shi2']:
                        for i in range(len(redlist)):
                            if redlist[i] in ['xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                                rednamecount += 1
                            else:
                                break
                        if rednamecount == len(redlist):
                            return (True, '平局')
                    elif blacklist[0] in ['xiang1', 'xiang2']:
                        for i in range(len(redlist)):
                            if redlist[i] in ['ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                                rednamecount += 1
                            else:
                                break
                        if rednamecount == len(redlist):
                            return (True, '平局')
                    elif blacklist[0] in ['ma1', 'ma2']:
                        for i in range(len(redlist)):
                            if redlist[i] in ['ju1', 'ju2', 'pao1', 'pao2', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                                rednamecount += 1
                            else:
                                break
                        if rednamecount == len(redlist):
                            return (True, '平局')
                    elif blacklist[0] in ['ju1', 'ju2']:
                        for i in range(len(redlist)):
                            if redlist[i] in ['pao1', 'pao2', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                                rednamecount += 1
                            else:
                                break
                        if rednamecount == len(redlist):
                            return (True, '平局')
                    elif blacklist[0] in ['pao1', 'pao2']:
                        for i in range(len(redlist)):
                            if redlist[i] in ['bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                                rednamecount += 1
                            else:
                                break
                        if rednamecount == len(redlist):
                            return (True, '平局')
        return(False, '')

    def player1Won(self, totalCount, wonCount, playerinfo):
        totalCount += 1
        wonCount += 1
        playerinfo['totalCount'] = totalCount
        playerinfo['wonCount'] = wonCount
        print('playerinfo[wonPlayer] = self.all_settings.player1_name')
    def player2Won(self, totalCount, playerinfo):
        totalCount += 1
        playerinfo['totalCount'] = totalCount
        print('playerinfo[wonPlayer] = self.all_settings.player2_name')
    def tieWon(self, totalCount, tieCount, playerinfo):
        totalCount += 1
        tieCount += 1
        playerinfo['totalCount'] = totalCount
        playerinfo['tieCount'] = tieCount

    def drawWon(self, displaySurf, playerinfo, wonPlayer):
        #当一轮游戏结束后加载游戏胜负动画和消息内容
        wonimage = pygame.image.load(self.all_settings.wonimage).convert_alpha()
        # image_back = pygame.transform.smoothscale(wonimage, (self.all_settings.pieces_size, self.all_settings.pieces_size))
        font_win = pygame.font.Font(self.all_settings.font_style, self.all_settings.font_win_size)
        font_str = pygame.font.Font(self.all_settings.font_style, self.all_settings.font_info_size)
        color1 = self.all_settings.RED
        color2 = self.all_settings.GREEN

        for i in range(10):
            color1, color2 = color2, color1
            font_win_status = font_win.render(wonPlayer, True, color1)
            displaySurf.fill(self.all_settings.bg_color)
            displaySurf.blit(wonimage, (400, 130))
            displaySurf.blit(font_win_status, (400, 280))
            if i >= 5:
                font_str_status = font_str.render(str(10 - i) + '秒之后开始下一局！', True, self.all_settings.GRAY)
                displaySurf.blit(font_str_status, (400, 340))
            self.loadPlayerMain(displaySurf, playerinfo)

            pygame.display.update()
            pygame.time.wait(1000)

    def drawBoard(self, displaySurf, box_x, box_y, revealedBoxes, playerinfo, all_pieces, **kwargs):
        # 加载初始化画布内容，包括棋盘和玩家参数信息等
        self.loadPieceBoard(displaySurf)
        self.loadPiecesBack(displaySurf, box_x, box_y, revealedBoxes, all_pieces, **kwargs)
        self.loadPlayerMain(displaySurf, playerinfo)

    def pieceVSpiece(self, displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces):
        # 核心部分：两个棋子之间互相比较
        fs_x = firstSelection[0]
        fs_y = firstSelection[1]
        ss_x = secSelection[0]
        ss_y = secSelection[1]
        boxss_x, boxss_y = self.getBoxXYFromNumXY(ss_x, ss_y)
        pieceMoveCount = 0

        if revealedBoxes[ss_x][ss_y] == True:
            if secSelection[2] != firstSelection[2]:
                if firstSelection[3] in ['pao1', 'pao2']:
                    # '炮'的吃法：
                    # 1、中间必须有且只有一个棋子，才能吃到对方棋子，没有距离限制；
                    # 2、炮没有大小吃法限制，上到将，下到卒都可以吃，如果炮吃到炮，则一起吃掉；
                    # 3、炮移动只能相邻的格子移动，不能跳着移动；
                    image = pygame.image.load(firstSelection[4]).convert_alpha()
                    image = pygame.transform.smoothscale(image, (self.all_settings.pieces_size, self.all_settings.pieces_size))
                    if fs_y == ss_y and int(fabs(ss_x - fs_x)) > 1:
                        #横排比较
                        beginmove_x = fs_x * 100 + 78
                        count_num = 0
                        increment = 1
                        if ss_x < fs_x:
                            increment = -1
                            self.all_settings.piece_move_speed = -self.all_settings.piece_move_speed
                        for i in range(fs_x + increment, ss_x, increment):
                            if revealedBoxes[i][fs_y] != None:
                                count_num += 1
                        if count_num == 1:
                            # 成功确定，炮到目标棋子之间有且只有一个棋子
                            if secSelection[3] not in ['pao1', 'pao2']:
                                revealedBoxes[fs_x][fs_y] = None
                                all_pieces[fs_x][fs_y] = [None, None]
                                for move_x in range(beginmove_x, boxss_x + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                                    displaySurf.blit(image, (move_x, boxss_y))
                                all_pieces[ss_x][ss_y] = [firstSelection[2] + '_' + firstSelection[3], firstSelection[4]]
                                pieceMoveCount += 1
                            elif secSelection[3] in ['pao1', 'pao2']:
                                revealedBoxes[fs_x][fs_y] = None
                                revealedBoxes[ss_x][ss_y] = None
                                all_pieces[fs_x][fs_y] = [None, None]
                                for move_x in range(beginmove_x, boxss_x + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                                    displaySurf.blit(image, (move_x, boxss_y))
                                all_pieces[ss_x][ss_y] = [None, None]
                                pieceMoveCount += 1
                    if fs_x == ss_x and int(fabs(ss_y - fs_y)) > 1:
                        #竖排比较
                        beginmove_y = fs_y * 100 + 42
                        count_num = 0
                        increment = 1
                        if ss_y < fs_y:
                            increment = -1
                            self.all_settings.piece_move_speed = -self.all_settings.piece_move_speed
                        for i in range(fs_y + increment, ss_y, increment):
                            if revealedBoxes[fs_x][i] != None:
                                count_num += 1
                        if count_num == 1:
                            # 成功确定，炮到目标棋子之间有且只有一个棋子
                            if secSelection[3] not in ['pao1', 'pao2']:
                                revealedBoxes[fs_x][fs_y] = None
                                all_pieces[fs_x][fs_y] = [None, None]
                                for move_y in range(beginmove_y, boxss_y + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                                    displaySurf.blit(image, (boxss_x, move_y))
                                all_pieces[ss_x][ss_y] = [firstSelection[2] + '_' + firstSelection[3], firstSelection[4]]
                                pieceMoveCount += 1
                            elif secSelection[3] in ['pao1', 'pao2']:
                                revealedBoxes[fs_x][fs_y] = None
                                revealedBoxes[ss_x][ss_y] = None
                                all_pieces[fs_x][fs_y] = [None, None]
                                for move_y in range(beginmove_y, boxss_y + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                                    displaySurf.blit(image, (boxss_x, move_y))
                                all_pieces[ss_x][ss_y] = [None, None]
                                pieceMoveCount += 1
                else:
                    # 其他的棋子的吃法：
                    # 1、大吃小（将（帅）>士>（象）相>马>车>炮和卒（兵）），两两相同则一起吃掉；
                    # 2、炮和卒（兵）、炮和将（帅）相互不能吃，任何棋子都可以吃炮，除了卒（兵）、将（帅）外；
                    # 3、任何棋子都可以吃卒（兵），而卒（兵）只吃对方的帅（将）；
                    # 4、棋子只能相邻的吃，而且一次只能走一步，吃一个棋子，炮除外
                    image = pygame.image.load(firstSelection[4]).convert_alpha()
                    image = pygame.transform.smoothscale(image, (self.all_settings.pieces_size, self.all_settings.pieces_size))
                    if fs_y == ss_y and int(fabs(ss_x - fs_x)) == 1:
                        beginmove_x = fs_x * 100 + 78
                        if firstSelection[3] in ['jiang', 'shuai']:
                            pieceMoveCount = self.pieceVSpieceMoveX(['jiang', 'shuai'],
                                                                    ['shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                        elif firstSelection[3] in ['shi1', 'shi2']:
                            pieceMoveCount = self.pieceVSpieceMoveX(['shi1', 'shi2'],
                                                                    ['xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2',
                                                                     'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                        elif firstSelection[3] in ['xiang1', 'xiang2']:
                            pieceMoveCount = self.pieceVSpieceMoveX(['xiang1', 'xiang2'],
                                                                    ['ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                        elif firstSelection[3] in ['ma1', 'ma2']:
                            pieceMoveCount = self.pieceVSpieceMoveX(['ma1', 'ma2'],
                                                                    ['ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                        elif firstSelection[3] in ['ju1', 'ju2']:
                            pieceMoveCount = self.pieceVSpieceMoveX(['ju1', 'ju2'],
                                                                    ['pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                        elif firstSelection[3] in ['zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                            pieceMoveCount = self.pieceVSpieceMoveX(['zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    ['jiang', 'shuai'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                    if fs_x == ss_x and int(fabs(ss_y - fs_y)) == 1:
                        beginmove_y = fs_y * 100 + 42
                        if firstSelection[3] in ['jiang', 'shuai']:
                            pieceMoveCount = self.pieceVSpieceMoveY(['jiang', 'shuai'],
                                                                    ['shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
                        elif firstSelection[3] in ['shi1', 'shi2']:
                            pieceMoveCount = self.pieceVSpieceMoveY(['shi1', 'shi2'],
                                                                    ['xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2',
                                                                     'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
                        elif firstSelection[3] in ['xiang1', 'xiang2']:
                            pieceMoveCount = self.pieceVSpieceMoveY(['xiang1', 'xiang2'],
                                                                    ['ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
                        elif firstSelection[3] in ['ma1', 'ma2']:
                            pieceMoveCount = self.pieceVSpieceMoveY(['ma1', 'ma2'],
                                                                    ['ju1', 'ju2', 'pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
                        elif firstSelection[3] in ['ju1', 'ju2']:
                            pieceMoveCount = self.pieceVSpieceMoveY(['ju1', 'ju2'],
                                                                    ['pao1', 'pao2', 'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
                        elif firstSelection[3] in ['zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5']:
                            pieceMoveCount = self.pieceVSpieceMoveY(['zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                                                    ['jiang', 'shuai'],
                                                                    displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
        elif revealedBoxes[ss_x][ss_y] == False:
            pass
        elif revealedBoxes[ss_x][ss_y] == None:
            image = pygame.image.load(firstSelection[4]).convert_alpha()
            image = pygame.transform.smoothscale(image, (self.all_settings.pieces_size, self.all_settings.pieces_size))
            if fs_y == ss_y and int(fabs(ss_x - fs_x)) == 1:
                beginmove_x = fs_x * 100 + 78
                pieceMoveCount = self.pieceVSpieceMoveX(['jiang', 'shuai', 'shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2',
                                        'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                        [None],displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image)
                revealedBoxes[ss_x][ss_y] = True
            if fs_x == ss_x and int(fabs(ss_y - fs_y)) == 1:
                beginmove_y = fs_y * 100 + 42
                pieceMoveCount = self.pieceVSpieceMoveY(['jiang', 'shuai', 'shi1', 'shi2', 'xiang1', 'xiang2', 'ma1', 'ma2', 'ju1', 'ju2', 'pao1', 'pao2',
                                        'zu1', 'zu2', 'zu3', 'zu4', 'zu5', 'bing1', 'bing2', 'bing3', 'bing4', 'bing5'],
                                        [None], displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image)
                revealedBoxes[ss_x][ss_y] = True
        return (pieceMoveCount, all_pieces, revealedBoxes)

    def pieceVSpieceMoveX(self, sourcepiecelist, piecelist, displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_x, image):
        fs_x = firstSelection[0]
        fs_y = firstSelection[1]
        ss_x = secSelection[0]
        ss_y = secSelection[1]
        mouse_clecked_count = 0
        box_x, box_y = self.getBoxXYFromNumXY(ss_x, ss_y)
        if ss_x < fs_x:
            self.all_settings.piece_move_speed = -self.all_settings.piece_move_speed
        if firstSelection[3] in sourcepiecelist:
            if secSelection[3] in piecelist:
                revealedBoxes[fs_x][fs_y] = None
                all_pieces[fs_x][fs_y] = [None, None]
                for move_x in range(beginmove_x, box_x + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                    displaySurf.blit(image, (move_x, box_y))
                all_pieces[ss_x][ss_y] = [firstSelection[2] + '_' + firstSelection[3], firstSelection[4]]
                mouse_clecked_count += 1
            elif secSelection[3] in sourcepiecelist:
                revealedBoxes[fs_x][fs_y] = None
                revealedBoxes[ss_x][ss_y] = None
                all_pieces[fs_x][fs_y] = [None, None]
                for move_x in range(beginmove_x, box_x + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                    displaySurf.blit(image, (move_x, box_y))
                all_pieces[ss_x][ss_y] = [None, None]
                mouse_clecked_count += 1
        return mouse_clecked_count

    def pieceVSpieceMoveY(self, sourcepiecelist, piecelist, displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces, beginmove_y, image):
        fs_x = firstSelection[0]
        fs_y = firstSelection[1]
        ss_x = secSelection[0]
        ss_y = secSelection[1]
        mouse_clecked_count = 0
        box_x, box_y = self.getBoxXYFromNumXY(ss_x, ss_y)
        if ss_y < fs_y:
            self.all_settings.piece_move_speed = -self.all_settings.piece_move_speed
        if firstSelection[3] in sourcepiecelist:
            if secSelection[3] in piecelist:
                revealedBoxes[fs_x][fs_y] = None
                all_pieces[fs_x][fs_y] = [None, None]
                for move_y in range(beginmove_y, box_y + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                    displaySurf.blit(image, (box_x, move_y))
                all_pieces[ss_x][ss_y] = [firstSelection[2] + '_' + firstSelection[3], firstSelection[4]]
                mouse_clecked_count += 1
            elif secSelection[3] in sourcepiecelist:
                revealedBoxes[fs_x][fs_y] = None
                revealedBoxes[ss_x][ss_y] = None
                all_pieces[fs_x][fs_y] = [None, None]
                for move_y in range(beginmove_y, box_y + self.all_settings.piece_move_speed, self.all_settings.piece_move_speed):
                    displaySurf.blit(image, (box_x, move_y))
                all_pieces[ss_x][ss_y] = [None, None]
                mouse_clecked_count += 1
        return mouse_clecked_count

    def writeinfofile(self, filename, writestr):
        # 这个方法用来写入走棋详细步骤的内容
        # 按照走棋执行步骤依次写入
        # filename = self.all_settings.filename
        f = open(filename, 'ab+')
        writestr = (writestr + os.linesep).encode('utf-8')
        f.write(writestr)
        f.close()
        pass

    def writeinfofilerewrite(self, filename, writelist):
        # 这个方法用来重写悔棋时候，重新写入chess.info的内容
        # filename = self.all_settings.filename
        f = open(filename, 'w+', encoding='utf-8')
        f.writelines(writelist)
        f.close()
        pass

    def readinfofile(self, filename):
        # 这个方法用来读取走棋详细步骤的内容
        # filename = self.all_settings.filename
        f = open(filename, 'r', encoding='utf-8')
        linelist = f.readlines()
        f.close()
        return linelist
        pass

    def getnowtime(self):
        # 获取当前系统时间
        ntime = time.strftime('%Y-%m-%d %H:%M:%S')
        return ntime
        pass

    def howlongtime(self, begintime, endtime):
        # 获取一轮游戏总共耗时的时间，返回str
        howlongdays = (endtime - begintime).days
        howlongsecs = (endtime - begintime).seconds
        hours = int(howlongsecs / 3600)
        mins = int((howlongsecs % 3600) / 60)
        secs = (howlongsecs % 3600) % 60
        howlongtimestr = ''
        if howlongdays != 0:
            howlongdays = '%s天' % (str(howlongdays))
            howlongtimestr += howlongdays
        if hours != 0:
            hours = '%s小时' % (str(hours))
            howlongtimestr += hours
        if mins != 0:
            mins = '%s分' % (str(mins))
            howlongtimestr += mins
        if secs != 0:
            secs = '%s秒' % (str(secs))
            howlongtimestr += secs
        return howlongtimestr



    def getfilename(self):
        # 返回文件名带时间后缀
        filename = self.all_settings.filename
        filenamelist = filename.split('.')
        timename = time.strftime('_%Y_%m_%d_%H_%M_%S')
        filename1 = filenamelist[0] + timename
        filename = filename1 + '.info'
        return filename
        pass

    def revealedboxesstrtolist(self, revealedBoxesstr):
        # 将str状态下的revealedboxes转换成list状态
        revealedBoxesstr = revealedBoxesstr.replace('[', '')
        revealedBoxesstr = revealedBoxesstr.replace(']', '')
        revealedBoxesstr = revealedBoxesstr.strip('\n')

        strlist = revealedBoxesstr.split(',')
        boxes_list = []
        boxes_list1 = []
        count = 0
        for str in strlist:
            str = str.strip(' ')
            if str == 'True':
                boxes_list1.append(True)
            elif str == 'False':
                boxes_list1.append(False)
            elif str == 'None':
                boxes_list1.append(None)
            count += 1
            if count % 4 == 0:
                boxes_list.append(boxes_list1)
                boxes_list1 = []
        return boxes_list

    def allpiecesstrtolist(self, all_piecesstr):
        # 将str状态下的all_pieces转换成list状态
        all_piecesstr = all_piecesstr.replace('[', '')
        all_piecesstr = all_piecesstr.replace(']', '')
        all_piecesstr = all_piecesstr.replace('\'', '')
        all_piecesstr = all_piecesstr.strip('\n')
        strlist = all_piecesstr.split(',')
        list1 = []
        list2 = []
        list3 = []
        count1, count2 = 0, 0
        for str in strlist:
            str = str.strip(' ')
            if str == 'None':
                str = None
            list1.append(str)
            count1 += 1
            count2 += 1
            if count1 % 2 == 0:
                list2.append(list1)
                list1 = []
            if count2 % 8 == 0:
                list3.append(list2)
                list2 = []
        return list3
