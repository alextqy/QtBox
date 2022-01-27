# -*- coding:utf-8 -*-
from interface._base import *


class FileTagFrame(BaseInterface, BaseFrame):
    def __init__(self):
        super().__init__()

        # =========================================== Ready ===========================================

        SelectTagData = DirFileAction().TagList()
        if SelectTagData["State"] != True:
            return

        self.TagData = SelectTagData["Data"]
        self.CurrentTagID = 0

        # =========================================== 标签 ===========================================
        self.TagVS = self.VS()

        # 标签标题栏
        self.TagHeader = TagHeaderLabel(self.Lang.TagList)
        self.TagHeader.setFixedHeight(20)
        self.TagHeader.setAlignment(Qt.AlignCenter)  # 字体居中
        self.TagHeader.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Header()
        )  # 设置样式

        # 标签列表
        self.TagTree = BaseTreeWidget()
        self.TagTree.setMaximumWidth(300)
        self.TagTree.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Tree_Widget()
        )  # 设置样式
        self.TagTree.HideVScroll()  # 隐藏纵向滚动条
        self.TagTree.setColumnCount(2)  # 设置列数
        self.TagTree.hideColumn(1)  # 隐藏列
        self.TagTree.setHeaderLabels(["Tag", "ID"])  # 设置标题栏
        self.TagTree.setHeaderHidden(True)  # 隐藏标题栏
        self.TagTree.setAcceptDrops(True)  # 开启接收拖动
        # self.TagTree.MoveSignal.connect(self.CheckMoveTreeItems)

        self.InsertTagListData(self.TagData)

        # 鼠标左键点击事件
        # self.TagTree.clicked.connect(self.TagItemClicked)

        # 鼠标右键 链接槽函数
        self.TagTree.Connect(self.TagRightContextMenuExec)

        self.TagListBtnFrame = QFrame()
        self.TagListBtnFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_List_Btn_Frame()
        )
        self.TagListBtnFrame.setFixedHeight(30)
        self.TagListBtnFrame.setContentsMargins(0, 0, 0, 0)

        self.TagListBtnLayout = QHBoxLayout()
        self.TagListBtnLayout.setContentsMargins(0, 0, 0, 0)

        self.NewTagBtn = QPushButton(self.Lang.NewTag)
        self.NewTagBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_List_Btn())
        self.NewTagBtn.setContentsMargins(1, 1, 1, 1)
        self.NewTagBtn.setFixedHeight(30)
        self.NewTagBtn.clicked.connect(self.CreateTagWindow)
        self.TagListBtnLayout.addWidget(self.NewTagBtn)

        self.TagListBtnFrame.setLayout(self.TagListBtnLayout)

        self.TagVS.addWidget(self.TagHeader)
        self.TagVS.addWidget(self.TagTree)
        self.TagVS.addWidget(self.TagListBtnFrame)

        # =========================================== 文件 ===========================================
        self.FileVS = self.VS()

        # 文件标题栏
        self.FileHeaderFrame = QFrame()
        self.FileHeaderFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Header_Frame())
        self.FileHeaderFrame.setFixedHeight(20)

        self.FileHeaderLayout = QHBoxLayout()
        self.FileHeaderLayout.setContentsMargins(0, 0, 0, 0)  # 设置边距

        self.FileHeader = QLabel(self.Lang.FileList)
        self.FileHeader.setStyleSheet(
            self.Style.Object.MainFrame_Mid_File_Tag_Top_Label()
        )  # 设置样式
        self.FileHeader.setAlignment(Qt.AlignCenter)  # 字体居中

        self.FileHeaderLayout.addWidget(self.FileHeader)
        self.FileHeaderFrame.setLayout(self.FileHeaderLayout)
        self.FileVS.addWidget(self.FileHeaderFrame)

        self.FileFrame = QFrame()
        self.FileFrame.setStyleSheet(
            self.Style.Object.MainFrame_Mid_File_Tag_Frame())
        self.FileLayout = QVBoxLayout()
        self.FileLayout.setContentsMargins(0, 0, 0, 0)

        self.FileTree = BaseTreeWidget()  # 员工列表控件
        self.FileTree.SetSelectionMode(2)  # 设置多选模式
        self.FileTree.setStyleSheet(
            self.Style.Object.MainFrame_Mid_File_Tag_Tree_Widget()
        )  # 设置样式
        self.FileTree.HideVScroll()  # 隐藏纵向滚动条
        self.FileTree.HideHScroll()  # 隐藏横向滚动条
        self.FileTree.setColumnCount(3)  # 设置列数
        self.FileTree.hideColumn(1)  # 隐藏列
        self.FileTree.setHeaderLabels(["TagName", "ID", "CreateTime"])  # 设置标题栏
        self.FileTree.setHeaderHidden(True)  # 隐藏标题栏
        self.FileTree.setColumnWidth(0, 200)  # 设置列宽
        self.FileTree.setDragEnabled(True)  # 设置item可拖动

        self.FileLayout.addWidget(self.FileTree)
        self.FileFrame.setLayout(self.FileLayout)
        self.FileVS.addWidget(self.FileFrame)

        # ============================================================================================
        # 分割线
        self.MidRS = self.HS()
        self.MidRS.addWidget(self.TagVS)
        self.MidRS.addWidget(self.FileVS)

        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.MidRS)
        self.setLayout(MainLayout)

    # 写入标签列表
    def InsertTagListData(self, TagList):
        TagTreeItems = []
        if len(TagList) > 0:
            for i in range(len(TagList)):
                item = QTreeWidgetItem()  # 设置item控件
                item.setText(0, TagList[i]["TagName"])  # 设置内容
                item.setText(1, str(TagList[i]["ID"]))  # 设置内容
                item.setTextAlignment(
                    0, Qt.AlignHCenter | Qt.AlignVCenter
                )  # 设置item字体居中
                item.setTextAlignment(
                    1, Qt.AlignHCenter | Qt.AlignVCenter
                )  # 设置item字体居中
                TagTreeItems.append(item)  # 添加到item list
            self.TagTree.insertTopLevelItems(
                0, TagTreeItems)  # 添加到标签列表

    # 标签右键菜单
    def TagRightContextMenuExec(self, pos):
        self.TagTreeMenu = BaseMenu()  # 左侧标签列表鼠标右键菜单
        self.TagTreeMenu.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Staff_Tree_Menu()
        )  # 设置样式
        Item = self.TagTree.currentItem()  # 获取被点击行控件
        ItemAt = self.TagTree.itemAt(pos)  # 获取点击焦点

        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            self.TagTreeMenu.AddAction(
                self.Lang.Rename, lambda: self.TagRenameWindow(Item)
            )  # 重命名
            self.TagTreeMenu.AddAction(
                self.Lang.Delete, lambda: self.DelTag(Item)
            )  # 删除标签
        else:  # 焦点外
            return

        self.TagTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.TagTreeMenu.show()  # 展示

    # 新建标签方法
    def CreateTapAction(self, Name, ID):
        Item = QTreeWidgetItem()  # 设置item控件
        Item.setText(0, Name)  # 设置内容
        Item.setText(1, str(ID))
        Item.setTextAlignment(0, Qt.AlignHCenter |
                              Qt.AlignVCenter)  # 设置item字体居中
        Item.setTextAlignment(1, Qt.AlignHCenter |
                              Qt.AlignVCenter)  # 设置item字体居中
        self.TagTree.insertTopLevelItem(0, Item)

    # 刷新标签列表
    def RefurbishTapList(self):
        self.TagTree.clear()
        self.InsertTagListData(DirFileAction().TagList()["Data"])

    # 添加标签
    def CreateTagWindow(self):
        self.TagWindow = CreateTagWindow()
        self.TagWindow.ActionSignal.connect(self.CreateTapAction)
        self.TagWindow.ActionSignal.connect(self.RefurbishTapList)
        self.TagWindow.show()

    # 重命名标签
    def TagRenameWindow(self, Item):
        self.TagRenameWindowObject = TagRenameWindow(Item)
        self.TagRenameWindowObject.show()

    # 删除标签
    def DelTag(self, Item):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            ID = Item.text(1)
            Result = DirFileAction().DelTag(ID)
            if Result["State"] == True:
                self.TagTree.RemoveItems(Item)
                MSGBOX().COMPLETE(self.Lang.Complete)
                return
            else:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return


