#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
本软件为自己工作之余学习python所做，主要是想学习PyQt5的使用及了解网络编程。
本人水平较低，难免有不足与错误之处，还望各位大佬指正，也希望自己在此过程中能扩展自己的知识面，提升自己的编程水平
"""

# Note:本软件使用 和风天气 提供的天气预报API，需要注册以获取key， 地址 https://dev.heweather.com/
# date:       2019/07/19
# dev os/ver: windows7-64bit, python3.7
# author:     gorkon
# soft ver:   V0.0.1
# change log: 创建程序
# V0.0.2 添加用户输入城市名称选项
# V0.0.3 天气API使用auto_ip选项


import sys
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QLineEdit, QDesktopWidget, QGridLayout
from PyQt5.QtGui import QFont

#UI类
class Ui_Class(QWidget):

    def __init__(self):
        super().__init__()
        self.city = QLabel("当前城市",self)
        self.time = QLabel("当前时间",self)
        self.weath= QLabel("当前天气",self)
        self.weath_1= QLabel("明天天气",self)
        self.weath_2= QLabel("后天天气",self)
        self.city_line = QLineEdit(self)
        self.time_line = QLineEdit(self)
        self.weat_line = QLineEdit(self)
        self.weat_line_1 = QLineEdit(self)
        self.weat_line_2 = QLineEdit(self)
        self.init_ui()
        
    def init_ui(self):
        ui_font = QFont("宋体",12)
        self.setFont(ui_font)
        self.resize(480,320)
        self.setWindowTitle("简易天气")
        
        #将窗体部署到屏幕中间
        screen_size = QDesktopWidget().screenGeometry()
        app_ui_size = self.geometry()
        self.move((screen_size.width()-app_ui_size.width())/2, (screen_size.height()-app_ui_size.height())/2)
        
        #设置lineedit不可编辑
        self.city_line.setDisabled(True)
        self.time_line.setDisabled(True)
        self.weat_line.setDisabled(True)
        self.weat_line_1.setDisabled(True)
        self.weat_line_2.setDisabled(True)
        
        #控件布局        
        grid = QGridLayout()
        grid.setSpacing(2)
        grid.addWidget(self.city, 1, 0)
        grid.addWidget(self.city_line, 1, 1)
        grid.addWidget(self.time, 2, 0)
        grid.addWidget(self.time_line, 2, 1)
        grid.addWidget(self.weath, 3, 0)
        grid.addWidget(self.weat_line, 3, 1)
        grid.addWidget(self.weath_1, 4, 0)
        grid.addWidget(self.weat_line_1, 4, 1)
        grid.addWidget(self.weath_2, 5, 0)
        grid.addWidget(self.weat_line_2, 5, 1)
        
        self.setLayout(grid) 

        self.show()
    
    #更新 当前天气 信息
    def update_now_weather(self, str_info):
        self.weat_line.setText(str_info)
    
    #更新当前时间信息
    def update_time(self, str_info):
        self.time_line.setText(str_info)
    
    #更新 明天天气 信息
    def update_1_weather(self, str_info):
        self.weat_line_1.setText(str_info)
        
    #更新 后天天气 信息
    def update_2_weather(self, str_info):
        self.weat_line_2.setText(str_info)
    
    #设置 当前天气 字体颜色
    def set_now_weathercolor(self, str_color):
        self.weat_line.setStyleSheet("color:"+str_color)
        
    #更新当前城市信息
    def update_location(self, str_info):
        self.city_line.setText(str_info)
     
    #设置 label 内容，index为1表示明日天气， 为2表示后天天气
    def set_label(self, index, str):
        if index == 1:
            self.weath_1.setText(str)
        elif index == 2:
            self.weath_2.setText(str)
        else:
            pass
     
    #设置 明天或后天 天气字体颜色
    def set_otr_weathercolor(self, index, str_color):
        if index==1:
            self.weat_line_1.setStyleSheet("color:"+str_color)
        else:
            self.weat_line_2.setStyleSheet("color:"+str_color)


