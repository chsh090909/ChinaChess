#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, sys, datetime
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

    # all_pieces = [[[None, None], [None, None], ['red_pao2', 'images/pieces_front_red_pao2.png'], [None, None]], [[None, None], ['red_ju2', 'images/pieces_front_red_ju2.png'], [None, None], ['black_shi2', 'images/pieces_front_black_shi2.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_shi1', 'images/pieces_front_red_shi1.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [['black_ju1', 'images/pieces_front_black_ju1.png'], ['black_pao2', 'images/pieces_front_black_pao2.png'], ['black_xiang1', 'images/pieces_front_black_xiang1.png'], ['black_ju2', 'images/pieces_front_black_ju2.png']], [['black_zu5', 'images/pieces_front_black_zu5.png'], ['red_xiang2', 'images/pieces_front_red_xiang2.png'], [None, None], [None, None]], [['red_ma2', 'images/pieces_front_red_ma2.png'], ['black_jiang', 'images/pieces_front_black_jiang.png'], ['black_xiang2', 'images/pieces_front_black_xiang2.png'], ['black_ma2', 'images/pieces_front_black_ma2.png']]]
    # revealedBoxes = [[None, None, True, None], [None, False, None, True], [None, None, None, None], [None, False, None, None], [None, None, None, None], [True, False, True, True], [False, False, None, None], [True, False, True, True]]
    # 这里有多个棋子
    # all_pieces = [[[None, None], ['red_shuai', 'images/pieces_front_red_shuai.png'], [None, None], ['black_xiang1', 'images/pieces_front_black_xiang1.png']], [[None, None], [None, None], ['red_xiang2', 'images/pieces_front_red_xiang2.png'], ['red_bing5', 'images/pieces_front_red_bing5.png']], [[None, None], ['black_ma2', 'images/pieces_front_black_ma2.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], ['red_ma1', 'images/pieces_front_red_ma1.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_xiang1', 'images/pieces_front_red_xiang1.png'], [None, None], [None, None]], [[None, None], [None, None], ['red_ma2', 'images/pieces_front_red_ma2.png'], ['red_bing2', 'images/pieces_front_red_bing2.png']]]
    # revealedBoxes = [[None, True, None, True], [None, None, True, True], [None, True, None, None], [None, None, None, True], [None, None, None, None], [None, None, None, None], [None, True, None, None], [None, None, True, True]]
    # 这里只有两个棋子做比较
    # all_pieces = [[[None, None], [None, None], [None, None], ['black_zu1', 'images/pieces_front_black_zu1.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_xiang1', 'images/pieces_front_red_xiang1.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]]]
    # revealedBoxes = [[None, None, None, True], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, True, None, None], [None, None, None, None]]
    global firstSelection, secSelection, mouse_clecked_count
    firstSelection = None
    secSelection = None
    mouse_clecked_count = 0
    player1_checked_count = 0
    player2_checked_count = 0

    begintime = datetime.datetime.now()
    beginstr = "*" * 20 + all_settings.beginstr + "*" * 20
    writestr = '%s|%d|%s|%s|(%d, %d)' % (game_fn.getnowtime(), mouse_clecked_count, playerinfo['nowPlayer'], 'None_None', -1, -1)
    filename = game_fn.getfilename()
    game_fn.writeinfofile(filename, beginstr)
    game_fn.writeinfofile(filename, writestr)
    game_fn.writeinfofile(filename, str(all_pieces))
    game_fn.writeinfofile(filename ,str(revealedBoxes))

    while True:
        mouse_clecked = False

        displaySurf.fill(all_settings.bg_color)
        game_fn.drawBoard(displaySurf, box_x, box_y, revealedBoxes, playerinfo, all_pieces, firstSelection=firstSelection)

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                # 用户点击关闭程序，或者按下键盘的esc键，程序退出
                # 退出系统之前记录本轮游戏的结果
                endtime = datetime.datetime.now()
                # 游戏共经历了多少时长howlongtime
                howlongtime = game_fn.howlongtime(begintime, endtime)
                # 记录游戏局数和胜利的玩家信息
                totalcount = playerinfo['totalCount']
                player1woncount = playerinfo['wonCount']
                tiecount = playerinfo['tieCount']
                player2woncount = totalcount - player1woncount - tiecount
                gameoverstr = "**********本轮游戏时长为%s，总共完成%d局" % (howlongtime, totalcount)
                if totalcount != 0:
                    if player1woncount > player2woncount:
                        gameoverstr += "，其中%s技高一筹，胜%d局，" % (all_settings.player1_name, player1woncount)
                    elif player1woncount < player2woncount:
                        gameoverstr += "，其中%s技高一筹，胜%d局，" % (all_settings.player2_name, player2woncount)
                    else:
                        gameoverstr += "，两位玩家旗鼓相当，均胜%d局，" % player1woncount
                    gameoverstr += "打平%d局" % tiecount
                gameoverstr += "**********"
                game_fn.writeinfofile(filename, gameoverstr)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clecked = True
            if event.type  == KEYUP and event.key == K_b:
                # 用户按下键盘字母b键，处理用户悔棋功能
                if mouse_clecked_count == 0:
                    break
                else:
                    linelist = game_fn.readinfofile(filename)
                    # 删除lastline最后一步的内容(倒数三行)，并还原倒数两行中的all_pieces和revealedBoxes的值
                    linelist.pop(len(linelist) - 1)
                    linelist.pop(len(linelist) - 1)
                    linelist.pop(len(linelist) - 1)
                    revealedBoxesstr = linelist[len(linelist) - 1]
                    revealedBoxes = game_fn.revealedboxesstrtolist(revealedBoxesstr)
                    all_piecesstr = linelist[len(linelist) - 2]
                    all_pieces = game_fn.allpiecesstrtolist(all_piecesstr)
                    print(revealedBoxes)
                    print(all_pieces)
                    # 还原mouse_clecked_count的数量
                    mouse_clecked_count -= 1
                    # 还原playerinfo的内容和状态
                    nowPlayer = playerinfo['nowPlayer']
                    playerinfo['nowPlayer'] = all_settings.player2_name if nowPlayer == all_settings.player1_name else all_settings.player1_name
                    print("悔棋成功！！")
                    # 将新的linelist重新写入info文件
                    game_fn.writeinfofilerewrite(filename, linelist)
                    print("重写info文件成功！！")
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
                    bplayer = all_settings.player2_name
                    if mouse_clecked_count % 2 != 0:
                        playerinfo['nowPlayer'] = all_settings.player2_name
                        bplayer = all_settings.player1_name
                    else:
                        playerinfo['nowPlayer'] = all_settings.player1_name
                    writestr = '%s|%d|%s|%s|(%d, %d)' % (game_fn.getnowtime(), mouse_clecked_count, bplayer, piece_name, box_numX, box_numY)
                    game_fn.writeinfofile(filename, writestr)
                    game_fn.writeinfofile(filename, str(all_pieces))
                    game_fn.writeinfofile(filename, str(revealedBoxes))
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

                                pieceVSpiece_info = game_fn.pieceVSpiece(displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces)
                                pieceVSpiece_count = int(pieceVSpiece_info[0])
                                mouse_clecked_count += pieceVSpiece_count
                                all_pieces = pieceVSpiece_info[1]
                                revealedBoxes = pieceVSpiece_info[2]
                                player1_checked_count += 1
                                bplayer = all_settings.player2_name
                                if mouse_clecked_count % 2 != 0:
                                    playerinfo['nowPlayer'] = all_settings.player2_name
                                    bplayer = all_settings.player1_name
                                else:
                                    playerinfo['nowPlayer'] = all_settings.player1_name
                                writestr = '%s|%d|%s|%s_%s|(%d, %d)|%s_%s|(%d, %d)' % \
                                           (game_fn.getnowtime(), mouse_clecked_count, bplayer, firstSelection[2], firstSelection[3], firstSelection[0], firstSelection[1], secSelection[2], secSelection[3], secSelection[0], secSelection[1])
                                game_fn.writeinfofile(filename, writestr)
                                game_fn.writeinfofile(filename, str(all_pieces))
                                game_fn.writeinfofile(filename, str(revealedBoxes))
                                firstSelection = None
                                secSelection = None
                                haswon = game_fn.hasWon(displaySurf, revealedBoxes, all_pieces, playerinfo, fpsClock)
                                if haswon[0] == True:
                                    writestr = '%s    第%d步：%s===>第%d局游戏结束！！！' % (game_fn.getnowtime(), mouse_clecked_count + 1, haswon[1], playerinfo['totalCount'])
                                    writestr1 = '*****第%d局游戏开始*****' % (playerinfo['totalCount'] + 1,)
                                    game_fn.writeinfofile(filename, writestr)
                                    game_fn.writeinfofile(filename, writestr1)
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
                                pieceVSpiece_info = game_fn.pieceVSpiece(displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces)
                                pieceVSpiece_count = int(pieceVSpiece_info[0])
                                mouse_clecked_count += pieceVSpiece_count
                                all_pieces = pieceVSpiece_info[1]
                                revealedBoxes = pieceVSpiece_info[2]
                                bplayer = all_settings.player2_name
                                if mouse_clecked_count % 2 != 0:
                                    playerinfo['nowPlayer'] = all_settings.player2_name
                                    bplayer = all_settings.player1_name
                                else:
                                    playerinfo['nowPlayer'] = all_settings.player1_name
                                writestr = '%s|%d|%s|%s_%s|(%d, %d)|%s_%s|(%d, %d)' % \
                                           (game_fn.getnowtime(), mouse_clecked_count, bplayer, firstSelection[2], firstSelection[3], firstSelection[0], firstSelection[1], secSelection[2], secSelection[3], secSelection[0], secSelection[1])
                                game_fn.writeinfofile(filename, writestr)
                                game_fn.writeinfofile(filename, str(all_pieces))
                                game_fn.writeinfofile(filename, str(revealedBoxes))
                                firstSelection = None
                                secSelection = None
                                haswon = game_fn.hasWon(displaySurf, revealedBoxes, all_pieces, playerinfo, fpsClock)
                                if haswon[0] == True:
                                    writestr = '%s    第%d步：%s===>第%d局游戏结束！！！' % (game_fn.getnowtime(), mouse_clecked_count + 1, haswon[1], playerinfo['totalCount'])
                                    writestr1 = '*****第%d局游戏开始*****' % (playerinfo['totalCount'] + 1,)
                                    game_fn.writeinfofile(filename, writestr)
                                    game_fn.writeinfofile(filename, writestr1)
                                    all_pieces, revealedBoxes, mouse_clecked_count, player1_checked_count, player2_checked_count, playerinfo = game_fn.startGame(playerinfo)
        pygame.display.update()
        fpsClock.tick(all_settings.FPS)

if __name__ == '__main__':
    main()