class TagHeaderLabel(QLabel):  # 标签列表标题栏
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


class CreateTagWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal(str, int)  # 设置信号

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.TagNameInput = QLineEdit()
        self.TagNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        )  # 内容居中
        self.TagNameInput.setFixedHeight(30)
        self.TagNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Win_Input()
        )

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_Tag_Win_Btn())
        self.Btn.clicked.connect(self.CreateAction)

        self.VLayout.addWidget(self.TagNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def CreateAction(self):
        if self.TagNameInput.text() == "":
            MSGBOX().ERROR(self.Lang.WrongTagName)
            return
        if len(self.TagNameInput.text()) < 2:
            MSGBOX().ERROR(self.Lang.WrongLengthOfTagName)
            return

        Result = DirFileAction().CreateTag(self.TagNameInput.text(), 0)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        elif Result["ID"] == 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        else:
            self.ActionSignal.emit(self.TagNameInput.text(), Result["ID"])
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)


class TagRenameWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()

    def __init__(self, Item):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.Item = Item
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.TagNameInput = QLineEdit()
        self.TagNameInput.setAlignment(
            Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        )  # 内容居中
        self.TagNameInput.setFixedHeight(30)
        self.TagNameInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Win_Input()
        )
        self.TagNameInput.setText(self.Item.text(0))

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_Tag_Win_Btn())
        self.Btn.clicked.connect(self.RenameAction)

        self.VLayout.addWidget(self.TagNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def RenameAction(self):
        if self.TagNameInput.text() == self.Item.text(0):
            return
        elif self.TagNameInput.text() == "":
            MSGBOX().ERROR(self.Lang.WrongTagName)
            return
        else:
            TagInfo = DirFileAction().TagInfo(self.Item.text(1))
            if TagInfo["State"] != True:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return
            else:
                Result = DirFileAction().ModifyTag(
                    self.Item.text(1),
                    self.TagNameInput.text(),
                    TagInfo["Data"]["ID"],
                )
                if Result["State"] == True:
                    self.Item.setText(0, self.TagNameInput.text())
                    self.close()
                    MSGBOX().COMPLETE(self.Lang.Complete)
                else:
                    MSGBOX().ERROR(self.Lang.OperationFailed)
                    return
