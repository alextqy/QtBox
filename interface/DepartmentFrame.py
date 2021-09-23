# -*- coding:utf-8 -*-
from interface._base import *


class DepartmentFrame(BaseInterface, BaseFrame):
    def __init__(self):
        super().__init__()

        # =========================================== Ready ===========================================

        SelectDepartmentData = DepartmentAction().SelectDepartment()
        if SelectDepartmentData["State"] != True:
            return

        self.DepartmentData = SelectDepartmentData["Data"]
        self.CurrentDepartmentID = 0

        # =========================================== 部门 ===========================================
        self.DepartmentVS = self.VS()

        # 部门标题栏
        self.DepartmentHeader = DepartmentHeaderLabel(self.Lang.DepartmentList)
        self.DepartmentHeader.setFixedHeight(20)
        self.DepartmentHeader.setAlignment(Qt.AlignCenter)  # 字体居中
        self.DepartmentHeader.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Header())  # 设置样式
        self.DepartmentHeader.ActionSignal.connect(self.DepartmentItemClicked)

        # 部门列表
        self.DepartmentTree = BaseTreeWidget()
        self.DepartmentTree.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Tree_Widget())  # 设置样式
        self.DepartmentTree.HideVScroll()  # 隐藏纵向滚动条
        self.DepartmentTree.setColumnCount(2)  # 设置列数
        self.DepartmentTree.hideColumn(1)  # 隐藏列
        self.DepartmentTree.setHeaderLabels(["Department", "ID"])  # 设置标题栏
        self.DepartmentTree.setHeaderHidden(True)  # 隐藏标题栏
        self.DepartmentTree.setAcceptDrops(True)  # 开启接收拖动
        self.DepartmentTree.MoveSignal.connect(self.CheckMoveTreeItems)

        self.InsertDepartmentListData(self.DepartmentData)

        # 鼠标左键点击事件
        self.DepartmentTree.clicked.connect(self.DepartmentItemClicked)

        # 鼠标右键 链接槽函数
        self.DepartmentTree.Connect(self.DepartmentRightContextMenuExec)

        # 部门列表下方按钮
        self.DepartmentListBtnFrame = QFrame()
        self.DepartmentListBtnFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_List_Btn_Frame())
        self.DepartmentListBtnFrame.setFixedHeight(30)
        self.DepartmentListBtnFrame.setContentsMargins(0, 0, 0, 0)

        self.DepartmentListBtnLayout = QHBoxLayout()
        self.DepartmentListBtnLayout.setContentsMargins(0, 0, 0, 0)

        self.NewDepartmentBtn = QPushButton(self.Lang.NewDepartment)
        self.NewDepartmentBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_List_Btn())
        self.NewDepartmentBtn.setContentsMargins(1, 1, 1, 1)
        self.NewDepartmentBtn.setFixedHeight(30)
        self.NewDepartmentBtn.clicked.connect(self.CreateTopDepartmentWindow)
        self.DepartmentListBtnLayout.addWidget(self.NewDepartmentBtn)
        self.DepartmentListBtnFrame.setLayout(self.DepartmentListBtnLayout)

        self.DepartmentVS.addWidget(self.DepartmentHeader)
        self.DepartmentVS.addWidget(self.DepartmentTree)
        self.DepartmentVS.addWidget(self.DepartmentListBtnFrame)

        # =========================================== 成员 ===========================================
        self.StaffVS = self.VS()
        self.StaffRightMouseButton = True

        # 成员标题栏
        self.StaffHeaderFrame = QFrame()
        self.StaffHeaderFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Staff_Header_Frame())
        self.StaffHeaderFrame.setFixedHeight(20)

        self.StaffHeaderLayout = QHBoxLayout()
        self.StaffHeaderLayout.setContentsMargins(0, 0, 0, 0)  # 设置边距

        self.StaffHeader = QLabel(self.Lang.StaffList)
        self.StaffHeader.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Staff_Top_Label())  # 设置样式
        self.StaffHeader.setAlignment(Qt.AlignCenter)  # 字体居中

        self.StaffHeaderLayout.addWidget(self.StaffHeader)
        self.StaffHeaderFrame.setLayout(self.StaffHeaderLayout)
        self.StaffVS.addWidget(self.StaffHeaderFrame)

        self.StaffFrame = QFrame()
        self.StaffFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Staff_Frame())
        self.StaffLayout = QVBoxLayout()
        self.StaffLayout.setContentsMargins(0, 0, 0, 0)

        self.StaffTree = BaseTreeWidget()  # 员工列表控件
        self.StaffTree.SetSelectionMode(2)  # 设置多选模式
        self.StaffTree.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Staff_Tree_Widget())  # 设置样式
        self.StaffTree.HideVScroll()  # 隐藏纵向滚动条
        self.StaffTree.HideHScroll()  # 隐藏横向滚动条
        self.StaffTree.setColumnCount(3)  # 设置列数
        self.StaffTree.hideColumn(1)  # 隐藏列
        self.StaffTree.setHeaderLabels(["Staff", "ID", "CreateTime"])  # 设置标题栏
        self.StaffTree.setHeaderHidden(True)  # 隐藏标题栏
        self.StaffTree.setColumnWidth(0, 200)  # 设置列宽
        self.StaffTree.setDragEnabled(True)  # 设置item可拖动

        # 鼠标左键点击事件
        # self.StaffTree.clicked.connect(self.DepartmentItemClicked)

        # 鼠标右键 链接槽函数
        self.StaffTree.Connect(self.StaffRightContextMenuExec)

        self.StaffLayout.addWidget(self.StaffTree)

        self.StaffFrame.setLayout(self.StaffLayout)
        self.StaffVS.addWidget(self.StaffFrame)

        # 成员列表下方按钮
        self.StaffListBtnFrame = QFrame()
        self.StaffListBtnFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Staff_List_Btn_Frame())
        self.StaffListBtnFrame.setFixedHeight(30)
        self.StaffListBtnFrame.setContentsMargins(0, 0, 0, 0)

        self.StaffListBtnLayout = QHBoxLayout()
        self.StaffListBtnLayout.setContentsMargins(0, 0, 0, 0)

        self.UnassignedBtn = QPushButton(self.Lang.AddEmployeesToTheDepartment)
        self.UnassignedBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Staff_List_Btn())
        self.UnassignedBtn.setContentsMargins(1, 1, 1, 1)
        self.UnassignedBtn.setFixedHeight(30)
        self.UnassignedBtn.clicked.connect(self.UnassignedList)

        self.StaffListBtnLayout.addWidget(self.UnassignedBtn)
        self.StaffListBtnFrame.setLayout(self.StaffListBtnLayout)
        self.StaffVS.addWidget(self.StaffListBtnFrame)

        # ============================================================================================
        # 分割线
        self.MidRS = self.HS()
        self.MidRS.addWidget(self.DepartmentVS)
        self.MidRS.addWidget(self.StaffVS)

        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.MidRS)
        self.setLayout(MainLayout)

    # 获取被拖拽的items
    def CheckMoveTreeItems(self, DepartmentID=0):
        if DepartmentID == 0:
            return
        Items = self.StaffTree.selectedItems()
        for i in range(len(Items)):
            UserID = Items[i].text(1)
            Name = Items[i].text(0)
            Result = UserAction().UserInfo(UserID)
            if Result["State"] != True:
                MSGBOX().ERROR(Name + " " + self.Lang.AbnormalData)
                return
            else:
                UserInfo = Result["Data"]
                ModifyResult = UserAction().UserModify(
                    UserInfo["Name"],
                    UserInfo["Password"],
                    UserInfo["Avatar"],
                    UserInfo["Wallpaper"],
                    UserInfo["Admin"],
                    UserInfo["Status"],
                    UserInfo["Permission"],
                    UserInfo["Master"],
                    DepartmentID,
                    UserID
                )
                if ModifyResult["State"] != True:
                    MSGBOX().ERROR(Name + " " + self.Lang.AbnormalData)
                    return
                else:
                    self.StaffTree.RemoveItems(Items[i])

        # 刷新部门列表 解决移动项目后框架列表减少的bug
        self.RefurbishDepartmentList()

    # 刷新部门列表
    def RefurbishDepartmentList(self):
        self.DepartmentTree.clear()
        self.InsertDepartmentListData(
            DepartmentAction().SelectDepartment()["Data"])

    # 添加顶级部门
    def CreateTopDepartmentWindow(self):
        self.CreateTopDepartmentWindowObject = CreateTopDepartmentWindow()
        self.CreateTopDepartmentWindowObject.ActionSignal.connect(
            self.CreateTopDepartmentAction)
        self.CreateTopDepartmentWindowObject.ActionSignal.connect(
            self.RefurbishDepartmentList)
        self.CreateTopDepartmentWindowObject.show()

    # 新建顶级部门方法
    def CreateTopDepartmentAction(self, Name, ID):
        Item = QTreeWidgetItem()  # 设置item控件
        Item.setText(0, Name)  # 设置内容
        Item.setText(1, str(ID))
        Item.setTextAlignment(
            0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        Item.setTextAlignment(
            1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        self.DepartmentTree.insertTopLevelItem(0, Item)

    # 单击部门
    def DepartmentItemClicked(self):
        self.UnassignedBtn.show()
        CurrentItem = self.DepartmentTree.currentItem()  # 获取当前item对象

        if CurrentItem is not None:
            # 获取部门ID
            ID = int(CurrentItem.text(1))
            self.CurrentDepartmentID = ID

            # 清除子节点 防止重复
            i = 0
            while i < CurrentItem.childCount():
                CurrentItem.removeChild(CurrentItem.child(i))

            # 获取子部门
            Result = DepartmentAction().SelectDepartment(ID)
            if Result["State"] != True:
                MSGBOX().ERROR(self.Lang.RequestWasAborted)
                return

            # 设置顶级部门数据
            SubList = Result["Data"]

            SubItemList = []  # 设置子部门数组
            if len(SubList) > 0:
                for i in range(len(SubList)):
                    Item = QTreeWidgetItem()  # 设置item控件
                    Item.setText(0, SubList[i]["DepartmentName"])  # 设置内容
                    Item.setText(1, str(SubList[i]["ID"]))  # 设置内容
                    Item.setTextAlignment(
                        0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                    Item.setTextAlignment(
                        1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                    SubItemList.append(Item)  # 添加到item list
                    CurrentItem.addChildren(SubItemList)  # 添加到部门列表

            # ============================================================================================

            self.StaffTree.clear()
            Result = UserAction().SelectUser(self.CurrentDepartmentID)
            if Result["State"] != True:
                MSGBOX().ERROR(self.Lang.RequestWasAborted)
                return

            StaffList = Result["Data"]
            self.InsertStaffListData(StaffList)

        self.StaffRightMouseButton = True  # 是否允许鼠标右键
        self.StaffHeader.setText(self.Lang.StaffList)

    # 部门右键菜单
    def DepartmentRightContextMenuExec(self, pos):
        self.DepartmentTreeMenu = BaseMenu()  # 左侧部门列表鼠标右键菜单
        self.DepartmentTreeMenu.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Staff_Tree_Menu())  # 设置样式
        Item = self.DepartmentTree.currentItem()  # 获取被点击行控件
        ItemAt = self.DepartmentTree.itemAt(pos)  # 获取点击焦点

        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            self.DepartmentTreeMenu.AddAction(
                self.Lang.Rename, lambda: self.DepartmentRenameWindow(Item))  # 重命名
            self.DepartmentTreeMenu.AddAction(
                self.Lang.AddSubDepartment, lambda: self.CreateSubDepartmentWindow(Item))  # 创建子部门
            self.DepartmentTreeMenu.AddAction(
                self.Lang.Delete, lambda: self.DelDepartment(Item))  # 删除部门
        else:  # 焦点外
            return

        self.DepartmentTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.DepartmentTreeMenu.show()  # 展示

    # 部门重命名
    def DepartmentRenameWindow(self, Item):
        self.DepartmentRenameWindowObject = DepartmentRenameWindow(Item)
        self.DepartmentRenameWindowObject.show()

    # 添加子部门
    def CreateSubDepartmentWindow(self, Item):
        self.CreateSubDepartmentWindowObject = CreateSubDepartmentWindow(Item)
        self.CreateSubDepartmentWindowObject.ActionSignal.connect(
            self.CreateSubDepartmentAction)
        self.CreateSubDepartmentWindowObject.show()

    # 添加子部门方法
    def CreateSubDepartmentAction(self, Name, ID):
        node = QTreeWidgetItem(self.DepartmentTree.currentItem())  # 设置Item控件
        node.setTextAlignment(0, Qt.AlignHCenter |
                              Qt.AlignVCenter)  # 设置item字体居中
        node.setText(0, Name)  # 写入部门名称
        node.setText(1, str(ID))  # 写入部门ID

    # 删除部门
    def DelDepartment(self, Item):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            ID = Item.text(1)
            Result = DepartmentAction().DeleteDepartment(ID)
            if Result["State"] == True:
                self.DepartmentTree.RemoveItems(Item)
                MSGBOX().COMPLETE(self.Lang.Complete)
                return
            else:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return

    # 未分配员工列表
    def UnassignedList(self):
        self.UnassignedBtn.hide()
        self.StaffRightMouseButton = False
        self.StaffHeader.setText(self.Lang.StaffWithoutOwnership)
        self.StaffTree.clear()

        Result = UserAction().SelectUser(0)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        StaffList = Result["Data"][1:]
        self.InsertStaffListData(StaffList)

    # 写入部门列表
    def InsertDepartmentListData(self, DepartmentList):
        DepartmentTreeItems = []
        if len(DepartmentList) > 0:
            for i in range(len(DepartmentList)):
                item = QTreeWidgetItem()  # 设置item控件
                item.setText(
                    0, DepartmentList[i]["DepartmentName"])  # 设置内容
                item.setText(1, str(DepartmentList[i]["ID"]))  # 设置内容
                item.setTextAlignment(
                    0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(
                    1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                DepartmentTreeItems.append(item)  # 添加到item list
            self.DepartmentTree.insertTopLevelItems(
                0, DepartmentTreeItems)  # 添加到部门列表

    # 写入员工列表
    def InsertStaffListData(self, StaffList):
        if len(StaffList) == 0:
            return

        self.StaffTree.clear()
        StaffTreeItems = []
        if len(StaffList) > 0:
            for i in range(len(StaffList)):
                item = QTreeWidgetItem()  # 设置item控件
                item.setText(0, StaffList[i]["Name"])  # 设置内容
                item.setText(1, str(StaffList[i]["ID"]))  # 设置内容
                item.setText(2, self.Common.TimeToStr(
                    StaffList[i]["Createtime"]))  # 设置内容
                item.setTextAlignment(
                    0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(
                    1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(
                    2, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                StaffTreeItems.append(item)  # 添加到item list
            self.StaffTree.insertTopLevelItems(0, StaffTreeItems)  # 添加到员工列表
            self.StaffLayout.addWidget(self.StaffTree)

    # 员工右键菜单
    def StaffRightContextMenuExec(self, pos):
        if self.StaffRightMouseButton == False:
            return

        self.StaffTreeMenu = BaseMenu()  # 左侧部门列表鼠标右键菜单
        self.StaffTreeMenu.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Staff_Tree_Menu())  # 设置样式
        Item = self.StaffTree.currentItem()  # 获取被点击行控件
        ItemAt = self.StaffTree.itemAt(pos)  # 获取点击焦点

        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            self.StaffTreeMenu.AddAction(
                self.Lang.EmployeeInformation, lambda: self.StaffInfoWindow(Item))  # 重命名
            self.StaffTreeMenu.AddAction(
                self.Lang.RemovedFromTheDepartment, self.RemoveStaff)  # 移除员工
        else:  # 焦点外
            return

        self.StaffTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.StaffTreeMenu.show()  # 展示

    # 员工信息
    def StaffInfoWindow(self, Item):
        ID = Item.text(1)
        if ID == 0:
            return
        Result = UserAction().UserInfo(ID)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        UserInfo = Result["Data"]
        self.StaffInfoWindowObject = StaffInfoWindow(
            UserInfo["Account"], UserInfo["Name"])
        self.StaffInfoWindowObject.show()

    # 移除员工
    def RemoveStaff(self):
        StaffList = self.StaffTree.selectedItems()
        if len(StaffList) > 0:
            YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
            if YesOrNo == QtWidgets.QMessageBox.Yes:
                for i in range(len(StaffList)):
                    ID = StaffList[i].text(1)
                    Name = StaffList[i].text(0)
                    Result = UserAction().UserInfo(ID)
                    if Result["State"] != True:
                        MSGBOX().ERROR(Name + " " + self.Lang.OperationFailed)
                        return
                    UserInfo = Result["Data"]
                    ModifyResult = UserAction().UserModify(
                        UserInfo["Name"],
                        UserInfo["Password"],
                        UserInfo["Avatar"],
                        UserInfo["Wallpaper"],
                        UserInfo["Admin"],
                        UserInfo["Status"],
                        UserInfo["Permission"],
                        UserInfo["Master"],
                        0,
                        ID
                    )
                    if ModifyResult["State"] == True:
                        self.StaffTree.RemoveItems(StaffList[i])
                    else:
                        MSGBOX().ERROR(Name + " " + self.Lang.OperationFailed)
                        return

# 部门列表标题栏


class DepartmentHeaderLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


# 添加顶级部门


class CreateTopDepartmentWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal(str, int)  # 设置信号

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.DepartmentNameInput = QLineEdit()
        self.DepartmentNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.DepartmentNameInput.setFixedHeight(30)
        self.DepartmentNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Input())

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Btn())
        self.Btn.clicked.connect(self.CreateAction)

        self.VLayout.addWidget(self.DepartmentNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def CreateAction(self):
        if self.DepartmentNameInput.text() == "":
            MSGBOX().ERROR(self.Lang.WrongDepartmentName)
            return
        if len(self.DepartmentNameInput.text()) < 2:
            MSGBOX().ERROR(self.Lang.WrongLengthOfDepartmentName)
            return

        Result = DepartmentAction().CreateDepartment(self.DepartmentNameInput.text(), 0)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        elif Result["ID"] == 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        else:
            self.ActionSignal.emit(
                self.DepartmentNameInput.text(), Result["ID"])
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)

# 重命名部门


class DepartmentRenameWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()

    def __init__(self, Item):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.Item = Item
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.DepartmentNameInput = QLineEdit()
        self.DepartmentNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.DepartmentNameInput.setFixedHeight(30)
        self.DepartmentNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Input())
        self.DepartmentNameInput.setText(self.Item.text(0))

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Btn())
        self.Btn.clicked.connect(self.RenameAction)

        self.VLayout.addWidget(self.DepartmentNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def RenameAction(self):
        if self.DepartmentNameInput.text() == self.Item.text(0):
            return
        elif self.DepartmentNameInput.text() == "":
            MSGBOX().ERROR(self.Lang.WrongDepartmentName)
            return
        else:
            DepartmentInfo = DepartmentAction().DepartmentInfo(self.Item.text(1))
            if DepartmentInfo["State"] != True:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return
            else:
                Result = DepartmentAction().ModifyDepartment(
                    self.Item.text(1), self.DepartmentNameInput.text(), DepartmentInfo["Data"]["ParentID"])
                if Result["State"] == True:
                    self.Item.setText(0, self.DepartmentNameInput.text())
                    self.close()
                    MSGBOX().COMPLETE(self.Lang.Complete)
                else:
                    MSGBOX().ERROR(self.Lang.OperationFailed)
                    return

# 添加子部门


class CreateSubDepartmentWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal(str, int)

    def __init__(self, Item):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.Item = Item
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.DepartmentNameInput = QLineEdit()
        self.DepartmentNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.DepartmentNameInput.setFixedHeight(30)
        self.DepartmentNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Input())

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Btn())
        self.Btn.clicked.connect(self.CreateAction)

        self.VLayout.addWidget(self.DepartmentNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def CreateAction(self):
        if self.DepartmentNameInput.text() == "":
            MSGBOX().ERROR(self.Lang.WrongDepartmentName)
            return

        Result = DepartmentAction().CreateDepartment(
            self.DepartmentNameInput.text(), self.Item.text(1))
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        elif Result["ID"] == 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        else:
            self.ActionSignal.emit(
                self.DepartmentNameInput.text(), Result["ID"])
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)

# 员工详情


class StaffInfoWindow(BaseInterface, BaseDialog):
    def __init__(self, Account, Name):
        super().__init__()
        self.AppMode()
        self.setFixedSize(320, 80)
        self.VLayout = QFormLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.StaffAccountInput = QLineEdit()
        self.StaffAccountInput.setEnabled(False)
        self.StaffAccountInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.StaffAccountInput.setFixedHeight(30)
        self.StaffAccountInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Input())
        self.StaffAccountInput.setToolTip(self.Lang.Account)
        self.StaffAccountInput.setText(Account)

        self.StaffNameInput = QLineEdit()
        self.StaffNameInput.setEnabled(False)
        self.StaffNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.StaffNameInput.setFixedHeight(30)
        self.StaffNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Department_Win_Input())
        self.StaffNameInput.setToolTip(self.Lang.Name)
        self.StaffNameInput.setText(Name)

        self.VLayout.addRow(self.Lang.Account + " :", self.StaffAccountInput)
        self.VLayout.addRow(self.Lang.Name + " :", self.StaffNameInput)
        self.setLayout(self.VLayout)
