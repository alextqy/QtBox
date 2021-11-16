# -*- coding:utf-8 -*-
from interface._base import *


class UserFrame(BaseInterface, BaseFrame):
    def __init__(self):
        super().__init__()

        # =========================================== Ready ===========================================
        SelectUserData = UserAction().SelectUser(-1)
        if SelectUserData["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        DataList = SelectUserData["Data"]
        DataLen = len(DataList)
        self.UserData = []
        if DataLen > 0:
            for i in range(DataLen):
                if DataList[i]["Account"] != self.Cache.Get("Account"):
                    self.UserData.append(DataList[i])

        self.IsMaster = UserAction().IsMaster()["State"]
        self.CurrentUserID = 0

        Result = UserAction().CheckSelf()
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        self.MyInfo = Result["Data"]
        self.MyID = self.MyInfo["ID"]
        self.MyName = self.MyInfo["Name"]

        self.TooltipWindow = TooltipWindow()  # 信息提示窗口
        self.Cache.Set("MessageCount", 0)  # 初始化当日信息数量

        self.TooltipThread = QThread()  # 提示窗线程
        self.InfoTipThread = QThread()  # 新信息提示线程

        # =========================================== 用户 ===========================================
        self.UserVS = self.VS()

        # 用户标题栏
        self.UserHeader = UserLabel(self.Lang.UserList)
        self.UserHeader.setFixedHeight(20)
        self.UserHeader.setAlignment(Qt.AlignCenter)  # 字体居中
        self.UserHeader.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Header())  # 设置样式
        self.UserHeader.ActionSignal.connect(
            self.AccountNumberStatisticsAction)

        # 用户列表
        self.UserTree = BaseTreeWidget()
        self.UserTree.setMaximumWidth(300)
        self.UserTree.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Tree_Widget())  # 设置样式
        self.UserTree.HideVScroll()  # 隐藏纵向滚动条
        self.UserTree.setColumnCount(2)  # 设置列数
        self.UserTree.hideColumn(1)  # 隐藏列
        self.UserTree.setHeaderLabels(["User", "ID"])  # 设置标题栏
        self.UserTree.setHeaderHidden(True)  # 隐藏标题栏

        if len(self.UserData) > 0:
            UserTreeItems = []
            for i in range(len(self.UserData)):
                item = QTreeWidgetItem()  # 设置item控件
                # item.setIcon(0, QtGui.QIcon(os.getcwd() + "/avatar.png"))
                item.setText(0, self.UserData[i]["Name"])  # 设置内容
                item.setText(1, str(self.UserData[i]["ID"]))  # 设置内容
                item.setTextAlignment(
                    0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(
                    1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                UserTreeItems.append(item)  # 添加到item list
            self.UserTree.insertTopLevelItems(0, UserTreeItems)  # 添加到用户列表

        # 鼠标左键点击事件
        self.UserTree.clicked.connect(self.UserItemClicked)

        # 鼠标右键 链接槽函数
        self.UserTree.Connect(self.UserRightContextMenuExec)

        # 用户列表下方按钮
        self.UserListBtnFrame = QFrame()
        self.UserListBtnFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_List_Btn_Frame())
        self.UserListBtnFrame.setFixedHeight(70)
        self.UserListBtnFrame.setContentsMargins(0, 0, 0, 0)

        self.UserListBtnLayout = QVBoxLayout()
        self.UserListBtnLayout.setContentsMargins(0, 0, 0, 0)

        if self.IsMaster == True:
            self.UserBtn = QHBoxLayout()
            self.UserBtn.setContentsMargins(0, 0, 0, 0)

            self.NewUserBtn = QPushButton(self.Lang.NewUser)
            self.NewUserBtn.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_List_Btn())
            self.NewUserBtn.setFixedHeight(70)
            self.NewUserBtn.clicked.connect(self.CreateUserWindow)
            self.NewUserBtn.setContentsMargins(0, 0, 0, 0)
            self.UserBtn.addWidget(self.NewUserBtn)

            self.UserBtnV = QVBoxLayout()
            self.UserBtnV.setContentsMargins(0, 0, 0, 0)

            self.ImportUsersBtn = QPushButton(self.Lang.ImportUsers)
            self.ImportUsersBtn.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_List_Btn())
            self.ImportUsersBtn.setFixedHeight(35)
            self.ImportUsersBtn.clicked.connect(self.ImportUsers)
            self.UserBtnV.addWidget(self.ImportUsersBtn)

            self.CheckDemoBtn = QPushButton("Demo")
            self.CheckDemoBtn.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_List_Btn())
            self.CheckDemoBtn.setFixedHeight(35)
            self.CheckDemoBtn.clicked.connect(self.CheckDemo)
            self.UserBtnV.addWidget(self.CheckDemoBtn)

            self.UserBtn.addLayout(self.UserBtnV)

            self.UserListBtnFrame.setLayout(self.UserBtn)

        self.UserVS.addWidget(self.UserHeader)
        self.UserVS.addWidget(self.UserTree)
        self.UserVS.addWidget(self.UserListBtnFrame)

        # =========================================== 信息 ===========================================
        self.MessageVS = self.VS()

        # 信息标题栏
        self.MessageHeader = QLabel(
            self.Lang.MessageList + " < " + self.Common.TodayStr()[:10] + " >")
        self.MessageHeader.setFixedHeight(20)
        self.MessageHeader.setAlignment(Qt.AlignCenter)  # 字体居中
        self.MessageHeader.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Header())  # 设置样式

        self.SA = QListWidget()
        self.SA.setContentsMargins(0, 0, 0, 0)
        self.SA.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Message_List())
        self.SA.setSpacing(10)  # 行间距

        # # 信息发送编辑布局
        self.MessageInputFrame = QFrame()
        self.MessageInputFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Message_Frame())
        self.MessageInputFrame.setFixedHeight(70)
        self.MessageInputFrame.setContentsMargins(0, 0, 0, 0)

        self.MessageInputLayout = QVBoxLayout()
        self.MessageInputLayout.setContentsMargins(0, 0, 0, 0)

        self.MessageInput = QLineEdit()
        self.MessageInput.returnPressed.connect(self.NewMessage)  # 绑定Enter键
        self.MessageInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Message_Input())
        self.MessageInput.setPlaceholderText(self.Lang.NewMessage)
        self.MessageInput.setFixedHeight(30)
        self.MessageInput.setContentsMargins(0, 0, 0, 0)

        self.SubmitBtn = QPushButton(self.Lang.Submit)
        self.SubmitBtn.setShortcut("Enter")  # 绑定Enter按钮
        self.SubmitBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Message_List_Btn())
        self.SubmitBtn.setContentsMargins(0, 0, 0, 0)
        self.SubmitBtn.setFixedHeight(30)
        self.SubmitBtn.clicked.connect(self.NewMessage)

        self.ClearBtn = QPushButton(self.Lang.Clear)
        self.ClearBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Message_List_Btn())
        self.ClearBtn.setContentsMargins(0, 0, 0, 0)
        self.ClearBtn.setFixedHeight(30)
        self.ClearBtn.clicked.connect(lambda: self.MessageInput.setText(""))

        self.HistoryBtn = QPushButton(self.Lang.History)
        self.HistoryBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Message_List_Btn())
        self.HistoryBtn.setContentsMargins(0, 0, 0, 0)
        self.HistoryBtn.setFixedHeight(30)
        self.HistoryBtn.clicked.connect(self.HistoryWindow)

        self.BtnLayout = QHBoxLayout()
        self.BtnLayout.setContentsMargins(0, 0, 0, 0)
        self.BtnLayout.addStretch()
        self.BtnLayout.addWidget(self.SubmitBtn)
        self.BtnLayout.addWidget(self.ClearBtn)
        self.BtnLayout.addWidget(self.HistoryBtn)

        self.MessageInputLayout.addWidget(self.MessageInput)
        self.MessageInputLayout.addLayout(self.BtnLayout)
        self.MessageInputFrame.setLayout(self.MessageInputLayout)

        self.MessageVS.addWidget(self.MessageHeader)
        self.MessageVS.addWidget(self.SA)
        self.MessageVS.addWidget(self.MessageInputFrame)

        # ============================================================================================
        # 分割线
        self.MidRS = self.HS()
        self.MidRS.setContentsMargins(0, 0, 0, 0)
        self.MidRS.addWidget(self.UserVS)
        self.MidRS.addWidget(self.MessageVS)

        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.MidRS)
        self.setLayout(MainLayout)

        # ============================================================================================
        self.InfoTipAction()  # 消息提示

    # 用户列表右键
    def UserRightContextMenuExec(self, pos):
        self.UserTreeMenu = BaseMenu()  # 左侧用户列表鼠标右键菜单
        self.UserTreeMenu.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Tree_Menu())  # 设置样式
        Item = self.UserTree.currentItem()  # 获取被点击行控件
        ItemAt = self.UserTree.itemAt(pos)  # 获取点击焦点

        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            self.UserTreeMenu.AddAction(
                self.Lang.UserDetails, lambda: self.UserInfoWindow(Item))
            if self.IsMaster == True:
                self.UserTreeMenu.AddAction(
                    self.Lang.Delete, lambda: self.RemoveAction(Item))  # 移除用户
        else:  # 焦点外
            return

        self.UserTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.UserTreeMenu.show()  # 展示

    # 用户详情
    def UserInfoWindow(self, Item):
        self.UserInfoWindowObject = UserInfoWindow(Item.text(1))
        self.UserInfoWindowObject.show()

    # 移除用户
    def RemoveAction(self, Item):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            ID = Item.text(1)
            Result = UserAction().RemoveUser(ID)
            if Result["State"] == True:
                self.UserTree.RemoveTopItem(Item)
                MSGBOX().COMPLETE(self.Lang.Complete)
            else:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return

    # 新建用户窗口
    def CreateUserWindow(self):
        self.CreateUserWindowObject = CreateUserWindow()
        self.CreateUserWindowObject.ActionSignal.connect(self.CreateUserAction)
        self.CreateUserWindowObject.show()

    # 新建用户方法
    def CreateUserAction(self, Name, ID):
        Item = QTreeWidgetItem()  # 设置item控件
        Item.setText(0, Name)  # 设置内容
        Item.setText(1, str(ID))
        Item.setTextAlignment(
            0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        Item.setTextAlignment(
            1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        self.UserTree.insertTopLevelItem(0, Item)

    # 查看demo
    def CheckDemo(self):
        Result = UserAction().CheckImportUsersDemo(self.Lang.Type)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        else:
            FileEntityName = Result["FileEntityName"]
            Data = self.Common.Base64ToBytes(Result["Data"])
            if self.File.WFileInByte(self.Cache.Get("UserTempDir") + FileEntityName, Data):
                self.File.OpenLocalDir(self.Cache.Get("UserTempDir"))
            else:
                self.File.DeleteFile(self.Cache.Get(
                    "UserTempDir") + FileEntityName)
                MSGBOX().ERROR(self.Lang.RequestWasAborted)
                return

    # 导入用户
    def ImportUsers(self):
        Files, _ = QFileDialog.getOpenFileName(self)  # 文件选择框
        if len(Files) == 0:
            return
        Result = UserAction().ImportUser(Files)
        if Result["State"] == True:
            self.UserTree.clear()
            UserData = UserAction().SelectUser(-1)["Data"]
            if len(UserData) > 0:
                UserTreeItems = []
                for i in range(len(UserData)):
                    if UserData[i]["Account"] != self.Cache.Get("Account"):
                        item = QTreeWidgetItem()  # 设置item控件
                        # item.setIcon(0, QtGui.QIcon(os.getcwd() + "/avatar.png"))
                        item.setText(0, UserData[i]["Name"])  # 设置内容
                        item.setText(1, str(UserData[i]["ID"]))  # 设置内容
                        item.setTextAlignment(
                            0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                        item.setTextAlignment(
                            1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                        UserTreeItems.append(item)  # 添加到item list
                    self.UserTree.insertTopLevelItems(
                        0, UserTreeItems)  # 添加到用户列表

            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return

    # 单击用户列表
    def UserItemClicked(self):
        self.SA.clear()
        self.CurrentUserID = self.UserTree.currentItem().text(1)
        if self.CurrentUserID == 0:
            return

        StartPoint = self.Common.StrToTime(self.Common.TodayStr())
        EndPoint = self.Common.TimeFuture(1)

        Result1 = UserAction().MessageList(
            1, self.CurrentUserID, 0, StartPoint, EndPoint)  # 收到的信息
        Result2 = UserAction().MessageList(
            2, self.CurrentUserID, 0, StartPoint, EndPoint)  # 发送的信息

        if Result1["State"] != True or Result2["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        Data1 = Result1["Data"]
        Data2 = Result2["Data"]

        Data = Data1 + Data2

        if len(Data) > 0:
            # 按时间戳排序
            SortData = sorted(Data, key=lambda e: e.__getitem__('Createtime'))
            for i in range(len(SortData)):
                ReceiverID = SortData[i]["ReceiverID"]
                SenderID = SortData[i]["SenderID"]
                Content = SortData[i]["Content"]
                Createtime = SortData[i]["Createtime"]

                Item = QListWidgetItem()
                self.SA.addItem(Item)
                FrameH = 0
                if self.MyID == SenderID:
                    ContentWidget = SentFrame(self.MyName, Content, Createtime)
                    FrameH = ContentWidget.height()
                    self.SA.setItemWidget(Item, ContentWidget)
                if self.MyID == ReceiverID:
                    ContentWidget = ReceivedFrame(
                        self.MyName, Content, Createtime)
                    FrameH = ContentWidget.height()
                    self.SA.setItemWidget(Item, ContentWidget)
                Item.setSizeHint(QtCore.QSize(200, FrameH))

        self.SA.setCurrentRow(self.SA.count() - 1)  # 滑动到底部

    # 发送简讯
    def NewMessage(self):
        if self.CurrentUserID == 0:
            MSGBOX().WARNING(self.Lang.NoUserSelected)
            return

        MSG = self.MessageInput.text()
        if MSG == "":
            return
        if len(MSG) > 950:
            MSGBOX().ERROR(self.Lang.ExceedTheWordLimit + " (950)")
            return

        Result = UserAction().CreateMessage(MSG, self.CurrentUserID)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        else:
            SName = ""
            STime = self.Common.Time()
            Result = UserAction().CheckSelf()
            if Result["State"] == True:
                SName = Result["Data"]["Name"]

            self.MessageInput.setText("")
            Item = QListWidgetItem()
            self.SA.addItem(Item)
            ContentWidget = SentFrame(SName, MSG, STime)
            FrameH = ContentWidget.height()
            Item.setSizeHint(QtCore.QSize(200, FrameH))
            self.SA.setItemWidget(Item, ContentWidget)
            self.SA.setCurrentRow(self.SA.count() - 1)  # 滑动到底部

    # 历史信息窗口
    def HistoryWindow(self):
        self.HistoryWindowObject = HistoryWindow(self.CurrentUserID)

    # 信息提示窗
    def InfoTipWindow(self, TextParam):
        if TextParam == "":
            return
        self.TooltipWorker = TooltipWorker()
        self.TooltipWindow.Label.setText(
            self.Lang.ReceivedNewMessageFrom + " " + TextParam)
        self.TooltipWorker.ActionSignal.connect(
            self.TooltipWindow.show)
        self.TooltipWorker.HideSignal.connect(
            self.TooltipWindow.hide)
        self.TooltipWorker.FinishSignal.connect(
            self.KillThread(self.TooltipThread))
        self.TooltipWorker.moveToThread(self.TooltipThread)
        self.TooltipThread.started.connect(self.TooltipWorker.Run)
        self.TooltipThread.start()

    # 新信息提示方法
    def InfoTipAction(self):
        self.InfoTipWorker = InfoTipWorker()
        self.InfoTipWorker.ActionSignal.connect(self.InfoTipWindow)
        self.InfoTipWorker.FinishSignal.connect(
            self.KillThread(self.InfoTipThread))
        self.InfoTipWorker.moveToThread(self.InfoTipThread)
        self.InfoTipThread.started.connect(self.InfoTipWorker.Run)
        self.InfoTipThread.start()

    # 账号统计提示
    def AccountNumberStatisticsAction(self):
        Result = ConfigAction().AccountNumberStatistics()
        if Result["State"] != True:
            return
        else:
            Data = Result["Data"]
            DataArr = Common().Explode("_", Data)
            MSGBOX().CUE(self.Lang.AccountsUsed + " " +
                         DataArr[0] + ". " + self.Lang.TotalAccounts + " " + DataArr[1] + ".")


class UserLabel(QLabel):  # 用户列表标题栏
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


class ReceivedFrame(BaseInterface, BaseFrame):  # 接收框
    def __init__(self, UserName="", Context="", Date=0):
        super().__init__()
        self.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Conversation_Frame())
        self.ConversationHLayout = QHBoxLayout()
        self.ConversationHLayout.setContentsMargins(0, 0, 0, 0)

        self.ConversationVLayout = QVBoxLayout()
        self.ConversationVLayout.setContentsMargins(0, 0, 0, 0)

        self.IconLabel = QLabel(
            UserName + "  " + self.Common.TimeToStr(Date))
        self.IconLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Conversation_Label())
        self.ConversationVLayout.addWidget(self.IconLabel)

        self.ConversationLabel = QTextEdit(Context)
        self.ConversationLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Message_Conversation_Received())
        self.ConversationLabel.setReadOnly(True)
        self.ConversationLabel.verticalScrollBar().hide()
        self.ConversationLabel.document().adjustSize()
        CurrentH = int(self.ConversationLabel.document().size().height()) + 40
        if CurrentH != self.ConversationLabel.height():
            if CurrentH > 200:
                self.ConversationLabel.verticalScrollBar().show()
            self.setFixedHeight(CurrentH)
        self.ConversationVLayout.addWidget(self.ConversationLabel)

        self.ConversationHLayout.addLayout(self.ConversationVLayout)
        self.ConversationHLayout.addStretch()

        self.setLayout(self.ConversationHLayout)


class SentFrame(BaseInterface, BaseFrame):  # 发出框
    def __init__(self, UserName="", Context="", Date=0):
        super().__init__()
        self.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Conversation_Frame())
        self.ConversationHLayout = QHBoxLayout()
        self.ConversationHLayout.setContentsMargins(0, 0, 0, 0)

        self.ConversationVLayout = QVBoxLayout()
        self.ConversationVLayout.setContentsMargins(0, 0, 0, 0)

        self.IconLabel = QLabel(
            UserName + "  " + self.Common.TimeToStr(Date))
        self.IconLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Conversation_Label())
        self.ConversationVLayout.addWidget(self.IconLabel)

        self.ConversationLabel = QTextEdit(Context)
        self.ConversationLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Message_Conversation_Sent())
        self.ConversationLabel.setReadOnly(True)
        self.ConversationLabel.verticalScrollBar().hide()
        self.ConversationLabel.document().adjustSize()
        self.ConversationLabel.document().adjustSize()
        CurrentH = int(self.ConversationLabel.document().size().height()) + 40
        if CurrentH != self.ConversationLabel.height():
            if CurrentH > 200:
                self.ConversationLabel.verticalScrollBar().show()
            self.setFixedHeight(CurrentH)
        self.ConversationVLayout.addWidget(self.ConversationLabel)

        self.ConversationHLayout.addStretch()
        self.ConversationHLayout.addLayout(self.ConversationVLayout)

        self.setLayout(self.ConversationHLayout)


