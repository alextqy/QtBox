# -*- coding:utf-8 -*-
from sre_constants import SRE_FLAG_IGNORECASE
from interface._base import *


class LoginFrame(BaseInterface, BaseFrame):
    ReloadSignal = Signal()

    def __init__(self):
        super().__init__()
        self.CleanUpAction()
        self.ExecutionStatus = False  # 设置登陆状态
        self.LoginLayoutH = QHBoxLayout()
        self.LoginLayoutV = QVBoxLayout()

        self.TopLogo = QLabel()
        self.TopLogo.setFixedSize(110, 110)
        self.TopLogo.setPixmap(self.SetIMG(TOPLOGO))
        self.TopLogo.setScaledContents(True)
        self.TopLogo.setAlignment(Qt.AlignCenter)  # 字体居中
        self.TopLogo.setStyleSheet(self.Style.Object.MainWindow_Login_Top_Logo())  # 设置样式

        self.TopLogoLayout = QHBoxLayout()
        self.TopLogoLayout.addWidget(self.TopLogo)

        self.AccountInput = QLineEdit()  # 账号输入
        self.AccountInput.setFixedWidth(300)  # 设置固定宽度
        self.AccountInput.setStyleSheet(self.Style.Object.MainWindow_Login_Input())  # 设置样式
        self.AccountInput.setPlaceholderText(self.Lang.Account)  # 设置提示文字
        self.AccountInput.setToolTip(self.Lang.Account)  # 设置鼠标提示

        self.PWDInput = QLineEdit()  # 密码输入
        self.PWDInput.returnPressed.connect(self.LoginAction)  # 绑定Enter键
        self.PWDInput.setFixedWidth(300)  # 设置固定宽度
        self.PWDInput.setEchoMode(QLineEdit.Password)  # 输入为密码类型
        self.PWDInput.setStyleSheet(self.Style.Object.MainWindow_Login_Input())  # 设置样式
        self.PWDInput.setPlaceholderText(self.Lang.PWD)  # 设置提示文字
        self.PWDInput.setToolTip(self.Lang.PWD)  # 设置鼠标提示

        self.URLLayout = QHBoxLayout()

        self.URLInput = QLineEdit()  # 设置输入控件
        self.URLInput.setFixedWidth(245)  # 设置固定宽度
        self.URLInput.setStyleSheet(self.Style.Object.MainWindow_Login_Input())  # 设置样式
        self.URLInput.setPlaceholderText("IP")  # 设置提示文字
        self.URLInput.setToolTip(self.Lang.IP)  # 设置鼠标提示

        self.HttpsSelect = QComboBox()
        self.HttpsSelect.setToolTip("SSL")
        self.HttpsSelect.setView(QListView())
        self.HttpsSelect.setFixedHeight(38)
        self.HttpsSelect.setFixedWidth(50)
        self.HttpsSelect.setStyleSheet(self.Style.Object.MainFrame_Lang_Box())
        HttpsOptions = [
            " OFF",
            " ON ",
        ]
        self.HttpsSelect.addItems(HttpsOptions)
        self.URLLayout.addWidget(self.URLInput)
        self.URLLayout.addWidget(self.HttpsSelect)

        self.HBtnLayout = QHBoxLayout()

        self.LangSelect = QComboBox()
        self.LangSelect.setView(QListView())
        self.LangSelect.setFixedHeight(35)
        self.LangSelect.setFixedWidth(85)
        self.LangSelect.setStyleSheet(self.Style.Object.MainFrame_Lang_Box())
        LangOptions = [" English", " Español", " Français", " 中文(简体)", " 中文(繁体)"]
        self.LangSelect.addItems(LangOptions)
        self.LangSelect.currentIndexChanged.connect(self.ChangeLang)

        self.LoginButton = QPushButton("  " + self.Lang.SignIn)  # 登录按钮
        self.LoginButton.setShortcut("Enter")  # 绑定Enter按钮
        self.LoginButton.setFixedWidth(210)
        self.LoginButton.setFixedHeight(35)
        self.LoginButton.setStyleSheet(self.Style.Object.MainWindow_Login_Btn())  # 设置样式
        self.LoginButton.clicked.connect(self.LoginAction)  # 连接槽函数
        # self.LoginButton.setIcon(QIcon(SIGNINW))

        self.HBtnLayout.addWidget(self.LangSelect)
        self.HBtnLayout.addWidget(self.LoginButton)

        self.LoginLayoutV.addStretch()  # 填充
        self.LoginLayoutV.addLayout(self.TopLogoLayout)  # 顶部LOGO
        self.LoginLayoutV.addWidget(self.AccountInput)  # 添加控件
        self.LoginLayoutV.addWidget(self.PWDInput)  # 添加控件
        self.LoginLayoutV.addLayout(self.URLLayout)  # 添加控件
        self.LoginLayoutV.addLayout(self.HBtnLayout)  # 添加控件
        self.LoginLayoutV.addStretch()  # 填充

        self.LoginLayoutH.addLayout(self.LoginLayoutV)  # 设置布局
        self.setLayout(self.LoginLayoutH)  # 设置控件

        # ============================================== Ready ==============================================

        self.AccountInput.setText(self.Cache.Get("Account"))
        self.URLInput.setText(self.Cache.Get("URL"))

        if self.Cache.Get("SwitchHttps") == True:
            self.HttpsSelect.setCurrentIndex(1)
        else:
            self.HttpsSelect.setCurrentIndex(0)

        if self.Cache.Get("Lang") == "":
            self.LangSelect.setCurrentIndex(0)
        elif self.Cache.Get("Lang") == "en":
            self.LangSelect.setCurrentIndex(0)
        elif self.Cache.Get("Lang") == "es":
            self.LangSelect.setCurrentIndex(1)
        elif self.Cache.Get("Lang") == "fr":
            self.LangSelect.setCurrentIndex(2)
        elif self.Cache.Get("Lang") == "zh-cn":
            self.LangSelect.setCurrentIndex(3)
        elif self.Cache.Get("Lang") == "zh-tw":
            self.LangSelect.setCurrentIndex(4)
        else:
            self.LangSelect.setCurrentIndex(0)

        # self.LoginAnimation()  # 运行动画

    # 选择事件
    def ChangeLang(self):
        if self.LangSelect.currentIndex() == 0:
            self.Cache.Set("Lang", "en")
        elif self.LangSelect.currentIndex() == 1:
            self.Cache.Set("Lang", "es")
        elif self.LangSelect.currentIndex() == 2:
            self.Cache.Set("Lang", "fr")
        elif self.LangSelect.currentIndex() == 3:
            self.Cache.Set("Lang", "zh-cn")
        elif self.LangSelect.currentIndex() == 4:
            self.Cache.Set("Lang", "zh-tw")
        else:
            return
        self.ReloadSignal.emit()

    # 登录页动效
    def LoginAnimation(self):
        Animation0 = QtCore.QPropertyAnimation(self.TopLogo, b'pos', self)
        Animation0.setKeyValueAt(0, QtCore.QPoint(520, 287))  # 起始位置
        Animation0.setKeyValueAt(1, QtCore.QPoint(520, 125))  # 最后位置
        Animation0.setDuration(500)
        # Animation1.start()

        Animation1 = QtCore.QPropertyAnimation(self.AccountInput, b'pos', self)
        Animation1.setKeyValueAt(0, QtCore.QPoint(426, 331))  # 起始位置
        Animation1.setKeyValueAt(1, QtCore.QPoint(426, 241))  # 最后位置
        Animation1.setDuration(600)
        # Animation1.start()

        Animation2 = QtCore.QPropertyAnimation(self.PWDInput, b'pos', self)
        Animation2.setKeyValueAt(0, QtCore.QPoint(426, 375))  # 起始位置
        Animation2.setKeyValueAt(1, QtCore.QPoint(426, 285))  # 最后位置
        Animation2.setDuration(800)
        # Animation2.start()

        Animation3_1 = QtCore.QPropertyAnimation(self.URLInput, b'pos', self)
        Animation3_1.setKeyValueAt(0, QtCore.QPoint(426, 419))  # 起始位置
        Animation3_1.setKeyValueAt(1, QtCore.QPoint(426, 329))  # 最后位置
        Animation3_1.setDuration(1100)
        # Animation3.start()

        Animation3_2 = QtCore.QPropertyAnimation(self.HttpsSelect, b'pos', self)
        Animation3_2.setKeyValueAt(0, QtCore.QPoint(676, 419))  # 起始位置
        Animation3_2.setKeyValueAt(1, QtCore.QPoint(676, 329))  # 最后位置
        Animation3_2.setDuration(1100)
        # Animation3.start()

        Animation4_1 = QtCore.QPropertyAnimation(self.LangSelect, b'pos', self)
        # Animation4.setStartValue(QtCore.QPoint(516, 463))  # 起始位置
        # Animation4.setEndValue(QtCore.QPoint(426, 373))  # 最后位置
        Animation4_1.setKeyValueAt(0, QtCore.QPoint(516, 470))
        Animation4_1.setKeyValueAt(0.8, QtCore.QPoint(516, 373))
        Animation4_1.setKeyValueAt(1, QtCore.QPoint(426, 373))
        Animation4_1.setDuration(2000)
        Animation4_1.start()

        Animation4_2 = QtCore.QPropertyAnimation(self.LoginButton, b'pos', self)
        Animation4_2.setKeyValueAt(0, QtCore.QPoint(516, 470))  # 起始位置
        Animation4_2.setKeyValueAt(0.8, QtCore.QPoint(516, 373))  # 中间位置
        Animation4_2.setKeyValueAt(1, QtCore.QPoint(516, 373))  # 最后位置
        Animation4_2.setDuration(2000)
        # Animation4.start()

        AnimationGroup = QtCore.QParallelAnimationGroup(self)  # 并行动画
        AnimationGroup.addAnimation(Animation0)
        AnimationGroup.addAnimation(Animation1)
        AnimationGroup.addAnimation(Animation2)
        AnimationGroup.addAnimation(Animation3_1)
        AnimationGroup.addAnimation(Animation3_2)
        AnimationGroup.addAnimation(Animation4_1)
        AnimationGroup.addAnimation(Animation4_2)
        AnimationGroup.start()

    # 登录操作
    def LoginAction(self):
        Account = self.AccountInput.text()
        Password = self.PWDInput.text()
        ServerAddr = self.URLInput.text()
        Type = 1

        if Account == "":
            MSGBOX().ERROR(self.Lang.IncorrectAccount)
            return
        if Password == "":
            MSGBOX().ERROR(self.Lang.IncorrectPassword)
            return
        # if ServerAddr == "":
        #     MSGBOX().ERROR(self.Lang.IncorrectPassword)
        #     return

        self.Cache.Set("Account", Account)  # 设置账号缓存
        self.Cache.Set("TokenType", Type)  # 登录类型

        # 设置HTTPS开关缓存
        if self.HttpsSelect.currentIndex() == 1:
            self.Cache.Set("SwitchHttps", True)
        else:
            self.Cache.Set("SwitchHttps", False)

        # 设置语言缓存
        if self.LangSelect.currentIndex() == 0:
            self.Cache.Set("Lang", "en")
        elif self.LangSelect.currentIndex() == 1:
            self.Cache.Set("Lang", "es")
        elif self.LangSelect.currentIndex() == 2:
            self.Cache.Set("Lang", "fr")
        elif self.LangSelect.currentIndex() == 3:
            self.Cache.Set("Lang", "zh-cn")
        elif self.LangSelect.currentIndex() == 4:
            self.Cache.Set("Lang", "zh-tw")
        else:
            self.Cache.Set("Lang", "en")

        # 是否填写IP地址
        if ServerAddr == "":
            UDPPort = self.Cache.Get("UDPPort")
            try:
                UDPReceived = self.UDPTool.UDPReceive(UDPPort)  # 获取UDP信息
            except Exception as e:
                MSGBOX().ERROR(self.Lang.RequestTimeout)
                return

            if UDPReceived == "null":
                MSGBOX.ERROR(self.Lang.UnableToGetServerAddress)
                return
            else:
                ServerAddr = UDPReceived

        ServerAddr = ServerAddr.replace("http://", "")
        ServerAddr = ServerAddr.replace("https://", "")
        if self.Cache.Get("SwitchHttps") == True:
            ServerAddr = "https://" + ServerAddr
        else:
            ServerAddr = "http://" + ServerAddr

        self.Cache.Set("URL", ServerAddr)  # 设置服务器地址缓存
        self.URLInput.setText(ServerAddr)
        Result = UserAction().SignIn(Account, Password, Type, ServerAddr)
        if Result["State"] == True:
            self.Cache.Set("Token", Result["Token"])  # 记录Token

            UploadDirPath, DownloadDirPath = self.File.SetUserDir(Account, UPLOADDIR, DOWNLOADDIR)  # 设置用户目录
            UserTempDir = self.File.SetDownloadTempDir(Account, DOWNLOADTEMP)  # 设置文件存放路径
            TempDir = self.File.SetTempDir(Account, TEMPDIR)  # 设置临时预览文件夹

            self.Cache.Set("UserUploadPath", UploadDirPath)
            self.Cache.Set("UserDownloadPath", DownloadDirPath)
            self.Cache.Set("UserTempDir", UserTempDir)
            self.Cache.Set("TempDir", TempDir)
            self.CleanUpDeferAction()
            self.ExecutionStatus = True
        else:
            MSGBOX().ERROR(self.Lang.LoginFailed)
            return

        # self.LoginFinishAnimation()

    # 完成登陆动效
    # def LoginFinishAnimation(self):
    #     Animation1 = QtCore.QPropertyAnimation(
    #         self.AccountInput, b'pos', self)
    #     Animation1.setKeyValueAt(0, QtCore.QPoint(426, 241))  # 起始位置
    #     Animation1.setKeyValueAt(1, QtCore.QPoint(426, -241))  # 最后位置
    #     Animation1.setDuration(300)

    #     Animation2 = QtCore.QPropertyAnimation(
    #         self.PWDInput, b'pos', self)
    #     Animation2.setKeyValueAt(0, QtCore.QPoint(426, 285))  # 起始位置
    #     Animation2.setKeyValueAt(1, QtCore.QPoint(426, -285))  # 最后位置
    #     Animation2.setDuration(800)

    #     Animation3 = QtCore.QPropertyAnimation(
    #         self.URLInput, b'pos', self)
    #     Animation3.setKeyValueAt(0, QtCore.QPoint(426, 329))  # 起始位置
    #     Animation3.setKeyValueAt(1, QtCore.QPoint(426, -329))  # 最后位置
    #     Animation3.setDuration(1300)

    #     Animation4 = QtCore.QPropertyAnimation(
    #         self.LoginButton, b'pos', self)
    #     Animation4.setKeyValueAt(0, QtCore.QPoint(426, 373))  # 起始位置
    #     Animation4.setKeyValueAt(1, QtCore.QPoint(426, -473))  # 最后位置
    #     Animation4.setDuration(1800)

    #     # AnimationGroup = QtCore.QSequentialAnimationGroup(self)  # 串行动画
    #     AnimationGroup = QtCore.QParallelAnimationGroup(self)  # 并行动画
    #     AnimationGroup.addAnimation(Animation1)
    #     AnimationGroup.addAnimation(Animation2)
    #     AnimationGroup.addAnimation(Animation3)
    #     AnimationGroup.addAnimation(Animation4)
    #     AnimationGroup.start()
    #     self.ExecutionStatus = True

    # 重新载入输入框以及提示信息
    def ReloadInputLang(self):
        from public.zead import Lang
        Lang = Lang()
        self.AccountInput.setPlaceholderText(Lang.Account)  # 设置提示文字
        self.AccountInput.setToolTip(Lang.Account)  # 设置鼠标提示
        self.PWDInput.setPlaceholderText(Lang.PWD)  # 设置提示文字
        self.PWDInput.setToolTip(Lang.PWD)  # 设置鼠标提示
        self.URLInput.setPlaceholderText("IP")  # 设置提示文字
        self.URLInput.setToolTip(Lang.IP)  # 设置鼠标提示
        self.LoginButton.setText("  " + Lang.SignIn)
