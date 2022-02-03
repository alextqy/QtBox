# -*- coding:utf-8 -*-
from interface._base import *
from interface.DirFileFrame import *
from interface.DepartmentFrame import *
from interface.UserFrame import *
from interface.SysConfFrame import *
from interface.MyDepartmentFrame import *
from interface.UploadListWindow import *
from interface.DownloadListWindow import *
from interface.OfflineTaskListWindow import *
from interface.ActivationWindow import *
from interface.FileTagFrame import *


class MainFrame(BaseInterface, BaseFrame):
    QuitSignal = Signal()

    def __init__(self):
        super().__init__()
        self.TokenRunningStateThread = QThread()

        self.MainLayout = QVBoxLayout()  # 主要布局
        self.MainLayout.setContentsMargins(5, 5, 5, 5)  # 设置边距
        self.TopLayout = QHBoxLayout()  # 头部布局
        self.MidLayout = QHBoxLayout()  # 中间布局
        self.BtmLayout = QHBoxLayout()  # 底部布局

        # ============================================== Data Ready ==============================================

        # 获取个人信息
        Result = UserAction().CheckSelf()
        if Result["State"] == False:
            MSGBOX().ERROR(self.Lang.UnableToGetPersonalInformation)
            self.Quit()
            return
        self.SelfData = Result["Data"]

        # 是否系统管理员
        self.IsMaster = False
        self.CheckMaster = UserAction().IsMaster()
        self.IsMaster = self.CheckMaster["State"]

        MidLQtWidgetsWidth = 180  # 左侧控件宽度
        MidLQtWidgetsHeight = 35  # 左侧控件高度

        # ============================================== TOP ==============================================
        self.TopLabel = TopLabel(self.SelfData["Name"])  # 个人标题
        self.TopLabel.adjustSize()  # 按内容自适应宽度
        self.TopLabel.setMinimumHeight(30)  # 设置固定高度
        self.TopLabel.setMinimumWidth(MidLQtWidgetsWidth + 14)  # 设置固定宽度
        self.TopLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.TopLabel.setStyleSheet(
            self.Style.Object.MainFrame_Top_Label())  # 设置样式
        self.TopLabel.ActionSignal.connect(self.UserInfo)  # 连接槽函数
        self.TopLayout.addWidget(self.TopLabel)  # 加入到布局

        self.TopLayout.addStretch()  # 设置空占位控件

        self.TaskUploadBtn = QPushButton("  " + self.Lang.UploadTask)  # 上传列表
        self.TaskUploadBtn.setAutoFillBackground(True)  # 允许修改背景颜色
        self.TaskUploadBtn.adjustSize()  # 按内容自适应宽度
        self.TaskUploadBtn.setFixedHeight(30)  # 设置固定大小
        self.TaskUploadBtn.setStyleSheet(
            self.Style.Object.MainFrame_Top_Task_Btn()
        )  # 设置样式
        self.TaskUploadBtn.clicked.connect(
            lambda: self.UploadListWindowObject.show()
        )  # 连接槽函数
        self.TaskUploadBtn.setIcon(QIcon(UPLOAD))
        self.TopLayout.addWidget(self.TaskUploadBtn)  # 加入到布局

        self.TaskDownLoadBtn = QPushButton("  " + self.Lang.DownloadTask)
        self.TaskDownLoadBtn.setAutoFillBackground(True)  # 允许修改背景颜色
        self.TaskDownLoadBtn.adjustSize()  # 按内容自适应宽度
        self.TaskDownLoadBtn.setFixedHeight(30)  # 设置固定大小
        self.TaskDownLoadBtn.setStyleSheet(
            self.Style.Object.MainFrame_Top_Task_Btn()
        )  # 设置样式
        self.TaskDownLoadBtn.clicked.connect(
            lambda: self.DownloadListWindowObject.show()
        )  # 连接槽函数
        self.TaskDownLoadBtn.setIcon(QIcon(DOWNLOAD))
        self.TopLayout.addWidget(self.TaskDownLoadBtn)  # 加入到布局

        self.OfflineTaskBtn = QPushButton("  " + self.Lang.OfflineTask)
        self.OfflineTaskBtn.setAutoFillBackground(True)  # 允许修改背景颜色
        self.OfflineTaskBtn.adjustSize()  # 按内容自适应宽度
        self.OfflineTaskBtn.setFixedHeight(30)  # 设置固定大小
        self.OfflineTaskBtn.setStyleSheet(
            self.Style.Object.MainFrame_Top_Task_Btn()
        )  # 设置样式
        self.OfflineTaskBtn.clicked.connect(
            lambda: self.OfflineTaskListWindowObject.show()
        )  # 连接槽函数
        self.OfflineTaskBtn.setIcon(QIcon(OFFLINETASK))
        self.TopLayout.addWidget(self.OfflineTaskBtn)  # 加入到布局

        # ============================================== MID Left ==============================================

        self.MidLayoutL = QVBoxLayout()  # 中间左侧布局
        self.MidLayoutLFrame = QFrame()  # 中间左侧控件
        self.MidLayoutLFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Frame_L()
        )  # 设置样式
        self.MidLayoutLFrame.setFixedWidth(MidLQtWidgetsWidth + 14)  # 设置固定宽度
        self.MidLV = QVBoxLayout()  # 左侧按钮布局
        self.MidLV.setContentsMargins(6, 5, 0, 5)  # 设置边距
        self.MidLV.setSpacing(5)  # 设置垂直间隔

        # ============================================== 动态模块 ==============================================

        if self.SelfData["Account"] != "root":
            if self.SelfData["DepartmentID"] > 0:
                self.MyDepartmentLabel = MyDepartmentLabel(
                    self.Lang.MyDepartment,
                    MidLQtWidgetsWidth,
                    MidLQtWidgetsHeight,
                    self.Style.Object.MainFrame_Mid_Banner_Btn()
                )  # 我的部门
                if self.SelfData["DepartmentID"] > 0:
                    self.MyDepartmentLabel.ActionSignal.connect(
                        lambda: self.ShowControl("MyDepartmentFrame"))  # 连接槽函数
                else:
                    self.MyDepartmentLabel.ActionSignal.connect(
                        lambda: self.ShowError(self.Lang.TheAccountHasNoDepartment))  # 连接槽函数
                self.MidLV.addWidget(self.MyDepartmentLabel)  # 添加到布局

        if self.IsMaster == True:
            self.UserLabel = MainUserLabel(
                self.Lang.UserList,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 用户管理
            self.UserLabel.ActionSignal.connect(
                lambda: self.ShowControl("UserFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.UserLabel)  # 添加到布局

            self.DepartmentLabel = MainDepartmentLabel(
                self.Lang.DepartmentManagement,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 部门管理
            self.DepartmentLabel.ActionSignal.connect(
                lambda: self.ShowControl("DepartmentFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.DepartmentLabel)  # 添加到布局

            self.DirFileLabel = MainDirFileLabel(
                self.Lang.FileManagement,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 文件 文件夹
            self.DirFileLabel.ActionSignal.connect(
                lambda: self.ShowControl("DirFileFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.DirFileLabel)  # 添加到布局

            self.FileTagLabel = MainFileTagLabel(
                self.Lang.FileTag,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 文件标签
            self.FileTagLabel.ActionSignal.connect(
                lambda: self.ShowControl("FileTagFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.FileTagLabel)  # 添加到布局

            self.SysConfLabel = MainSysConfLabel(
                self.Lang.SystemSettings,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 系统设置
            self.SysConfLabel.ActionSignal.connect(
                lambda: self.ShowControl("SysConfFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.SysConfLabel)  # 添加到布局
        else:
            self.DirFileLabel = MainDirFileLabel(
                self.Lang.FileManagement,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 文件 文件夹
            self.DirFileLabel.ActionSignal.connect(
                lambda: self.ShowControl("DirFileFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.DirFileLabel)  # 添加到布局

            self.FileTagLabel = MainFileTagLabel(
                self.Lang.FileTag,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 文件标签
            self.FileTagLabel.ActionSignal.connect(
                lambda: self.ShowControl("FileTagFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.FileTagLabel)  # 添加到布局

            self.UserLabel = UserLabel(
                self.Lang.UserList,
                MidLQtWidgetsWidth,
                MidLQtWidgetsHeight,
                self.Style.Object.MainFrame_Mid_Banner_Btn()
            )  # 用户管理
            self.UserLabel.ActionSignal.connect(
                lambda: self.ShowControl("UserFrame")
            )  # 连接槽函数
            self.MidLV.addWidget(self.UserLabel)  # 添加到布局
        # =====================================================================================================

        self.MidLV.addStretch()  # 底部占位

        self.ActivationBtn = QPushButton("")  # 系统设置
        self.ActivationBtn.setFixedSize(
            MidLQtWidgetsWidth, MidLQtWidgetsHeight
        )  # 设置固定大小
        self.ActivationBtn.clicked.connect(self.ShowActivation)  # 连接槽函数
        self.ActivationBtn.setIcon(QIcon(UNLOCK))
        self.MidLV.addWidget(self.ActivationBtn)  # 添加到布局
        self.SetActivationBtn()

        self.FeedbackBtn = QPushButton("  " + self.Lang.Feedback)  # 系统设置
        self.FeedbackBtn.setFixedSize(
            MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.FeedbackBtn.setStyleSheet(
            self.Style.Object.MainFrame_Exit_Btn())  # 设置样式
        self.FeedbackBtn.clicked.connect(self.ShowFeedback)  # 连接槽函数
        self.FeedbackBtn.setIcon(QIcon(FEEDBACK))
        self.MidLV.addWidget(self.FeedbackBtn)  # 添加到布局

        self.ExitBtn = QPushButton("  " + self.Lang.SignOut)  # 退出按钮
        self.ExitBtn.setFixedSize(
            MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.ExitBtn.setStyleSheet(
            self.Style.Object.MainFrame_Exit_Btn())  # 设置样式
        self.ExitBtn.clicked.connect(self.DoQuit)  # 连接槽函数
        self.ExitBtn.setIcon(QIcon(SIGNOUT))
        self.MidLV.addWidget(self.ExitBtn)  # 添加到布局

        # 添加到布局
        self.MidLayoutLFrame.setLayout(self.MidLV)
        self.MidLayoutL.addWidget(self.MidLayoutLFrame)
        self.MidLayout.addLayout(self.MidLayoutL)

        # ============================================== MID Right ==============================================
        self.MidLayoutR = QVBoxLayout()  # 中间右侧布局
        self.MidLayoutRFrame = QFrame()  # 中间右侧控件
        self.MidLayoutRFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Frame_R()
        )  # 设置样式
        self.MidLayoutRLayout = QHBoxLayout()  # 设置右侧基础布局
        self.MidLayoutRLayout.setContentsMargins(0, 0, 0, 0)  # 设置外边距

        # 添加到布局
        self.MidLayoutRFrame.setLayout(self.MidLayoutRLayout)
        self.MidLayoutR.addWidget(self.MidLayoutRFrame)
        self.MidLayout.addLayout(self.MidLayoutR)

        # ============================================== BTM ==============================================
        self.BtmLayout = QHBoxLayout()  # 底部布局
        self.BtmLabel = BtmLabel("About Us")
        self.BtmLabel.setStyleSheet(
            self.Style.Object.MainFrame_Btm_Label())  # 设置样式
        self.BtmLabel.ActionSignal.connect(self.AboutUS)  # 连接槽函数
        self.BtmLabel.setFixedHeight(25)  # 设置固定高度
        self.BtmLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.BtmLayout.addWidget(self.BtmLabel)  # 添加到布局

        # ============================================== 加载模块 ================================================
        self.MainLayout.addLayout(self.TopLayout)  # 加载顶部控件
        self.MainLayout.addLayout(self.MidLayout)  # 加载中部控件
        self.MainLayout.addLayout(self.BtmLayout)  # 加载底部控件
        self.setLayout(self.MainLayout)  # 添加到布局
        self.InitAnimation()  # 执行动效

        # ============================================== Ready ==============================================

        # 实例化常驻控件
        self.CheckMyself = CheckMyself(self.SelfData)
        self.UploadListWindowObject = UploadListWindow()
        self.DownloadListWindowObject = DownloadListWindow()
        self.OfflineTaskListWindowObject = OfflineTaskListWindow()
        self.ActivationWindowObject = ActivationWindow()
        self.ActivationWindowObject.ActionSignal.connect(self.SetActivationBtn)
        self.FeedbackWindowObject = FeedbackWindow()
        self.AboutUSWindowObject = AboutUSWindow()

        self.InitLeftModule()
        self.TokenRunningStateAction()

    # 顶部动效
    def InitAnimation(self):
        Animation1 = QtCore.QPropertyAnimation(
            self.TopLabel, b"pos", self)  # 实例化动效对象
        Animation1.setKeyValueAt(0, QtCore.QPoint(5, -20))  # 起始位置
        Animation1.setKeyValueAt(1, QtCore.QPoint(5, 5))  # 最后位置
        Animation1.setDuration(800)  # 执行时长
        AnimationGroup = QtCore.QParallelAnimationGroup(self)  # 并行动画
        AnimationGroup.addAnimation(Animation1)  # 添加到执行方法
        AnimationGroup.start()

    # 实例化常驻非窗体控件
    def InitLeftModule(self):
        self.LeftFrameLayout = QVBoxLayout()

        self.UserFrameObject = UserFrame()
        self.UserFrameObject.hide()
        self.LeftFrameLayout.addWidget(self.UserFrameObject)

        self.DepartmentFrameObject = DepartmentFrame()
        self.DepartmentFrameObject.hide()
        self.LeftFrameLayout.addWidget(self.DepartmentFrameObject)

        self.SysConfFrameObject = SysConfFrame()
        self.SysConfFrameObject.hide()
        self.LeftFrameLayout.addWidget(self.SysConfFrameObject)

        self.MyDepartmentFrameObject = MyDepartmentFrame(
            self.SelfData["DepartmentID"])
        self.MyDepartmentFrameObject.DownloadSignal.connect(self.DoDownload)
        self.MyDepartmentFrameObject.hide()
        self.LeftFrameLayout.addWidget(self.MyDepartmentFrameObject)

        self.FileTagFrameObject = FileTagFrame()
        self.FileTagFrameObject.DownloadSignal.connect(self.DoDownload)
        self.FileTagFrameObject.hide()
        self.LeftFrameLayout.addWidget(self.FileTagFrameObject)

        self.DirFileFrameObject = DirFileFrame()
        self.DirFileFrameObject.UploadSignal.connect(self.DoUpload)
        self.DirFileFrameObject.DownloadSignal.connect(self.DoDownload)
        self.DirFileFrameObject.RefreshFileTagListSignal.connect(
            self.FileTagFrameObject.InsertFileListData)
        self.DirFileFrameObject.hide()
        self.LeftFrameLayout.addWidget(self.DirFileFrameObject)

        self.MidLayoutRLayout.addLayout(self.LeftFrameLayout)

    # 登录监控
    def TokenRunningStateAction(self):
        self.TokenRunningStateWorker = TokenRunningStateWorker()
        self.TokenRunningStateWorker.ActionSignal.connect(self.DoQuit)
        self.TokenRunningStateWorker.FinishSignal.connect(
            self.KillThread(self.TokenRunningStateThread)
        )
        self.TokenRunningStateWorker.moveToThread(self.TokenRunningStateThread)
        self.TokenRunningStateThread.started.connect(
            self.TokenRunningStateWorker.Run)
        self.TokenRunningStateThread.start()

    # ============================================== 模块链接 ==============================================

    # 展示用户详情窗口
    def UserInfo(self):
        self.CheckMyself.ActionSignal.connect(self.TopLabel.setText)
        self.CheckMyself.show()

    # 上传列表
    # def UploadListWindow(self):
    #     self.UploadListWindowObject.show()

    # 下载列表
    # def DownloadListWindow(self):
    #     self.DownloadListWindowObject.show()

    # 离线任务列表
    # def OfflineTaskListWindow(self):
    #     self.OfflineTaskListWindowObject.show()

    # 激活
    def ShowActivation(self):
        self.ActivationWindowObject.show()

    # 反馈
    def ShowFeedback(self):
        self.FeedbackWindowObject.show()

    # 关于我们
    def AboutUS(self):
        self.AboutUSWindowObject.show()

    # 退出程序
    def DoQuit(self):
        self.QuitSignal.emit()

    # ============================================== 模块方法 ==============================================

    # 上传
    def DoUpload(self, FilesPath=[], DirID=0):
        self.UploadListWindowObject.ActionSignal.connect(
            self.UploadListWindowObject.DOUploadInThread(FilesPath, DirID)
        )

    # 下载
    def DoDownload(self, FileIDList):
        self.DownloadListWindowObject.ActionSignal.connect(
            self.DownloadListWindowObject.DODownloadInThread(FileIDList)
        )

    # 左侧展示控制
    def ShowControl(self, ModuleKey=""):
        self.FrameObject = None
        if ModuleKey == "":
            return
        elif ModuleKey == "DirFileFrame":
            self.DirFileFrameObject.show()
            self.UserFrameObject.hide()
            self.DepartmentFrameObject.hide()
            self.SysConfFrameObject.hide()
            self.MyDepartmentFrameObject.hide()
            self.FileTagFrameObject.hide()
            self.FrameObject = self.DirFileFrameObject
        elif ModuleKey == "UserFrame":
            self.DirFileFrameObject.hide()
            self.UserFrameObject.show()
            self.DepartmentFrameObject.hide()
            self.SysConfFrameObject.hide()
            self.MyDepartmentFrameObject.hide()
            self.FileTagFrameObject.hide()
            self.FrameObject = self.UserFrameObject
        elif ModuleKey == "DepartmentFrame":
            self.DirFileFrameObject.hide()
            self.UserFrameObject.hide()
            self.DepartmentFrameObject.show()
            self.SysConfFrameObject.hide()
            self.MyDepartmentFrameObject.hide()
            self.FileTagFrameObject.hide()
            self.FrameObject = self.DepartmentFrameObject
        elif ModuleKey == "SysConfFrame":
            self.DirFileFrameObject.hide()
            self.UserFrameObject.hide()
            self.DepartmentFrameObject.hide()
            self.SysConfFrameObject.show()
            self.MyDepartmentFrameObject.hide()
            self.FileTagFrameObject.hide()
            self.FrameObject = self.SysConfFrameObject
        elif ModuleKey == "MyDepartmentFrame":
            self.DirFileFrameObject.hide()
            self.UserFrameObject.hide()
            self.DepartmentFrameObject.hide()
            self.SysConfFrameObject.hide()
            self.MyDepartmentFrameObject.show()
            self.FileTagFrameObject.hide()
            self.FrameObject = self.MyDepartmentFrameObject
        elif ModuleKey == "FileTagFrame":
            self.DirFileFrameObject.hide()
            self.UserFrameObject.hide()
            self.DepartmentFrameObject.hide()
            self.SysConfFrameObject.hide()
            self.MyDepartmentFrameObject.hide()
            self.FileTagFrameObject.show()
            self.FrameObject = self.FileTagFrameObject
        else:
            return

    # 错误提示
    def ShowError(self, Content):
        MSGBOX().ERROR(Content)

    # 是否激活
    def IsItActivated(self):
        Result = ConfigAction().AccountNumberStatistics()
        if Result["State"] != True:
            return False
        else:
            Data = Result["Data"]
            DataArr = Common().Explode("_", Data)
            if int(DataArr[1]) != 5:
                return True
            else:
                return False

    # 设置激活按钮样式
    def SetActivationBtn(self):
        CheckIsItActivated = self.IsItActivated()  # 是否激活
        ActivationBtnText = ""
        ActivationBtnStyle = ""
        if CheckIsItActivated == True:
            ActivationBtnText = self.Lang.ActivateMoreAccounts
            ActivationBtnStyle = self.Style.Object.MainFrame_Activation_Btn_Pro()
        else:
            ActivationBtnText = self.Lang.Activation
            ActivationBtnStyle = self.Style.Object.MainFrame_Activation_Btn()
        self.ActivationBtn.setText("  " + ActivationBtnText)  # 设置文字
        self.ActivationBtn.setStyleSheet(ActivationBtnStyle)  # 设置样式


# 顶部控件
class TopLabel(QLabel):
    ActionSignal = Signal(int)  # 设置信号

    def __init__(self, Text, UserID=0):
        super().__init__()
        self.setText(Text)
        self.UserID = UserID

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit(self.UserID)  # 发送信号


# 文件管理
class MainDirFileLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text, MidLQtWidgetsWidth, MidLQtWidgetsHeight, StyleObj):
        super().__init__()
        self.setText(Text)
        self.setFixedSize(MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.setAlignment(Qt.AlignCenter)  # 字体居中
        self.setStyleSheet(StyleObj)  # 设置样式

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 文件标签
class MainFileTagLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text, MidLQtWidgetsWidth, MidLQtWidgetsHeight, StyleObj):
        super().__init__()
        self.setText(Text)
        self.setFixedSize(MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.setAlignment(Qt.AlignCenter)  # 字体居中
        self.setStyleSheet(StyleObj)  # 设置样式

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 用户列表
class MainUserLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text, MidLQtWidgetsWidth, MidLQtWidgetsHeight, StyleObj):
        super().__init__()
        self.setText(Text)
        self.setFixedSize(MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.setAlignment(Qt.AlignCenter)  # 字体居中
        self.setStyleSheet(StyleObj)  # 设置样式

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 部门管理
class MainDepartmentLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text, MidLQtWidgetsWidth, MidLQtWidgetsHeight, StyleObj):
        super().__init__()
        self.setText(Text)
        self.setFixedSize(MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.setAlignment(Qt.AlignCenter)  # 字体居中
        self.setStyleSheet(StyleObj)  # 设置样式

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 系统设置
class MainSysConfLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text, MidLQtWidgetsWidth, MidLQtWidgetsHeight, StyleObj):
        super().__init__()
        self.setText(Text)
        self.setFixedSize(MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.setAlignment(Qt.AlignCenter)  # 字体居中
        self.setStyleSheet(StyleObj)  # 设置样式

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 我的部门
class MyDepartmentLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text, MidLQtWidgetsWidth, MidLQtWidgetsHeight, StyleObj):
        super().__init__()
        self.setText(Text)
        self.setFixedSize(MidLQtWidgetsWidth, MidLQtWidgetsHeight)  # 设置固定大小
        self.setAlignment(Qt.AlignCenter)  # 字体居中
        self.setStyleSheet(StyleObj)  # 设置样式

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 个人信息窗口
class CheckMyself(BaseInterface, BaseDialog):
    ActionSignal = Signal(str)  # 设置信号

    def __init__(self, UserData):
        super().__init__()
        self.AppMode()  # 设置窗口模式
        self.setFixedSize(220, 335)  # 设置窗口大小
        self.UserData = UserData
        self.Avatar = self.UserData["Avatar"]

        VLayout = QVBoxLayout()  # 设置主布局
        VLayout.setContentsMargins(5, 5, 5, 5)  # 设置边距

        self.AvatarLayout = QHBoxLayout()  # 设置横向布局

        self.AvatarLabel = AvatarLabel("")  # 默认展示内容
        self.AvatarLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.AvatarLabel.setFixedSize(125, 120)  # 固定大小
        self.AvatarLabel.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Label()
        )  # 设置样式
        self.AvatarLabel.setScaledContents(True)  # 图片自适应
        self.AvatarLabel.ActionSignal.connect(self.DoAvatarUpload)  # 链接槽函数
        self.AvatarLabel.setToolTip(self.Lang.Avatar)  # 设置鼠标提示
        self.AvatarLayout.addWidget(self.AvatarLabel)  # 添加控件到布局

        self.TextLabel = QLabel("100 X 100 ico")
        self.TextLabel.setFixedHeight(20)
        self.TextLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.TextLabel.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Avatar_Label()
        )  # 设置样式

        self.AccountInput = QLineEdit()  # 账号输入
        self.AccountInput.setText(self.UserData["Account"])  # 设置内容
        self.AccountInput.setEnabled(False)  # 不允许编辑
        self.AccountInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        )  # 内容居中
        self.AccountInput.setPlaceholderText(self.Lang.Account)  # 设置空内容提示
        self.AccountInput.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Input()
        )  # 设置样式
        self.AccountInput.setToolTip(self.Lang.Account)  # 设置鼠标提示

        self.NameInput = QLineEdit()  # 姓名输入
        self.NameInput.setText(self.UserData["Name"])  # 设置内容
        self.NameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        )  # 内容居中
        self.NameInput.setPlaceholderText(self.Lang.Name)  # 设置空内容提示
        self.NameInput.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Input()
        )  # 设置样式
        self.NameInput.setToolTip(self.Lang.Name)  # 设置鼠标提示

        self.PasswordInput = QLineEdit()  # 密码输入
        self.PasswordInput.setEchoMode(QLineEdit.Password)  # 输入为密码类型
        self.PasswordInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        )  # 内容居中
        self.PasswordInput.setPlaceholderText(self.Lang.PWD)
        self.PasswordInput.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Input()
        )
        self.PasswordInput.setToolTip(self.Lang.PWD)  # 设置鼠标提示

        self.PasswordInput_ = QLineEdit()
        self.PasswordInput_.setEchoMode(QLineEdit.Password)  # 输入为密码类型
        self.PasswordInput_.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        )  # 内容居中
        self.PasswordInput_.setPlaceholderText(self.Lang.Repeat)
        self.PasswordInput_.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Input()
        )
        self.PasswordInput_.setToolTip(self.Lang.Repeat)  # 设置鼠标提示

        self.Btn = QPushButton(self.Lang.Submit)
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_CheckMyself_Btn())
        self.Btn.clicked.connect(lambda: self.DoModify())

        VLayout.addLayout(self.AvatarLayout)
        VLayout.addWidget(self.TextLabel)
        VLayout.addWidget(self.AccountInput)
        VLayout.addWidget(self.NameInput)
        VLayout.addWidget(self.PasswordInput)
        VLayout.addWidget(self.PasswordInput_)
        VLayout.addWidget(self.Btn)

        # 加载图像到Label
        if self.UserData["Avatar"] != "":
            AvatarByte = QByteArray.fromBase64(
                self.UserData["Avatar"].encode("utf8")
            )  # 读取二进制信息
            QPObject = QPixmap()  # 实例化图像处理类
            QPObject.loadFromData(AvatarByte)  # 加载到类

            IMG = QPObject.scaled(100, 100, Qt.KeepAspectRatio)  # 按比例缩放
            # IMG = AvatarFile.scaled(100, 100, Qt.IgnoreAspectRatio)  # 不按比例缩放
            self.AvatarLabel.setPixmap(self.SetIMG(IMG))

        self.setLayout(VLayout)

    def DoAvatarUpload(self):
        TheFile, _ = QFileDialog.getOpenFileName(self)  # 文件选择框
        if TheFile != "":
            TheFileSize = self.File.CheckFileSize(TheFile)
            # if self.File.CheckFileType(TheFile) != "ico":
            #     MSGBOX().ERROR(self.Lang.WrongFileType)
            #     return

            if TheFileSize > (1024 * 1024 * 2):
                MSGBOX().ERROR(self.Lang.FileSizeTooLarge)
                return

            AvatarFile = QPixmap(TheFile)
            # IMG = AvatarFile.scaled(100, 100, Qt.KeepAspectRatio)  # 按比例缩放
            IMG = AvatarFile.scaled(100, 100, Qt.IgnoreAspectRatio)  # 不按比例缩放
            self.AvatarLabel.setPixmap(self.SetIMG(IMG))
            self.Avatar = self.Common.IMGToBase64(TheFile)

    def DoModify(self):
        Password = self.PasswordInput.text()
        Password_ = self.PasswordInput_.text()
        if Password != Password_:
            MSGBOX().ERROR(self.Lang.IncorrectPassword)
            return

        if str.strip(self.NameInput.text()) == "":
            MSGBOX().ERROR(self.Lang.WrongInput)
            return

        self.UserData["Name"] = self.NameInput.text()
        self.UserData["Password"] = Password
        self.UserData["Avatar"] = self.Avatar

        Result = UserAction().UserModify(
            self.UserData["Name"],
            self.UserData["Password"],
            self.UserData["Avatar"],
            self.UserData["Wallpaper"],
            self.UserData["Admin"],
            self.UserData["Status"],
            self.UserData["Permission"],
            self.UserData["Master"],
            self.UserData["DepartmentID"],
        )

        if Result["State"] == True:
            self.ActionSignal.emit(self.NameInput.text())
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)


# 头像上传控件
class AvatarLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 反馈窗口
class FeedbackWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()  # 设置信号
    ResultSignal = Signal()
    SendMailThread = QThread()

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setFixedSize(450, 300)

        VLayout = QVBoxLayout()
        VLayout.setContentsMargins(5, 5, 5, 5)

        self.Input = QTextEdit()
        self.Input.setPlaceholderText(self.Lang.OpinionsOrSuggestions)
        self.Input.setStyleSheet(
            self.Style.Object.MainFrame_Feedback_Window_Input())

        HLayout = QHBoxLayout()

        self.Btn1 = QPushButton("  " + self.Lang.Submit)
        self.Btn1.setFixedHeight(30)
        self.Btn1.setStyleSheet(
            self.Style.Object.MainFrame_Feedback_Window_Btn())
        self.Btn1.clicked.connect(self.SendMail)
        self.Btn1.setIcon(QIcon(SUBMIT))
        HLayout.addWidget(self.Btn1)

        self.Btn2 = QPushButton("  " + self.Lang.Clear)
        self.Btn2.setFixedHeight(30)
        self.Btn2.setFixedWidth(100)
        self.Btn2.setStyleSheet(
            self.Style.Object.MainFrame_Feedback_Window_Btn())
        self.Btn2.clicked.connect(self.Input.clear)
        self.Btn2.setIcon(QIcon(CLEAR))
        HLayout.addWidget(self.Btn2)

        VLayout.addWidget(self.Input)
        VLayout.addLayout(HLayout)
        self.setLayout(VLayout)

    # 发送邮件
    def SendMail(self):
        Content = self.Input.toPlainText()
        if str.strip(Content) == "":
            return
        self.SendMailWorker = SendMailWorker(Content)
        self.SendMailWorker.ResultSignal.connect(self.ReferAction)
        self.SendMailWorker.FinishSignal.connect(
            self.KillThread(self.SendMailThread))
        self.SendMailWorker.moveToThread(self.SendMailThread)
        self.SendMailThread.started.connect(self.SendMailWorker.Run)  # 设置执行方法
        self.SendMailThread.start()  # 线程启动

    def ReferAction(self, Result):
        if Result == True:
            self.Input.clear()
            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)


# 邮件操作
class SendMailWorker(BaseInterface, BaseObject):
    ResultSignal = Signal(bool)

    def __init__(self, Content):
        super().__init__()
        self.Content = Content

    def Run(self):
        Result = self.Common.SendMail(self.Content)
        self.ResultSignal.emit(Result)
        self.FinishSignal.emit()


# 底部控件
class BtmLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 关于我们
class AboutUSWindow(BaseInterface, BaseDialog):
    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setFixedSize(220, 120)

        VLayout = QVBoxLayout()
        VLayout.setContentsMargins(5, 5, 5, 5)

        self.AboutUSLabel = QLabel(
            """
            Contact Us:<br/>
            alextqy@gmail.com<br/>
            285150667@qq.com<br/>
            © 2021 Bit factory
        """
        )
        self.AboutUSLabel.setAlignment(Qt.AlignCenter)
        self.AboutUSLabel.setStyleSheet(
            self.Style.Object.MainFrame_AboutUS_Window_Label()
        )

        VLayout.addWidget(self.AboutUSLabel)
        self.setLayout(VLayout)


# 登录状态监控
class TokenRunningStateWorker(BaseInterface, BaseObject):
    ActionSignal = Signal()

    def __init__(self):
        super().__init__()

    def Run(self):
        while True:
            sleep(1)
            Result = UserAction().TokenRunningState()
            if Result["State"] != True:
                self.ActionSignal.emit()
                break
