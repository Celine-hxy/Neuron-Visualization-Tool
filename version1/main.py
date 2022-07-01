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
from fonts import *


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
        self.initCombobox()
        self.initNetwork()
    
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
    def load_Neuron(self):
        """
        加载存放激活Neuron的文件夹
        """
        self.neuron_file_dir = QFileDialog.getExistingDirectory() 
        print(self.neuron_file_dir)
    
    def load_Network(self):
        """
        加载Network, 将模型的构架显示在UI界面的左下角, 并调用显示Network函数
        """
        # img_name, _ = QFileDialog.getOpenFileName(self, "打开图片", "", "All Files(*);;*.jpg;;*.png")
        file_name, _ = QFileDialog.getOpenFileName(None, "Open csv file","","*.csv;;All Files(*)")          # ;;All Files(*)
        print(file_name)
        if file_name != '':
            self.network_file = pd.read_csv(str(file_name)) # 有两列，分别为Name和Neuron_Num
            # print(self.network_file)
            self.generateNetwork()          # 显示Network
            self.generateNeuron()           # 根据Network架构生成Neuron
    
    def load_Prompt(self):
        """
        加载Prompt, 并根据得到的Prompt初始化Combo box
        """
        file_name, _ = QFileDialog.getOpenFileName(None, "Open csv file","","*.csv;;All Files(*)")          # ;;All Files(*)
        print(file_name)
        if file_name != '':
            self.prompt_file = pd.read_csv(str(file_name))
            self.prompt_file = np.array(self.prompt_file.values).flatten()
            # print(self.prompt_file)
            self.genergateCombobox()
    
    # ---------- 初始化Combo box ---------- # 
    def initCombobox(self):
        self.ui.Combo_Prompt.clear()
        self.default_prompt_file = pd.read_csv('./Prompt_default.csv')
        self.default_prompt_file = np.array(self.default_prompt_file.values).flatten()
        self.ui.Combo_Prompt.clear()
        for prompt in self.default_prompt_file:
            self.ui.Combo_Prompt.addItem(prompt)    # 将获取的Prompt加到Combo box中
    
    def initNetwork(self):
        self.network_file_default = pd.read_csv('./Network_default.csv') # 有两列，分别为Name和Neuron_Num
        num = self.network_file_default.shape[0]    # 数据行数
        networkLabels = []
        connectionLabels = []
        
        for i in range(num):
            networkLabels.append(QLabel())
            networkLabels[-1].setObjectName(str(self.network_file_default['Name'][i]))
            networkLabels[-1].setText('Layer:'+str(self.network_file_default['Name'][i])+'  Size:'+str(self.network_file_default['Neuron_Num'][i]))
            networkLabels[-1].setFont(font_Layer)
            # networkLabels[-1].setMaximumSize(QtCore.QSize(16777215, 80))
            networkLabels[-1].setStyleSheet("border-image: url(./pics/pics/border/bk.png);")
            networkLabels[-1].setAlignment(Qt.AlignCenter)
            
            connectionLabels.append(QLabel())
            connectionLabels[-1].setObjectName('LayerConnection'+str(i))
            connectionLabels[-1].setText("↑      ↑      ↑      ↑")
            connectionLabels[-1].setFont(font_connection)
            connectionLabels[-1].setAlignment(Qt.AlignCenter)
            
            self.ui.QVL_NetworkArchitecture.addWidget(networkLabels[-1])
            self.ui.QVL_NetworkArchitecture.addWidget(connectionLabels[-1])
        
        # 设置Layout Stretch, Layer:Connection = 2:1
        for j in range(num*2):
            if j % 2 == 0:
                self.ui.QVL_NetworkArchitecture.setStretch(j,2)
            else:
                self.ui.QVL_NetworkArchitecture.setStretch(j,1)
         
    def initMenubar(self):
        self.ui.actionLoad_Neuron_file.triggered.connect(self.load_Neuron)
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
        print(self.neuron_file_dir)
    
    def generateNetwork(self):
        # 清理布局里原来的所有控件
        item_list = list(range(self.ui.QVL_NetworkArchitecture.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.ui.QVL_NetworkArchitecture.itemAt(i)
            self.ui.QVL_NetworkArchitecture.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
        # 添加新的控件
        num = self.network_file.shape[0]    # 数据行数
        networkLabels = []
        connectionLabels = []
        
        for i in range(num):
            networkLabels.append(QLabel())
            networkLabels[-1].setObjectName(str(self.network_file['Name'][i]))
            networkLabels[-1].setText('Layer:'+str(self.network_file['Name'][i])+'  Size:'+str(self.network_file['Neuron_Num'][i]))
            networkLabels[-1].setFont(font_Layer)
            # networkLabels[-1].setMaximumSize(QtCore.QSize(16777215, 80))
            networkLabels[-1].setStyleSheet("border-image: url(./pics/pics/border/bk.png);")
            networkLabels[-1].setAlignment(Qt.AlignCenter)
            
            connectionLabels.append(QLabel())
            connectionLabels[-1].setObjectName('LayerConnection'+str(i))
            connectionLabels[-1].setText("↑      ↑      ↑      ↑")
            connectionLabels[-1].setFont(font_connection)
            connectionLabels[-1].setAlignment(Qt.AlignCenter)
            
            self.ui.QVL_NetworkArchitecture.addWidget(networkLabels[-1])
            self.ui.QVL_NetworkArchitecture.addWidget(connectionLabels[-1])
        
        # 设置Layout Stretch, Layer:Connection = 2:1
        for j in range(num*2):
            if j % 2 == 0:
                self.ui.QVL_NetworkArchitecture.setStretch(j,2)
            else:
                self.ui.QVL_NetworkArchitecture.setStretch(j,1)
        
    def genergateCombobox(self):
        self.ui.Combo_Prompt.clear()
        for prompt in self.prompt_file:
            self.ui.Combo_Prompt.addItem(prompt)    # 将获取的Prompt加到Combo box中

    def generateNeuron(self):
        print(self.network_file)
        
        # 清理布局里原来的所有控件
        item_list = list(range(self.ui.formLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序
        for i in item_list:
            item = self.ui.formLayout.itemAt(i)
            self.ui.formLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
                
                
        # 添加新的控件
        num = self.network_file.shape[0]    # 数据行数
        self.LayerQWidget = []              # 一层, 放层名称LayerName(Label) 和 NeuronQWidget(QWidget)
        self.NeuronQWidget = []
        self.connectionLabels_n = []
        self.NeuronsQLabel = []
        
        for i in range(num):        # num = Layer数目
            # Layer名字放入formLayout中
            # 展示的部件列表
            LayerName = QLabel()
            LayerName.setText(str(self.network_file['Name'][i]))
            LayerName.setFont(font_LayerName)
            LayerName.setAlignment(Qt.AlignCenter)
            
            # 层layer初始化
            self.LayerQWidget.append(QWidget())
            self.LayerQWidget[-1].setObjectName('LayerQWidget_'+str(i))
            self.LayerQWidget[-1].setStyleSheet("background-color: rgb(222, 235, 247);")
            
            NeuronQLabel = []
            for k in range(self.network_file['Neuron_Num'][i]):     # 当前Layer的Neuron数目
                NeuronQLabel.append(QLabel())
                NeuronQLabel[-1].setObjectName('Neuron_'+str(i)+str(k))
                NeuronQLabel[-1].setStyleSheet("image: url(./pics/pics/neuron/w.png);")
                NeuronQLabel[-1].setMaximumSize(QtCore.QSize(100, 100))
                NeuronQLabel[-1].setMinimumSize(QtCore.QSize(50, 50))
            
            layoutQH = QHBoxLayout()
            for k in NeuronQLabel:
                layoutQH.addWidget(k)
  
            self.LayerQWidget[-1].setLayout(layoutQH)
            
            self.ui.formLayout.addRow(LayerName, self.LayerQWidget[-1])
        
        

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