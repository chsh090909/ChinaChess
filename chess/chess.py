#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, sys
from pygame.locals import *
from settings import Settings
from game_functions import GameFunctions

def main():
    all_settings = Settings()
    game_fn = GameFunctions(all_settings)
    fpsClock = pygame.time.Clock()

    pygame.init()
    displaySurf = pygame.display.set_mode((all_settings.screen_width, all_settings.screen_height))
    pygame.display.set_caption(all_settings.game_title)
    displaySurf.fill(all_settings.bg_color)

    mouse_x = 0
    mouse_y = 0
    playerinfo = {
        'nowPlayer': all_settings.player1_name,
        # 'pieceColor': 'red',
        'pieceColor': 'None',
        'totalCount': 0,
        'wonCount': 0,
        'tieCount': 0
    }
    box_x, box_y = game_fn.getBoxXY(mouse_x, mouse_y)
    all_pieces = game_fn.getRandomAllPieces()
    revealedBoxes = game_fn.getPiecesStatus(False)

    #all_pieces = [[[None, None], ['red_shuai', 'images/pieces_front_red_shuai.png'], [None, None], ['black_xiang1', 'images/pieces_front_black_xiang1.png']], [[None, None], [None, None], ['red_xiang2', 'images/pieces_front_red_xiang2.png'], ['red_bing5', 'images/pieces_front_red_bing5.png']], [[None, None], ['black_ma2', 'images/pieces_front_black_ma2.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], ['red_ma1', 'images/pieces_front_red_ma1.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_xiang1', 'images/pieces_front_red_xiang1.png'], [None, None], [None, None]], [[None, None], [None, None], ['red_ma2', 'images/pieces_front_red_ma2.png'], ['red_bing2', 'images/pieces_front_red_bing2.png']]]
    #revealedBoxes = [[None, True, None, True], [None, None, True, True], [None, True, None, None], [None, None, None, True], [None, None, None, None], [None, None, None, None], [None, True, None, None], [None, None, True, True]]

    # all_pieces = [[[None, None], [None, None], [None, None], ['black_zu1', 'images/pieces_front_black_zu1.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_xiang1', 'images/pieces_front_red_xiang1.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]]]
    # revealedBoxes = [[None, None, None, True], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, True, None, None], [None, None, None, None]]
    firstSelection = None
    secSelection = None
    mouse_clecked_count = 0
    player1_checked_count = 0
    player2_checked_count = 0

    while True:
        mouse_clecked = False

        displaySurf.fill(all_settings.bg_color)
        game_fn.drawBoard(displaySurf, box_x, box_y, revealedBoxes, playerinfo, all_pieces, firstSelection=firstSelection)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                # 用户点击关闭程序，或者按下键盘的esc键，程序退出
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clecked = True
            if event.type  == KEYUP and event.key == K_b:
                # 用户按下键盘字母b键，处理用户悔棋功能
                pass

        box_x, box_y = game_fn.getBoxXY(mouse_x, mouse_y)
        if box_x != None and box_y != None:
            box_numX, box_numY = game_fn.getBoxNum(box_x, box_y)

            if revealedBoxes[box_numX][box_numY] == False:
                # FALSE：表示棋子还没有被打开
                if mouse_clecked:
                    # 选择了没有翻开的棋子，就打开棋子的内容并展示出来
                    revealedBoxes[box_numX][box_numY] = True
                    piece_name = all_pieces[box_numX][box_numY][0]
                    mouse_clecked_count += 1
                    piecelist = piece_name.split('_')
                    piece_color = piecelist[0]
                    if mouse_clecked_count == 1:
                        playerinfo['pieceColor'] = piece_color
                    mouse_clecked = False
                    firstSelection = None
                    if mouse_clecked_count % 2 == 0:
                        playerinfo['nowPlayer'] = all_settings.player1_name
                    else:
                        playerinfo['nowPlayer'] = all_settings.player2_name
            else:
                nowPlayer = playerinfo['nowPlayer']
                player1PieceColor = playerinfo['pieceColor']
                player2PieceColor = 'red' if player1PieceColor == 'black' else 'black'
                if revealedBoxes[box_numX][box_numY] == True:
                    # TRUE：表示棋子已经打开，需要展示棋子上的内容
                    piece_name = all_pieces[box_numX][box_numY][0]
                    piece_image_url = all_pieces[box_numX][box_numY][1]
                    piecelist = piece_name.split('_')
                    piece_name_color = piecelist[0]
                    piece_name_name = piecelist[1]
                elif revealedBoxes[box_numX][box_numY] == None:
                    # NONE：表示当前棋子为空位
                    piece_image_url = None
                    piece_name_color = None
                    piece_name_name = None
                print('当前%s走棋！' % nowPlayer)

                if nowPlayer == all_settings.player1_name:
                    if piece_name_color == player1PieceColor:
                        # 当前棋子的颜色与player1玩家的执方颜色一致，就需要判断用户是第几次选择该棋子：
                        # 如果是第一次选择该棋子，就获取该棋子的颜色和棋面，用于和第二次的棋子比大小；
                        # 如果是第二次选择该棋子了，就认为重复选择了，就取消该棋子的选中功能；
                        if mouse_clecked:
                            player1_checked_count += 1
                            if player1_checked_count % 2 == 1:
                                print('Player1走棋！选择了%s，当前第1次选择！允许选择！' % piece_name)
                                firstSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                print('Player1的firstSelection: ' + str(firstSelection))
                            else:
                                print('Player1走棋！选择了%s，当前第2次选择！取消选择！' % piece_name)
                                firstSelection = None
                                print('Player1的firstSelection: ' + str(firstSelection))
                    else:
                        # 当前棋子的颜色与player1玩家的执方颜色不一致
                        # 获取当前棋子棋面，和前面的firstSelection比大小
                        if mouse_clecked:
                            if firstSelection != None:
                                if revealedBoxes[box_numX][box_numY] == True:
                                    print('Player1走棋完成！第二次选择了%s' % piece_name)
                                    secSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                    print('Player1的secSelection: ' + str(secSelection))
                                elif revealedBoxes[box_numX][box_numY] == None:
                                    print('Player1走棋完成！第二次选择了%s' % 'None')
                                    secSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                    print('Player1的secSelection: ' + str(secSelection))

                                pieceVSpiece_count = game_fn.pieceVSpiece(displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces)
                                mouse_clecked_count += pieceVSpiece_count
                                player1_checked_count += 1
                                firstSelection = None
                                secSelection = None
                                if mouse_clecked_count % 2 == 0:
                                    playerinfo['nowPlayer'] = all_settings.player1_name
                                else:
                                    playerinfo['nowPlayer'] = all_settings.player2_name
                                haswon = game_fn.hasWon(displaySurf, revealedBoxes, all_pieces, playerinfo, fpsClock)
                                if haswon:
                                    all_pieces, revealedBoxes, mouse_clecked_count, player1_checked_count, player2_checked_count, playerinfo = game_fn.startGame(playerinfo)
                elif nowPlayer == all_settings.player2_name:
                    if piece_name_color == player2PieceColor:
                        if mouse_clecked:
                            player2_checked_count += 1
                            if player2_checked_count % 2 == 1:
                                print('Player2走棋！选择了%s，当前第1次选择！允许选择！' % piece_name)
                                firstSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                print('Player2的firstSelection: ' + str(firstSelection))
                            else:
                                print('Player2走棋！选择了%s，当前第2次选择！取消选择！' % piece_name)
                                firstSelection = None
                                print('Player2的firstSelection: ' + str(firstSelection))
                    else:
                        if mouse_clecked:
                            if firstSelection != None:
                                if revealedBoxes[box_numX][box_numY] == True:
                                    print('Player2走棋完成！第二次选择了%s' % piece_name)
                                    secSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                    print('Player2的secSelection: ' + str(secSelection))
                                elif revealedBoxes[box_numX][box_numY] == None:
                                    print('Player2走棋完成！第二次选择了%s' % 'None')
                                    secSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                    print('Player2的secSelection: ' + str(secSelection))
                                player2_checked_count += 1
                                pieceVSpiece_count = game_fn.pieceVSpiece(displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces)
                                mouse_clecked_count += pieceVSpiece_count
                                firstSelection = None
                                secSelection = None
                                if mouse_clecked_count % 2 == 0:
                                    playerinfo['nowPlayer'] = all_settings.player1_name
                                else:
                                    playerinfo['nowPlayer'] = all_settings.player2_name
                                haswon = game_fn.hasWon(displaySurf, revealedBoxes, all_pieces, playerinfo, fpsClock)
                                if haswon:
                                    all_pieces, revealedBoxes, mouse_clecked_count, player1_checked_count, player2_checked_count, playerinfo = game_fn.startGame(playerinfo)
        pygame.display.update()
        fpsClock.tick(all_settings.FPS)

if __name__ == '__main__':
    main()