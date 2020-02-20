#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, sys, datetime, random, logging
from pygame.locals import *
from settings import Settings
from game_functions import GameFunctions

all_settings = Settings()

def main():
    try:
        game_fn = GameFunctions(all_settings)
        fpsClock = pygame.time.Clock()
        # 定义日志
        logger = logging.getLogger('main')
        logger.setLevel(level=logging.DEBUG)
        # 定义打印到控制台的日志内容
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(all_settings.sysoutlevel)
        sysout_format = logging.Formatter(all_settings.sysoutformat)
        stream_handler.setFormatter(sysout_format)
        logger.addHandler(stream_handler)
        # 获取log日志文件的名称（带时间戳后缀）
        getlogfilename = all_settings.logfilename
        logfilename = game_fn.getfilename(getlogfilename)
        # 定义写入日志文件的日志内容
        file_handler = logging.FileHandler(filename=logfilename, encoding='utf-8')
        file_handler.setLevel(all_settings.filewritelevel)
        filewrite_format = logging.Formatter(all_settings.filewriteformat)
        file_handler.setFormatter(filewrite_format)
        logger.addHandler(file_handler)
        # 获取info文件的名称（带时间戳后缀）
        getinfofilename = all_settings.infofilename
        infofilename = game_fn.getfilename(getinfofilename)
        # 初始化游戏引擎
        pygame.init()
        pygame.mixer.init()
        # 初始化画布
        displaySurf = pygame.display.set_mode((all_settings.screen_width, all_settings.screen_height))
        pygame.display.set_caption(all_settings.game_title)
        displaySurf.fill(all_settings.bg_color)
        # 加载背景音乐随机播放
        music_play_flag = True
        keyboard_p = 0
        bgmusiclist = all_settings.bgmusiclist
        bgmusic = random.sample(bgmusiclist, 1)
        pygame.mixer.music.load('mids/%s' % bgmusic[0])
        pygame.mixer.music.play()
        logger.info("播放背景音乐： %s" % bgmusic[0])

        mouse_x = 0
        mouse_y = 0
        playerinfo = {
            'nowPlayer': all_settings.player1_name,
            # 'pieceColor': 'black',
            'pieceColor': 'None',
            'totalCount': 0,
            'wonCount': 0,
            'tieCount': 0
        }
        box_x, box_y = game_fn.getBoxXY(mouse_x, mouse_y)
        all_pieces = game_fn.getRandomAllPieces()
        revealedBoxes = game_fn.getPiecesStatus(False)

        # all_pieces = [[[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [['black_shi2', 'images/pieces_front_black_shi2.png'], [None, None], [None, None], [None, None]], [['red_bing4', 'images/pieces_front_red_bing4.png'], [None, None], [None, None], ['red_shuai', 'images/pieces_front_red_shuai.png']], [['black_ju2', 'images/pieces_front_black_ju2.png'], ['black_ma2', 'images/pieces_front_black_ma2.png'], ['black_zu4', 'images/pieces_front_black_zu4.png'], [None, None]], [[None, None], [None, None], [None, None], [None, None]]]
        # revealedBoxes = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [True, None, None, None], [True, None, None, True], [True, True, True, None], [None, None, None, None]]
        # 这里有多个棋子
        # all_pieces = [[[None, None], ['red_shuai', 'images/pieces_front_red_shuai.png'], [None, None], ['black_xiang1', 'images/pieces_front_black_xiang1.png']], [[None, None], [None, None], ['red_xiang2', 'images/pieces_front_red_xiang2.png'], ['red_bing5', 'images/pieces_front_red_bing5.png']], [[None, None], ['black_ma2', 'images/pieces_front_black_ma2.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], ['red_ma1', 'images/pieces_front_red_ma1.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_xiang1', 'images/pieces_front_red_xiang1.png'], [None, None], [None, None]], [[None, None], [None, None], ['red_ma2', 'images/pieces_front_red_ma2.png'], ['red_bing2', 'images/pieces_front_red_bing2.png']]]
        # revealedBoxes = [[None, True, None, True], [None, None, True, True], [None, True, None, None], [None, None, None, True], [None, None, None, None], [None, None, None, None], [None, True, None, None], [None, None, True, True]]
        # 这里只有两个棋子做比较
        # all_pieces = [[[None, None], [None, None], [None, None], ['black_zu1', 'images/pieces_front_black_zu1.png']], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]], [[None, None], ['red_xiang1', 'images/pieces_front_red_xiang1.png'], [None, None], [None, None]], [[None, None], [None, None], [None, None], [None, None]]]
        # revealedBoxes = [[None, None, None, True], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, True, None, None], [None, None, None, None]]
        global firstSelection, secSelection, mouse_clicked_count
        firstSelection = None
        secSelection = None
        mouse_clicked_count = 0
        player1_checked_count = 0
        player2_checked_count = 0
        # 游戏开始，写入游戏开始信息
        begintime = datetime.datetime.now()
        beginstr = "*" * 20 + all_settings.beginstr + "*" * 20
        writestr = '%s|%d|%s|%s|(%d, %d)' % (game_fn.getnowtime(), mouse_clicked_count, playerinfo['nowPlayer'], 'None_None', -1, -1)
        game_fn.writeinfofile(infofilename, beginstr)
        game_fn.writeinfofile(infofilename, writestr)
        game_fn.writeinfofile(infofilename, str(all_pieces))
        game_fn.writeinfofile(infofilename, str(revealedBoxes))

        while True:
            mouse_clecked = False
            # 加载画布信息
            displaySurf.fill(all_settings.bg_color)
            game_fn.drawBoard(displaySurf, box_x, box_y, revealedBoxes, playerinfo, all_pieces, firstSelection=firstSelection)
            # 加载背景音乐
            if pygame.mixer.music.get_busy() == False:
                if music_play_flag is True and keyboard_p == 0:
                    bgmusic = random.sample(bgmusiclist, 1)
                    pygame.mixer.music.load('mids/%s' % bgmusic[0])
                    pygame.mixer.music.play()
                    logger.info("更新播放背景音乐： %s" % bgmusic[0])
            for events in pygame.event.get():  # event handling loop
                if events.type == QUIT or (events.type == KEYUP and events.key == K_ESCAPE):
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
                    gameoverstr = "*" * 20
                    gameoverstr += "本轮游戏时长为%s，总共完成%d局" % (howlongtime, totalcount)
                    if totalcount != 0:
                        if player1woncount > player2woncount:
                            gameoverstr += "，其中%s技高一筹，胜%d局" % (all_settings.player1_name, player1woncount)
                        elif player1woncount < player2woncount:
                            gameoverstr += "，其中%s技高一筹，胜%d局" % (all_settings.player2_name, player2woncount)
                        else:
                            gameoverstr += "，两位玩家旗鼓相当，均胜%d局" % player1woncount
                        if tiecount != 0:
                            gameoverstr += "，打平%d局" % tiecount
                    gameoverstr += "*" * 20
                    game_fn.writeinfofile(infofilename, gameoverstr)
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.quit()
                    pygame.quit()
                    sys.exit()
                if events.type == MOUSEMOTION:
                    mouse_x, mouse_y = events.pos
                if events.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = events.pos
                    mouse_clecked = True
                if events.type  == KEYUP and events.key == K_b:
                    # 用户按下键盘字母b键，处理用户悔棋功能
                    # 以下为2019-07-04完成的内容
                    if mouse_clicked_count == 0:
                        break
                    else:
                        linelist = game_fn.readinfofile(infofilename)
                        # 删除lastline最后一步的内容(倒数三行)，并还原倒数两行中的all_pieces和revealedBoxes的值
                        linelist.pop(len(linelist) - 1)
                        linelist.pop(len(linelist) - 1)
                        linelist.pop(len(linelist) - 1)
                        revealedBoxesstr = linelist[len(linelist) - 1]
                        revealedBoxes = game_fn.revealedboxesstrtolist(revealedBoxesstr)
                        all_piecesstr = linelist[len(linelist) - 2]
                        all_pieces = game_fn.allpiecesstrtolist(all_piecesstr)
                        # 还原mouse_clicked_count的数量
                        mouse_clicked_count -= 1
                        # 还原playerinfo的内容和状态
                        nowPlayer = playerinfo['nowPlayer']
                        playerinfo['nowPlayer'] = all_settings.player2_name if nowPlayer == all_settings.player1_name else all_settings.player1_name
                        logger.info("悔棋成功！！")
                        # 将新的linelist重新写入info文件
                        game_fn.writeinfofilerewrite(infofilename, linelist)
                        logger.info("重写info文件成功！！")
                        # 加载悔棋的音效
                        soundobj = pygame.mixer.Sound(all_settings.hq)
                        soundobj.play()
                if events.type == KEYUP and events.key == K_p:
                    # 用户按下键盘字母p键，背景音乐停止，再次按下p键再次播放
                    if keyboard_p == 1:
                        music_play_flag = True
                        keyboard_p = 0
                    else:
                        pygame.mixer.music.stop()
                        music_play_flag = False
                        keyboard_p = 1
                        logger.info('背景音乐停止！')

            box_x, box_y = game_fn.getBoxXY(mouse_x, mouse_y)
            if box_x != None and box_y != None:
                box_numX, box_numY = game_fn.getBoxNum(box_x, box_y)

                if revealedBoxes[box_numX][box_numY] == False:
                    # FALSE：表示棋子还没有被打开
                    if mouse_clecked:
                        # 选择了没有翻开的棋子，就打开棋子的内容并展示出来
                        revealedBoxes[box_numX][box_numY] = True
                        # 加载走棋完成的音效
                        soundobj = pygame.mixer.Sound(all_settings.zqwc)
                        soundobj.play()
                        piece_name = all_pieces[box_numX][box_numY][0]
                        mouse_clicked_count += 1
                        piecelist = piece_name.split('_')
                        piece_color = piecelist[0]
                        if mouse_clicked_count == 1:
                            playerinfo['pieceColor'] = piece_color
                        firstSelection = None
                        bplayer = all_settings.player2_name
                        if mouse_clicked_count % 2 != 0:
                            playerinfo['nowPlayer'] = all_settings.player2_name
                            bplayer = all_settings.player1_name
                        else:
                            playerinfo['nowPlayer'] = all_settings.player1_name
                        writestr = '%s|%d|%s|%s|(%d, %d)' % (game_fn.getnowtime(), mouse_clicked_count, bplayer, piece_name, box_numX, box_numY)
                        game_fn.writeinfofile(infofilename, writestr)
                        game_fn.writeinfofile(infofilename, str(all_pieces))
                        game_fn.writeinfofile(infofilename, str(revealedBoxes))
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
                    # logger.debug('当前%s走棋！' % nowPlayer)
                    # 以下为2019-07-09优化的内容
                    if (nowPlayer == all_settings.player1_name and piece_name_color == player1PieceColor) or (nowPlayer == all_settings.player2_name and piece_name_color == player2PieceColor):
                        if mouse_clecked:
                            if nowPlayer == all_settings.player1_name:
                                player1_checked_count += 1
                            if nowPlayer == all_settings.player2_name:
                                player2_checked_count += 1
                            if player1_checked_count % 2 == 1 or player2_checked_count % 2 == 1:
                                # 加载选中棋子的音效
                                soundobj = pygame.mixer.Sound(all_settings.xz)
                                soundobj.play()
                                logger.info('%s走棋！选择了%s，当前第1次选择！允许选择！' % (nowPlayer, piece_name))
                                firstSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                logger.info('%s的firstSelection: %s' % (nowPlayer, str(firstSelection)))
                            else:
                                # 加载走棋完成的音效
                                soundobj = pygame.mixer.Sound(all_settings.zqwc)
                                soundobj.play()
                                logger.info('%s走棋！选择了%s，当前第2次选择！取消选择！' % (nowPlayer, piece_name))
                                firstSelection = None
                                logger.info('%s的firstSelection: %s' % (nowPlayer, str(firstSelection)))

                    if (nowPlayer == all_settings.player1_name and piece_name_color == player2PieceColor) or (nowPlayer == all_settings.player2_name and piece_name_color == player1PieceColor) or (nowPlayer == all_settings.player1_name and piece_name_color == None) or (nowPlayer == all_settings.player2_name and piece_name_color == None):
                        if mouse_clecked:
                            if firstSelection != None:
                                if revealedBoxes[box_numX][box_numY] == True:
                                    # 加载吃棋子的音效
                                    soundobj = pygame.mixer.Sound(all_settings.cq)
                                    soundobj.play()
                                    logger.info('%s走棋完成！第二次选择了%s' % (nowPlayer, piece_name))
                                    secSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                    logger.info('%s的secSelection: %s' % (nowPlayer, str(secSelection)))
                                elif revealedBoxes[box_numX][box_numY] == None:
                                    # 加载走棋完成的音效
                                    soundobj = pygame.mixer.Sound(all_settings.zqwc)
                                    soundobj.play()
                                    logger.info('%s走棋完成！第二次选择了%s' % (nowPlayer, 'None'))
                                    secSelection = (box_numX, box_numY, piece_name_color, piece_name_name, piece_image_url)
                                    logger.info('%s的secSelection: %s' % (nowPlayer, str(secSelection)))

                                pieceVSpiece_info = game_fn.pieceVSpiece(displaySurf, firstSelection, secSelection, revealedBoxes, all_pieces)
                                pieceVSpiece_count = int(pieceVSpiece_info[0])
                                mouse_clicked_count += pieceVSpiece_count
                                all_pieces = pieceVSpiece_info[1]
                                revealedBoxes = pieceVSpiece_info[2]
                                if nowPlayer == all_settings.player1_name:
                                    player1_checked_count += 1
                                if nowPlayer == all_settings.player2_name:
                                    player2_checked_count += 1
                                bplayer = all_settings.player2_name
                                if mouse_clicked_count % 2 != 0:
                                    playerinfo['nowPlayer'] = all_settings.player2_name
                                    bplayer = all_settings.player1_name
                                else:
                                    playerinfo['nowPlayer'] = all_settings.player1_name
                                writestr = '%s|%d|%s|%s_%s|(%d, %d)|%s_%s|(%d, %d)' % \
                                           (game_fn.getnowtime(), mouse_clicked_count, bplayer, firstSelection[2], firstSelection[3], firstSelection[0], firstSelection[1], secSelection[2], secSelection[3], secSelection[0], secSelection[1])
                                game_fn.writeinfofile(infofilename, writestr)
                                game_fn.writeinfofile(infofilename, str(all_pieces))
                                game_fn.writeinfofile(infofilename, str(revealedBoxes))
                                firstSelection = None
                                secSelection = None
                                haswon = game_fn.hasWon(displaySurf, revealedBoxes, all_pieces, playerinfo)
                                if haswon[0] == True:
                                    writestr = '%s 第%d步：%s===>第%d局游戏结束！！！' % (game_fn.getnowtime(), mouse_clicked_count + 1, haswon[1], playerinfo['totalCount'])
                                    writestr1 = '*****第%d局游戏开始*****' % (playerinfo['totalCount'] + 1)
                                    game_fn.writeinfofile(infofilename, writestr)
                                    game_fn.writeinfofile(infofilename, writestr1)
                                    all_pieces, revealedBoxes, mouse_clicked_count, player1_checked_count, player2_checked_count, playerinfo = game_fn.startGame(playerinfo)
            pygame.display.update()
            fpsClock.tick(all_settings.FPS)
    except Exception:
        # 两种方式任选其一
        logger.exception('Error')
        #logger.error('Error', exc_info = True)

if __name__ == '__main__':
    main()
