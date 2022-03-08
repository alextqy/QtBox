# -*- coding:utf-8 -*-
from interface._base import *


class MyDepartmentFrame(BaseInterface, BaseFrame):
    DownloadSignal = Signal(list)

    def __init__(self, DepartmentID):
        super().__init__()

        # =========================================== Ready ===========================================
        self.UserList = []
        self.FileList = []

        self.DepartmentID = DepartmentID
        if self.DepartmentID == 0:
            return

        Result2 = UserAction().SelectDepartmentFile()
        if Result2["State"] == True:
            self.FileList = Result2["Data"]

        self.PromptPopUpsThread = QThread()
        self.PromptPopUpsWindow = PromptPopUpsWindow()  # 提示窗

        # =========================================== 人员 ===========================================
        self.UserVS = self.VS()

        # 人员标题栏
        self.UserHeaderLabel = UserHeaderLabel(self.Lang.StaffList)
        self.UserHeaderLabel.setFixedHeight(20)
        self.UserHeaderLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.UserHeaderLabel.setStyleSheet(self.Style.Object.MainFrame_Mid_My_Department_User_Header())  # 设置样式
        self.UserHeaderLabel.ActionSignal.connect(self.InsertFileListData)

        # 人员列表
        self.UserTree = BaseTreeWidget()
        self.UserTree.setMaximumWidth(300)
        self.UserTree.setStyleSheet(self.Style.Object.MainFrame_Mid_My_Department_User_Tree_Widget())  # 设置样式
        self.UserTree.HideVScroll()  # 隐藏纵向滚动条
        self.UserTree.setColumnCount(2)  # 设置列数
        self.UserTree.hideColumn(1)  # 隐藏列
        self.UserTree.setHeaderLabels(["User", "ID"])  # 设置标题栏
        self.UserTree.setHeaderHidden(True)  # 隐藏标题栏

        # 鼠标左键点击事件
        # self.UserTree.clicked.connect(self.UserItemClicked)

        # 鼠标右键 链接槽函数
        self.UserTree.Connect(self.UserRightContextMenuExec)

        self.InsertUserListData()
        self.UserVS.addWidget(self.UserHeaderLabel)
        self.UserVS.addWidget(self.UserTree)

        # =========================================== 文件 ===========================================
        self.FileVS = self.VS()

        self.FileHeaderLabel = UserHeaderLabel(self.Lang.ShareList)
        self.FileHeaderLabel.setFixedHeight(20)
        self.FileHeaderLabel.setAlignment(Qt.AlignCenter)  # 字体居中
        self.FileHeaderLabel.setStyleSheet(self.Style.Object.MainFrame_Mid_My_Department_File_Header())  # 设置样式

        self.FileTree = BaseTreeWidget()
        self.FileTree.SetSelectionMode(2)  # 设置多选模式
        self.FileTree.setStyleSheet(self.Style.Object.MainFrame_Mid_My_Department_File_Tree_Widget())  # 设置样式
        self.FileTree.HideVScroll()  # 隐藏纵向滚动条
        self.FileTree.HideHScroll()  # 隐藏横向滚动条
        self.FileTree.setColumnCount(4)  # 设置列数
        self.FileTree.hideColumn(1)  # 隐藏列
        self.FileTree.hideColumn(3)  # 隐藏列
        self.FileTree.setHeaderLabels(["FILE", "FileID", "CreateTime", "ID"])  # 设置标题栏
        self.FileTree.setHeaderHidden(True)  # 隐藏标题栏
        self.FileTree.setColumnWidth(0, 450)  # 设置列宽

        # 鼠标右键 链接槽函数
        self.FileTree.Connect(self.FileRightContextMenuExec)

        self.InsertFileListData()
        self.FileVS.addWidget(self.FileHeaderLabel)
        self.FileVS.addWidget(self.FileTree)

        # ============================================================================================
        # 分割线
        self.MidRS = self.HS()
        self.MidRS.addWidget(self.UserVS)
        self.MidRS.addWidget(self.FileVS)

        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.MidRS)
        self.setLayout(MainLayout)

    # 写入人员列表
    def InsertUserListData(self):
        self.UserTree.clear()
        Result = UserAction().SelectUser(self.DepartmentID)
        if Result["State"] == True:
            self.UserList = Result["Data"]
        UserTreeItems = []
        if len(self.UserList) > 0:
            for i in range(len(self.UserList)):
                if self.UserList[i]["Account"] != self.Cache.Get("Account"):
                    item = QTreeWidgetItem()  # 设置item控件
                    item.setText(0, self.UserList[i]["Name"])  # 设置内容
                    item.setText(1, str(self.UserList[i]["ID"]))  # 设置内容
                    item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                    item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                    UserTreeItems.append(item)  # 添加到item list
                self.UserTree.insertTopLevelItems(0, UserTreeItems)  # 添加到部门列表

    # 写入文件列表
    def InsertFileListData(self, UserID=0):
        self.FileTree.clear()
        self.FileList = []
        Result = UserAction().SelectDepartmentFile(0, 0, UserID)
        if Result["State"] == True:
            self.FileList = Result["Data"]
        FileTreeItems = []
        if len(self.FileList) > 0:
            for i in range(len(self.FileList)):
                FileID = self.FileList[i]["FileID"]
                CheckFile = DirFileAction().CheckFile(FileID)
                if CheckFile["State"] != True:
                    continue
                FileInfo = CheckFile["Data"]
                item = QTreeWidgetItem()  # 设置item控件

                item.setText(0, FileInfo["FileName"])  # 设置内容
                item.setText(1, str(FileInfo["ID"]))  # 设置内容
                item.setText(2, str(self.Common.TimeToStr(self.FileList[i]["Createtime"])))  # 设置内容
                item.setText(3, str(self.FileList[i]["ID"]))  # 设置内容

                item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(3, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中

                item.setToolTip(2, self.Lang.ReleaseTime)

                FileTreeItems.append(item)  # 添加到item list
            self.FileTree.insertTopLevelItems(0, FileTreeItems)  # 添加到部门列表

    # 用户列表单击事件
    def UserItemClicked(self):
        CurrentDirItem = self.UserTree.currentItem()  # 获取当前item对象
        UserID = CurrentDirItem.text(1)
        self.InsertFileListData(UserID)

    # 用户列表鼠标右键
    def UserRightContextMenuExec(self, pos):
        self.UserTreeMenu = BaseMenu()  # 左侧用户列表鼠标右键菜单
        self.UserTreeMenu.setStyleSheet(self.Style.Object.MainFrame_Mid_My_Department_User_Tree_Menu())  # 设置样式
        Item = self.UserTree.currentItem()  # 获取被点击行控件
        ItemAt = self.UserTree.itemAt(pos)  # 获取点击焦点
        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            return
        else:  # 焦点外
            self.UserTreeMenu.AddAction(self.Lang.Refresh, lambda: self.InsertUserListData())
        self.UserTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.UserTreeMenu.show()  # 展示

    # 文件列表鼠标右键
    def FileRightContextMenuExec(self, pos):
        self.FileTreeMenu = BaseMenu()  # 左侧用户列表鼠标右键菜单
        self.FileTreeMenu.setStyleSheet(self.Style.Object.MainFrame_Mid_My_Department_User_Tree_Menu())  # 设置样式
        Item = self.FileTree.currentItem()  # 获取被点击行控件
        ItemAt = self.FileTree.itemAt(pos)  # 获取点击焦点
        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            self.FileTreeMenu.AddAction(self.Lang.Download, lambda: self.Download())
            self.FileTreeMenu.AddAction(self.Lang.Remove, lambda: self.RemoveFile())
        else:  # 焦点外
            self.FileTreeMenu.AddAction(self.Lang.Refresh, lambda: self.InsertFileListData())
        self.FileTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.FileTreeMenu.show()  # 展示

    # 下载文件
    def Download(self):
        Files = self.FileTree.selectedItems()

        if (len(Files) > 0):
            DownloadFileList = []
            for i in range(len(Files)):
                FileInfo = {}
                FileInfo["FileName"] = Files[i].text(0)
                FileInfo["ID"] = Files[i].text(1)
                DownloadFileList.append(FileInfo)
            self.DownloadSignal.emit(DownloadFileList)
            self.PromptPopUpsAction(self.Lang.AddedToDownloadTaskList)

    # 移除文件
    def RemoveFile(self):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            Files = self.FileTree.selectedItems()
            if len(Files) > 0:
                for i in range(len(Files)):
                    Name = Files[i].text(0)
                    ID = Files[i].text(3)
                    Result = UserAction().DeleteDepartmentFile(ID)
                    if Result["State"] != True:
                        if Result["Memo"] == "Permission denied":
                            MSGBOX().ERROR(self.Lang.PermissionDenied)
                        else:
                            MSGBOX().ERROR(Name + " " + self.Lang.OperationFailed)
                        return
                    else:
                        self.FileTree.RemoveItems(Files[i])
                MSGBOX().COMPLETE(self.Lang.Complete)

    # 提示窗
    def PromptPopUpsAction(self, TextParam=""):
        if TextParam == "":
            return
        self.PromptPopUpsWorker = PromptPopUpsWorker()
        self.PromptPopUpsWindow.Label.setText(TextParam)
        self.PromptPopUpsWorker.ActionSignal.connect(self.PromptPopUpsWindow.show)
        self.PromptPopUpsWorker.HideSignal.connect(self.PromptPopUpsWindow.hide)
        self.PromptPopUpsWorker.FinishSignal.connect(self.KillThread(self.PromptPopUpsThread))
        self.PromptPopUpsWorker.moveToThread(self.PromptPopUpsThread)
        self.PromptPopUpsThread.started.connect(self.PromptPopUpsWorker.Run)
        self.PromptPopUpsThread.start()


# 成员列表标题栏


class UserHeaderLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 文件列表标题栏


class FileHeaderLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 提示窗线程


class PromptPopUpsWorker(BaseInterface, BaseObject):
    ActionSignal = Signal()
    HideSignal = Signal()

    def __init__(self):
        super().__init__()

    def Run(self):
        self.ActionSignal.emit()
        sleep(3)
        self.HideSignal.emit()
