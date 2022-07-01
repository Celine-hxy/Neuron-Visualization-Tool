# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 15:02:08 2022

@author: Celine Huang 黄绣媛
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
import pandas as pd
import numpy as np


class MainWindow(QMainWindow):
    '''
    加载自定义的激活neuron, 模型构架, 显示激活的Neurons
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi("main.ui",self)
        self.initUI()               # 界⾯绘制交给InitUi⽅法
        self.initButton()           # 初始化Button
        self.initMenubar()          # 初始化Menubar
    
    # ---------- 初始化UI界面 ---------- # 
    def initUI(self):
        self.desktop = QApplication.desktop()
        # 获取显⽰器分辨率⼤⼩
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        # 设置窗口大小（初始、最大、最小）
        self.setFixedSize(self.width, self.height)    # 设置界面与屏幕同大
        # self.setFixedSize(1100, 435)
        self.setMaximumSize(16777215, 16777215)
        self.setMinimumSize(0, 0)
        # 设置窗口标题
        self.setWindowTitle('Activated Neurons Visualization Tools')
    
    # ---------- 定义加载函数 ---------- # 
    def load_csv(self):
        """
        加载激活的Neuron
        """
        # img_name, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "All Files(*);;*.jpg;;*.png")
        file_name, _ = QFileDialog.getOpenFileName(None, "Open csv file","","All Files(*);;*.csv")
        print(file_name)
        csv_file = pd.read_csv(str(file_name))
        print(csv_file)
    
    def load_Network(self):
        """
        加载Network, 将模型的构架显示在UI界面的左下角
        """
        # img_name, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "All Files(*);;*.jpg;;*.png")
        file_name, _ = QFileDialog.getOpenFileName(None, "Open csv file","","*.csv;;All Files(*)")          # ;;All Files(*)
        print(file_name)
        self.csv_file = pd.read_csv(str(file_name))
        self.csv_file = np.array(self.csv_file.values).flatten()
        print(self.csv_file)
    
    def load_Prompt(self):
        """
        加载Prompt, 并根据得到的Prompt初始化Combo box
        """
        file_name, _ = QFileDialog.getOpenFileName(None, "Open csv file","","*.csv;;All Files(*)")          # ;;All Files(*)
        print(file_name)
        self.prompt_file = pd.read_csv(str(file_name))
        self.prompt_file = np.array(self.prompt_file.values).flatten()
        print(self.prompt_file)
        self.initCombobox()
    
    # ---------- 初始化Combo box ---------- # 
    def initCombobox(self):
        self.ui.Combo_Prompt.clear()
        for prompt in self.prompt_file:
            self.ui.Combo_Prompt.addItem(prompt)    # 将获取的Prompt加到Combo box中
    
    def initMenubar(self):
        self.ui.actionLoad_csv_file.triggered.connect(self.load_csv)
        self.ui.actionLoad_Network.triggered.connect(self.load_Network)
        self.ui.actionLoad_Prompt.triggered.connect(self.load_Prompt)
    
    def initButton(self):
        self.ui.Bnt_Activate.clicked.connect(self.onButtonClick)
    
    def onButtonClick(self):
        '''
        按下按键之后获取当前Combo box中的Emotion任务, 在
        '''
        prompt = self.ui.Combo_Prompt.currentText()
        print(prompt)
    
        

class Example(QWidget):
    '''
    Example: 简单演示Prompt的激活原理
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi("example.ui",self)
        self.initUI()           # 界⾯绘制交给InitUi⽅法
        self.initButton()       # 初始化Button
        # self.ui.Example_QWidget.setStyleSheet("QLabel#Example_QWidget{border-image: url(./pics/pics/border/background.png);}")
        
    def initUI(self):
        self.desktop = QApplication.desktop()
        # 获取显⽰器分辨率⼤⼩
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        # 设置窗口大小（初始、最大、最小）
        # self.setFixedSize(self.width, self.height)    # 与屏幕同大
        self.setFixedSize(1300, 435)                    # 固定界面大小
        self.setMaximumSize(16777215, 16777215)
        self.setMinimumSize(0, 0)
        # 设置窗口标题
        self.setWindowTitle('Example')
        
    def initButton(self):
        self.buttonCount = 0
        self.ui.pushButton.clicked.connect(self.onButtonClick)
    
    def onButtonClick(self):
        # 创建对话框
        # print("clicked")
        self.buttonCount = self.buttonCount + 1
        if self.buttonCount%2 == 0:    
            self.ui.Prompt_label.setStyleSheet("border-image: url(./pics/pics/border/dark_bk.png);")
            self.ui.n_a_1.setStyleSheet("border-image: url(./pics/pics/neuron/b.png);")
            self.ui.n_a_2.setStyleSheet("border-image: url(./pics/pics/neuron/w.png);")
            self.ui.n_a_3.setStyleSheet("border-image: url(./pics/pics/neuron/b.png);")
            self.ui.n_a_4.setStyleSheet("border-image: url(./pics/pics/neuron/b.png);")
            self.ui.n_a_5.setStyleSheet("border-image: url(./pics/pics/neuron/w.png);")
            self.ui.n_a_6.setStyleSheet("border-image: url(./pics/pics/neuron/w.png);")
            self.ui.n_a_7.setStyleSheet("border-image: url(./pics/pics/neuron/b.png);")
            self.ui.Prompt_text.setText("The Captain of America is [MASK]")
            
        else:    
            self.ui.Prompt_label.setStyleSheet("border-image: url(./pics/pics/border/gk.png);")
            self.ui.n_a_1.setStyleSheet("border-image: url(./pics/pics/neuron/w.png);")
            self.ui.n_a_2.setStyleSheet("border-image: url(./pics/pics/neuron/g.png);")
            self.ui.n_a_3.setStyleSheet("border-image: url(./pics/pics/neuron/g.png);")
            self.ui.n_a_4.setStyleSheet("border-image: url(./pics/pics/neuron/w.png);")
            self.ui.n_a_5.setStyleSheet("border-image: url(./pics/pics/neuron/g.png);")
            self.ui.n_a_6.setStyleSheet("border-image: url(./pics/pics/neuron/g.png);")
            self.ui.n_a_7.setStyleSheet("border-image: url(./pics/pics/neuron/w.png);")
            self.ui.Prompt_text.setText("The capital of Australia is [MASK]")

class Welcome(QWidget):
    '''
    初始界面
    Start: 加载自定义的激活neuron, 模型构架, 显示激活的Neurons
    Example: 简单演示Prompt的激活原理
    Exit: 退出程序
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = uic.loadUi("welcome.ui",self)
        self.setWindowTitle("Welcome")
        # ---------- 定义跳转界面 ---------- #
        self.Start.clicked.connect(self.onBtnClickStart)        
        self.Example.clicked.connect(self.onBtnClickExample)    
        self.Exit.clicked.connect(self.onBtnClickCloseWin)     
    
    def onBtnClickStart(self):
        self.StartWindow = MainWindow()
        self.StartWindow.show()
        
    def onBtnClickExample(self):
        self.ExampleWindow = Example()
        self.ExampleWindow.show()
        
    def onBtnClickCloseWin(self):      
        appInstance=QApplication.instance()
        appInstance.quit()


# 创建应用实例，通过 sys.argv 传入命令行参数
app = QApplication(sys.argv)
# 创建窗口实例
welcome = Welcome()
welcome.show()
# window = MainWindow()
# 显示窗口
# window.show()
# 执行应用，进入事件循环
app.exec_()