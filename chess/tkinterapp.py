#!/usr/bin/python3
# encoding: utf-8

"""
@author: chsh
@contact:
@file:  tkinterapp.py
@time:  2019/7/25 16:52
"""

from tkinter import *
from tkinter import messagebox
from settings import Settings
from chess import main
import platform
import os

all_settings = Settings()

class App:
    def __init__(self, master):
        self.master = master
        self.init_menu()

    def init_menu(self):
        # 创建menubar，放入master中
        menubar = Menu(self.master)
        # 可设置子目录的名称的图片icon
        # self.master.icon1 = PhotoImage(file='images/111.png')
        # 添加菜单条
        self.master['menu'] = menubar
        # 创建顶级菜单内容
        game_menu = Menu(menubar, tearoff=0)
        action_menu = Menu(menubar, tearoff=0)
        about_menu = Menu(menubar, tearoff=0)
        # 将顶级菜单放入menuber中
        menubar.add_cascade(label='游戏', menu=game_menu)
        menubar.add_cascade(label='操作', menu=action_menu)
        menubar.add_cascade(label='关于', menu=about_menu)
        # 为顶级菜单加入二级子菜单
        game_menu.add_command(label='游戏开始', command=main)
        game_menu.add_command(label='游戏结束', command=None)
        action_menu.add_command(label='悔棋', command=None, accelerator='B')
        about_menu.add_command(label='如何玩？', command=self.openpdffile)
        about_menu.add_command(label='关于...', command=None)
        # 如果有子菜单图片icon
        # action_menu.add_command(label='开始', command=None, compound=LEFT, image=self.master.icon1)
        # 为子菜单之间添加分割条
        #action_menu.add_separator()
        # action_menu中有三级子菜单，则需要在action_menu再建子菜单
        changemusic_menu = Menu(action_menu, tearoff=0)
        action_menu.add_cascade(label='更换背景音乐', menu=changemusic_menu)
        # 用ttk的variable绑定changemusic_menu菜单
        self.bgmusicVar = StringVar()
        # 列出背景音乐列表可供选择
        for bgmusic in all_settings.bgmusiclist:
            changemusic_menu.add_radiobutton(label=bgmusic, command=self.changemusicvalue, variable=self.bgmusicVar, value=bgmusic)

    # 为背景音乐列表中选中的值做处理
    def changemusicvalue(self):
        messagebox.showinfo(title="消息", message="选择的音乐是：%s" % self.bgmusicVar.get())

    # 为'如何玩？'选项添加打开pdf帮助文档
    def openpdffile(self):
        # 获取当前文件路径
        curpwd = os.getcwd()
        # 获取当前系统的名称，用以区分mac和windows
        ostypestr = platform.platform()
        ostype = ostypestr.split('-')[0]
        opencmd = ''
        if ostype == 'Darwin':
            # MacOS
            filepath = os.path.join(curpwd, all_settings.helppdffile)
            opencmd += 'open %s' % filepath
        elif ostype == 'Windows':
            # Windows
            filepath = curpwd + '/' + all_settings.helppdffile
            opencmd += filepath
        # 调用系统命令行，打开pdf文件
        os.system(opencmd)

if __name__ == '__main__':
    root = Tk()
    root.title(all_settings.game_title)
    App(root)
    root.mainloop()