class UserInfoWindow(BaseInterface, BaseDialog):  # 用户详情
    def __init__(self, ID):
        super().__init__()
        self.AppMode()
        self.UserID = ID
        self.VLayout = QFormLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        Result = UserAction().UserInfo(self.UserID)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        self.UserInfo = Result["Data"]

        MasterCheck = UserAction().IsMaster()["State"]

        AvatarLayout = QHBoxLayout()
        AvatarLayout.setContentsMargins(0, 0, 0, 0)
        AvatarLayout.setAlignment(Qt.AlignCenter)  # 居中
        self.AvatarLabel = QLabel("")  # 默认展示内容
        self.AvatarLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.AvatarLabel.setFixedSize(125, 120)  # 固定大小
        self.AvatarLabel.setStyleSheet(
            self.Style.Object.MainFrame_CheckMyself_Label())  # 设置样式
        self.AvatarLabel.setScaledContents(True)  # 图片自适应
        self.AvatarLabel.setToolTip(self.Lang.Avatar)  # 设置鼠标提示
        AvatarLayout.addWidget(self.AvatarLabel)
        self.VLayout.addRow(self.Lang.Avatar + " :", AvatarLayout)

        # 加载图像到Label
        if self.UserInfo["Avatar"] != "":
            AvatarByte = QByteArray.fromBase64(
                self.UserInfo["Avatar"].encode("utf8"))  # 读取二进制信息
            QPObject = QPixmap()  # 实例化图像处理类
            QPObject.loadFromData(AvatarByte)  # 加载到类
            # IMG = QPObject.scaled(100, 100, Qt.KeepAspectRatio)  # 按比例缩放
            IMG = QPObject.scaled(100, 100, Qt.IgnoreAspectRatio)  # 不按比例缩放
            self.AvatarLabel.setPixmap(self.SetIMG(IMG))

        self.UserAccountInput = QLineEdit()
        self.UserAccountInput.setEnabled(False)
        self.UserAccountInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.UserAccountInput.setFixedHeight(30)
        self.UserAccountInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Info_Win_Input())
        self.UserAccountInput.setToolTip(self.Lang.Account)
        self.UserAccountInput.setText(self.UserInfo["Account"])
        self.VLayout.addRow(self.Lang.Account + " :", self.UserAccountInput)

        self.UserNameInput = QLineEdit()
        self.UserNameInput.setEnabled(False)
        self.UserNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.UserNameInput.setFixedHeight(30)
        self.UserNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Info_Win_Input())
        self.UserNameInput.setToolTip(self.Lang.Name)
        self.UserNameInput.setText(self.UserInfo["Name"])
        self.VLayout.addRow(self.Lang.Name + " :", self.UserNameInput)

        if MasterCheck == True:
            self.UserPWDInput = QLineEdit()
            self.UserPWDInput.setEnabled(True)
            self.UserPWDInput.setAlignment(
                Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
            self.UserPWDInput.setFixedHeight(30)
            self.UserPWDInput.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_Info_Win_Input())
            self.UserPWDInput.setToolTip(self.Lang.PWD)
            self.UserPWDInput.setEchoMode(QLineEdit.Password)  # 输入为密码类型
            self.VLayout.addRow(self.Lang.PWD + " :", self.UserPWDInput)

            self.AdminSelect = QComboBox()
            self.AdminSelect.setView(QListView())
            self.AdminSelect.setFixedHeight(30)
            self.AdminSelect.setFixedWidth(60)
            self.AdminSelect.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_Info_Win_Box())
            Options = [
                " " + self.Lang.Select,
                " " + self.Lang.No,
                " " + self.Lang.Yes
            ]
            self.AdminSelect.addItems(Options)
            self.AdminSelect.setCurrentIndex(self.UserInfo["Admin"])
            self.VLayout.addRow(self.Lang.DepartmentManager +
                                " :", self.AdminSelect)

            self.MasterSelect = QComboBox()
            self.MasterSelect.setView(QListView())
            self.MasterSelect.setFixedHeight(30)
            self.MasterSelect.setFixedWidth(60)
            self.MasterSelect.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_Info_Win_Box())
            Options = [
                " " + self.Lang.Select,
                " " + self.Lang.No,
                " " + self.Lang.Yes
            ]
            self.MasterSelect.addItems(Options)
            self.MasterSelect.setCurrentIndex(self.UserInfo["Master"])
            self.VLayout.addRow(self.Lang.SuperAdmin +
                                " :", self.MasterSelect)

            self.Btn = QPushButton("OK")
            self.Btn.setFixedHeight(30)
            self.Btn.setStyleSheet(
                self.Style.Object.MainFrame_Mid_User_Info_Win_Btn())
            self.Btn.clicked.connect(self.ModifyAction)
            self.VLayout.addRow(self.Btn)

            self.setFixedSize(400, 345)
        else:
            self.setFixedSize(300, 200)

        self.setLayout(self.VLayout)

    def ModifyAction(self):
        Name = self.UserInfo["Name"],
        Password = ""
        if self.UserPWDInput.text() != "":
            Password = self.UserPWDInput.text()
        if Password != "" and len(Password) < 6:
            MSGBOX().ERROR(self.Lang.IncorrectPassword)
            return
        Avatar = self.UserInfo["Avatar"]
        Wallpaper = self.UserInfo["Wallpaper"]
        Admin = self.AdminSelect.currentIndex()
        Master = self.MasterSelect.currentIndex()
        Status = self.UserInfo["Status"]
        Permission = self.UserInfo["Permission"]
        DepartmentID = self.UserInfo["DepartmentID"]
        Result = UserAction().UserModify(
            Name,
            Password,
            Avatar,
            Wallpaper,
            Admin,
            Status,
            Permission,
            Master,
            DepartmentID,
            self.UserID
        )
        if Result["State"] == True:
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return


