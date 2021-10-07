# -*- coding:utf-8 -*-
from interface._base import *
from interface.LoginFrame import *
from interface.MainFrame import *


class Test(BaseInterface, BaseObject):  # 测试worker
    TestSignal = Signal()

    def __init__(self, Param):
        super().__init__()
        self.Check = Param

    def Run(self):
        while True:
            sleep(1)
            print(self.Check.geometry().x(),
                  self.Check.geometry().y())


class MainWindow(BaseInterface, BaseMainWindow):  # 主界面
    ReloadSignalMain = Signal()

    def __init__(self):
        super().__init__()
        self.File.MkDir(os.getcwd() + "/temp/")
        self.File.MkDir(os.getcwd() + "/" + UPLOADDIR)
        self.File.MkDir(os.getcwd() + "/" + DOWNLOADDIR)
        self.File.MkDir(os.getcwd() + "/" + DOWNLOADTEMP)
        self.File.MkDir(os.getcwd() + "/" + TEMPDIR)

        # self.ShowMinMaxBtnOnly() # 隐藏关闭按钮
        self.setMinimumSize(self.SW * 0.6, self.SH * 0.6)  # 设置窗口大小
        self.setStyleSheet(self.Style.Object.MainWindow())

        self.CenterWidget = QtWidgets.QWidget()  # 设置窗口的中央部件
        self.CenterWidget.setContentsMargins(0, 0, 0, 0)  # 设置边距
        self.CenterLayout = QtWidgets.QVBoxLayout()  # 設置主佈局
        self.CenterLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中
        self.CenterLayout.setContentsMargins(0, 0, 0, 0)  # 设置边距

        self.LoginFrame = LoginFrame()  # 加载登陆界面
        self.LoginFrame.ReloadSignal.connect(self.AppReload)
        self.CheckLoginStatus()  # 执行登陆监控线程
        self.CenterLayout.addWidget(self.LoginFrame)  # 设置控件

        self.ReloadSignalMain.connect(self.LoginFrame.ReloadInputLang)

        self.CenterWidget.setLayout(self.CenterLayout)  # 设置佈局
        self.setCentralWidget(self.CenterWidget)  # 添加中央控件

        # self.Test(self.LoginFrame.TopLogo)

    def AppReload(self):  # 重载登录界面
        self.ReloadSignalMain.emit()
        self.hide()
        sleep(0.3)
        self.show()

    def CheckLoginStatus(self):  # 登陆状态监控
        self.LoginThread = QThread()  # 实例化线程
        self.MainWindowWorker = MainWindowWorker(self.LoginFrame)  # 实例化worker
        self.MainWindowWorker.LoginOverSignal.connect(
            self.LoginFrame.hide)  # 链接槽函数 隐藏登录框体
        self.MainWindowWorker.LoadMainFrameSignal.connect(
            self.LoadMainFrame)  # 链接槽函数 展示主框体
        self.MainWindowWorker.FinishSignal.connect(
            self.KillThread(self.LoginThread))  # 链接槽函数 结束线程
        self.MainWindowWorker.moveToThread(self.LoginThread)  # 异步执行
        self.LoginThread.started.connect(self.MainWindowWorker.Run)  # 设置执行方法
        self.LoginThread.start()  # 线程启动

    def LoadMainFrame(self):
        self.MainFrame = MainFrame()  # 加载主界面
        self.MainFrame.QuitSignal.connect(self.Quit)
        self.CenterLayout.addWidget(self.MainFrame)  # 设置控件

    def Test(self, param):  # 测试线程
        self.TestThread = QThread()
        self.DoTest = Test(param)
        self.DoTest.moveToThread(self.TestThread)
        self.TestThread.started.connect(self.DoTest.Run)  # 设置执行方法
        self.TestThread.start()  # 线程启动


class MainWindowWorker(BaseInterface, BaseObject):
    LoginOverSignal = Signal()
    LoadMainFrameSignal = Signal()

    def __init__(self, LoginFrame):
        super().__init__()
        self.LoginFrame = LoginFrame

    def Run(self):
        sleep(0.1)
        while True:
            if self.LoginFrame.ExecutionStatus == True:
                self.LoginOverSignal.emit()
                self.LoadMainFrameSignal.emit()
                self.FinishSignal.emit()
                return
