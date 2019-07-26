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
# V0.0.5 添加最小化至系统托盘功能，添加后台时自动提示当前天气和明天天气有雨情况
# V0.1.0 添加手动输入城市的功能
# V0.1.2 修复手动模式下，多次输入城市信息时，由于list未清空导致的城市信息不能更新


import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QPushButton, QApplication, QLineEdit, QDesktopWidget, 
                            QGridLayout, QSystemTrayIcon, QMessageBox, QMenu, QAction, QCheckBox, QDialog, 
                            QVBoxLayout, QHBoxLayout, QComboBox, qApp)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import *
import requests


SEARCH_CITY_URL = r"https://search.heweather.net/find?location="
USR_KEY = r"&key=80aa4504b70a4de4bf27bf4c521dc362"
SEARCH_GROUP = r"&group=cn"

#UI类
class Ui_Class(QWidget):
    click_btn_sig = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.dg_clicked_flg = True  #这个标识是：勾选手动输城市时，第一次点弹出下拉框，第二次点确认信息； 
        self.usr_define_city = False
        self.usr_def_flag_ret = False
        self.cid_list = []
        self.city_name_list = []
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
        
        self.manu_check = QCheckBox("手动输入城市名称",self)
        self.usr_city_line = QLineEdit(self)
        self.usr_confirm_btn = QPushButton("确定",self)
        
        #系统托盘实例
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QIcon('weather.ico'))
        self.trayIcon.activated.connect(self.ico_clicked)
        
        #托盘添加右键退出菜单
        self.quit_action = QAction("退出",self,triggered=self.tray_quit)
        self.traymenu = QMenu(self)
        self.traymenu.addAction(self.quit_action)
        self.trayIcon.setContextMenu(self.traymenu)
        
        self.tray_msg_flag = True
        
        self.init_ui()
    
    #重写关闭事件
    def closeEvent(self, e):
        sel = QMessageBox.question(self, "后台提示", "是否需要最小化到系统托盘", QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if sel == QMessageBox.Yes:
            e.ignore()    #忽略关闭事件
            self.trayIcon.setVisible(True)
            self.hide()
        else:
            self.trayIcon.setVisible(False)
            e.accept()  #响应关闭事件
            
    def tray_quit(self):
        self.trayIcon.setVisible(False)
        qApp.quit()
        
    
    #托盘上的图标被左键单击或者双击时的响应函数
    def ico_clicked(self, reason):
        if(reason==QSystemTrayIcon.Trigger or reason==QSystemTrayIcon.DoubleClick):
            if self.isVisible():
                self.hide()
            else:
                self.show()
        
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
        self.usr_city_line.setDisabled(True)
        self.usr_confirm_btn.setDisabled(False)
        
        #控件布局        
        grid = QGridLayout()
        grid.setSpacing(2)
        grid.addWidget(self.manu_check, 0, 0)
        grid.addWidget(self.usr_city_line, 0, 1)
        grid.addWidget(self.usr_confirm_btn, 0, 2)
        grid.addWidget(self.city, 1, 0)
        grid.addWidget(self.city_line, 1, 1, 1, 2)
        grid.addWidget(self.time, 2, 0)
        grid.addWidget(self.time_line, 2, 1, 1, 2)
        grid.addWidget(self.weath, 3, 0)
        grid.addWidget(self.weat_line, 3, 1, 1, 2)
        grid.addWidget(self.weath_1, 4, 0)
        grid.addWidget(self.weat_line_1, 4, 1, 1, 2)
        grid.addWidget(self.weath_2, 5, 0)
        grid.addWidget(self.weat_line_2, 5, 1, 1, 2)
        
        #设置信号响应
        self.manu_check.toggled.connect(self.check_box_toggle)
        self.usr_confirm_btn.clicked.connect(self.confirm_btn_click)
        
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
    
    #手动输入城市名称checkbox响应
    def check_box_toggle(self, check_stat):
        if check_stat==True: #checkBox被勾选
            self.usr_city_line.setDisabled(False)
            self.usr_confirm_btn.setDisabled(False)
            self.usr_define_city = True
        else:
            self.usr_city_line.setDisabled(True)
            self.usr_confirm_btn.setDisabled(True)
            self.usr_define_city = False
            
    #确定按钮响应函数
    def confirm_btn_click(self):
        #自动模式下点击 确定 按钮
        if self.usr_define_city==False:
            self.usr_def_flag_ret = False
            self.usr_confirm_btn.setDisabled(True)
            self.manu_check.setDisabled(True)
            self.click_btn_sig.emit(False)
        #手动模式下点击 确定 按钮
        else:
            self.usr_def_flag_ret = True
            if self.dg_clicked_flg==True: #当前是第一次点击 确定 按钮
                self.city_name_list.clear() #清空list，否则会在输入内容变化时，无法及时更新城市信息
                usr_def_city_str = self.usr_city_line.text()
                if len(usr_def_city_str)>0:
                    url_str = SEARCH_CITY_URL+usr_def_city_str+USR_KEY+SEARCH_GROUP
                    rs_we = requests.get(url_str).json()
                    get_status = rs_we["HeWeather6"][0]["status"]
                    if get_status=="ok":
                        city_num = len(rs_we["HeWeather6"][0]["basic"])
                        city_str_index = 0
                        while(city_str_index<city_num):
                            self.city_name_list.append(rs_we["HeWeather6"][0]["basic"][city_str_index]["admin_area"]+"-"+rs_we["HeWeather6"][0]["basic"][city_str_index]["parent_city"]+"-"+rs_we["HeWeather6"][0]["basic"][city_str_index]["location"])
                            self.cid_list.append(rs_we["HeWeather6"][0]["basic"][city_str_index]["cid"])
                            city_str_index = city_str_index + 1
                        self.showDialog(self.city_name_list)
                    else:
                        QMessageBox.warning(self, "错误", "无法获取城市信息!")
                else:
                    QMessageBox.warning(self, "错误", "用户未输入!")
            else: #第二次点击
                self.usr_city_line.setDisabled(True)
                self.usr_confirm_btn.setDisabled(True)
                self.manu_check.setDisabled(True)
                self.click_btn_sig.emit(True)
    
    #托盘弹出气泡提示框，弹出频率由刷新天气频率确定
    def tray_msg_show(self, str_info):
        if len(str_info)>5:    #确保是有效数据
            if self.tray_msg_flag == True:
                self.trayIcon.showMessage("简易天气提示",str_info,QSystemTrayIcon.Information,2000)
                #self.tray_msg_flag = False  #保留功能
            else:
                pass
        else:
            pass
            
    def showDialog(self, city_list):
        vbox=QVBoxLayout()#纵向布局
        hbox=QHBoxLayout()#横向布局
        self.dialog=QDialog(self)
        self.dialog.resize(100,60)
        self.okBtn=QPushButton("确定")
        self.cancelBtn=QPushButton("取消")
        self.okBtn.clicked.connect(self.click_diag_ok_btn)
        self.cancelBtn.clicked.connect(self.click_diag_cancel_btn)
        self.city_cmb = QComboBox(self)
        for ct in city_list:
            self.city_cmb.addItem(ct)

        self.dialog.setWindowTitle("城市选择")
        # 确定与取消按钮横向布局
        hbox.addWidget(self.okBtn)
        hbox.addWidget(self.cancelBtn)

        vbox.addWidget(self.city_cmb)
        vbox.addLayout(hbox)
        self.dialog.setLayout(vbox)
        
        self.dialog.setWindowModality(Qt.ApplicationModal)#该模式下，只有该dialog关闭，才可以关闭父界面
        self.dialog.exec_()
    
    # 弹出的对话框里的确认按钮    
    def click_diag_ok_btn(self):
        select_txt = self.city_cmb.currentText()
        self.usr_city_line.setText(select_txt)
        self.dialog.close()
        self.dg_clicked_flg=False
      
    # 弹出的对话框里的取消按钮 
    def click_diag_cancel_btn(self):
        self.dialog.close()
    
    #根据城市名称获取城市id
    def get_cid(self):
        ret = 0
        index = 0
        usr_cit = self.usr_city_line.text()
        for i in self.city_name_list:
            if usr_cit==i:
                ret = index
                break
            else:
                index = index+1
        return self.cid_list[ret]
        
    def get_usr_define_flg(self):
        return self.usr_define_city
        
    #返回False表示使用自动获取，返回True表示用户自定义
    def get_flag(self):
        return self.usr_def_flag_ret
        