class CreateUserWindow(BaseInterface, BaseDialog):  # 新建用户
    ActionSignal = Signal(str, int)  # 设置信号

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setFixedSize(320, 150)
        self.FLayout = QFormLayout()
        self.FLayout.setContentsMargins(5, 5, 5, 5)

        self.UserAccountInput = QLineEdit()
        self.UserAccountInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.UserAccountInput.setFixedHeight(30)
        self.UserAccountInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Info_Win_Input())

        self.UserNameInput = QLineEdit()
        self.UserNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.UserNameInput.setFixedHeight(30)
        self.UserNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Info_Win_Input())

        self.UserPWDInput = QLineEdit()
        self.UserPWDInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.UserPWDInput.setFixedHeight(30)
        self.UserPWDInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Info_Win_Input())
        self.UserPWDInput.setEchoMode(QLineEdit.Password)  # 输入为密码类型

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Info_Win_Btn())
        self.Btn.clicked.connect(self.CreateAction)

        self.FLayout.addRow(self.Lang.Account + " :", self.UserAccountInput)
        self.FLayout.addRow(self.Lang.Name + " :", self.UserNameInput)
        self.FLayout.addRow(self.Lang.PWD + " :", self.UserPWDInput)
        self.FLayout.addRow(self.Btn)
        self.setLayout(self.FLayout)

    def CreateAction(self):
        Account = self.UserAccountInput.text()
        Name = self.UserNameInput.text()
        PWD = self.UserPWDInput.text()

        if self.Common.MatchAll(Account) == False:
            MSGBOX().ERROR(self.Lang.IncorrectAccount)
            return
        elif len(Account) < 4:
            MSGBOX().ERROR(self.Lang.IncorrectAccount)
            return
        elif self.Common.MatchSafe(Name) == False:
            MSGBOX().ERROR(self.Lang.WrongUserName)
            return
        elif len(Name) < 2:
            MSGBOX().ERROR(self.Lang.WrongNameLength)
            return
        elif PWD == "":
            MSGBOX().ERROR(self.Lang.IncorrectPassword)
            return
        elif len(PWD) < 6:
            MSGBOX().ERROR(self.Lang.IncorrectPassword)
            return
        else:
            Result = UserAction().CreateUser(Account, Name, PWD)
            if Result["State"] == True:
                self.ActionSignal.emit(Name, Result["ID"])
                self.close()
                MSGBOX().COMPLETE(self.Lang.Complete)
            else:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return


class HistoryWindow(BaseInterface, BaseDialog):  # 历史信息
    def __init__(self, UserID):
        super().__init__()
        self.UserID = UserID
        if self.UserID == 0:
            self.destroy()
            MSGBOX().WARNING(self.Lang.NoUserSelected)
            return
        Result = UserAction().UserInfo(self.UserID)
        if Result["State"] != True:
            self.destroy()
            MSGBOX().WARNING(self.Lang.RequestWasAborted)
            return
        self.UserInfo = Result["Data"]

        self.AppMode()
        self.setFixedSize(450, 300)
        self.Layout = QVBoxLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.CalendarLayout = QHBoxLayout()
        # self.CalendarLayout.setContentsMargins(0, 0, 0, 0)
        self.BtnLayout = QHBoxLayout()
        # self.BtnLayout.setContentsMargins(0, 0, 0, 0)

        self.CalendarWidget = QCalendarWidget()
        self.CalendarLayout.addWidget(self.CalendarWidget)

        self.Btn = QPushButton(self.Lang.Confirm)
        self.Btn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Message_List_Btn())
        self.Btn.setFixedHeight(30)
        self.Btn.clicked.connect(self.ShowMessageList)
        self.BtnLayout.addWidget(self.Btn)

        self.Layout.addLayout(self.CalendarLayout)
        self.Layout.addLayout(self.BtnLayout)
        self.setLayout(self.Layout)
        self.show()

    def ShowMessageList(self):
        DateStr = self.CalendarWidget.selectedDate().toString("yyyy-MM-dd 00:00:00")
        StartDate = self.Common.StrToTime(DateStr)
        EndDate = self.Common.TheTimeFuture(StartDate, 1)
        Result1 = UserAction().MessageList(1, self.UserID, 0, StartDate, EndDate)
        Result2 = UserAction().MessageList(2, self.UserID, 0, StartDate, EndDate)
        if Result1["State"] != True or Result2["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        Data1 = Result1["Data"]
        Data2 = Result2["Data"]
        Data = Data1 + Data2
        if len(Data) > 0:
            self.MessageWindow = HistoryMessageListWindow(
                Data, self.UserInfo["Name"])
        else:
            MSGBOX().WARNING(self.Lang.NoData)
            return


class HistoryMessageListWindow(BaseInterface, BaseDialog):  # 历史信息展示
    def __init__(self, List=[], UserName=""):
        super().__init__()
        if len(List) == 0:
            return
        if UserName == "":
            return
        Result = UserAction().CheckSelf()
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        MyInfo = Result["Data"]
        MyID = MyInfo["ID"]
        MyName = MyInfo["Name"]

        self.AppMode()
        self.Top()
        self.setMinimumSize(450, 300)

        self.Layout = QVBoxLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.SA = QScrollArea()
        self.SA.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条
        self.SA.setWidgetResizable(True)  # 自适应宽度
        self.SA.setStyleSheet(
            self.Style.Object.BaseScrollArea())

        self.MessageFrame = QFrame()
        self.MessageFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_User_Message_Frame())

        self.MessageLayout = QVBoxLayout()
        self.MessageLayout.setContentsMargins(10, 10, 10, 10)

        SortData = sorted(
            List, key=lambda e: e.__getitem__('Createtime'))  # 按时间戳排序
        for i in range(len(SortData)):
            ReceiverID = SortData[i]["ReceiverID"]
            SenderID = SortData[i]["SenderID"]
            Content = SortData[i]["Content"]
            Createtime = SortData[i]["Createtime"]
            if MyID == SenderID:
                self.MessageLayout.addWidget(
                    SentFrame(MyName, Content, Createtime))
            if MyID == ReceiverID:
                self.MessageLayout.addWidget(
                    ReceivedFrame(UserName, Content, Createtime))
        self.MessageLayout.addStretch()

        self.MessageFrame.setLayout(self.MessageLayout)
        self.SA.setWidget(self.MessageFrame)

        self.Layout.addWidget(self.SA)
        self.setLayout(self.Layout)
        self.setStyleSheet(self.Style.Object.BaseDialog())
        self.show()


class TooltipWorker(BaseInterface, BaseObject):  # 提示窗
    ActionSignal = Signal()
    HideSignal = Signal()

    def __init__(self):
        super().__init__()

    def Run(self):
        self.ActionSignal.emit()
        sleep(3)
        self.HideSignal.emit()


class InfoTipWorker(BaseInterface, BaseObject):  # 当天的新信息提示
    ActionSignal = Signal(str)

    def __init__(self):
        super().__init__()

    def Run(self):
        StartPoint = self.Common.StrToTime(self.Common.TodayStr())
        EndPoint = self.Common.TimeFuture(1)
        while True:
            sleep(1)
            Result = UserAction().MessageList(
                1, 0, 1, StartPoint, EndPoint)["Data"]  # 收到的信息

            if len(Result) > self.Cache.Get("MessageCount"):
                SenderID = Result[-1]["SenderID"]
                SenderInfo = UserAction().UserInfo(SenderID)["Data"]
                SenderName = SenderInfo["Name"]
                self.Cache.Set("MessageCount", len(Result))
                self.ActionSignal.emit(SenderName)

            for i in range(len(Result)):
                UserAction().SetMessage(Result[i]["ID"])
