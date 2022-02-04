# -*- coding:utf-8 -*-
from email.charset import QP
from unittest import result
from interface._base import *


class OfflineTaskListWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()  # 设置信号

    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 400)  # 初始化窗口大小

        Layout = QVBoxLayout()  # 设置布局
        Layout.setContentsMargins(5, 5, 5, 5)  # 设置布局内边距

        self.TaskTree = BaseTreeWidget()  # 设置tree控件
        self.TaskTree.SetSelectionMode(2)  # 设置为多选模式
        self.TaskTree.setStyleSheet(
            self.Style.Object.Download_Tree())  # 设置tree控件样式
        self.TaskTree.setColumnCount(5)  # 设置tree控件列数
        self.TaskTree.hideColumn(3)
        self.TaskTree.hideColumn(4)
        self.TaskTree.setHeaderLabels(
            ["URL", self.Lang.TaskStatus, self.Lang.Remark, "ID", "State"])  # 设置标题栏
        self.TaskTree.setColumnWidth(0, 300)  # 设置列宽度
        self.TaskTree.Connect(self.TaskTreeRightContextMenuExec)  # 右键菜单

        BtnLayout = QHBoxLayout()
        BtnLayout.setContentsMargins(0, 0, 0, 0)  # 设置布局内边距

        self.AddTaskBtn = QPushButton(self.Lang.AddTask)
        self.AddTaskBtn.setFixedHeight(30)
        self.AddTaskBtn.setStyleSheet(
            self.Style.Object.Offline_Task_Btn())
        self.AddTaskBtn.clicked.connect(self.AddTaskWindow)

        self.RefreshBtn = QPushButton(self.Lang.Refresh)
        self.RefreshBtn.setFixedSize(150, 30)
        self.RefreshBtn.setStyleSheet(
            self.Style.Object.Offline_Task_Btn())
        self.RefreshBtn.clicked.connect(self.InsertTreeData)

        self.ClearBtn = QPushButton(self.Lang.RemoveAllCompletedTasks)
        self.ClearBtn.setFixedSize(300, 30)
        self.ClearBtn.setStyleSheet(
            self.Style.Object.Offline_Task_Btn())
        self.ClearBtn.clicked.connect(self.RemoveFinish)

        Layout.addWidget(self.TaskTree)
        BtnLayout.addWidget(self.AddTaskBtn)
        BtnLayout.addWidget(self.RefreshBtn)
        BtnLayout.addWidget(self.ClearBtn)
        Layout.addLayout(BtnLayout)
        self.setLayout(Layout)

        self.InsertTreeData()

    def InsertTreeData(self):
        self.TaskTree.clear()
        Data = DirFileAction().OfflineTaskList()
        TaskInfo = Data["Data"]
        TaskItems = []
        if len(TaskInfo) > 0:
            for i in range(len(TaskInfo)):
                item = QTreeWidgetItem()  # 设置item控件
                item.setText(0, TaskInfo[i]["URL"])  # 设置内容
                # 1未处理 2处理中 3处理完成 4任务失败
                if TaskInfo[i]["State"] == 1:
                    StateMemo = self.Lang.InTheLine
                elif TaskInfo[i]["State"] == 2:
                    StateMemo = self.Lang.Processing
                elif TaskInfo[i]["State"] == 3:
                    StateMemo = self.Lang.Complete
                elif TaskInfo[i]["State"] == 4:
                    StateMemo = self.Lang.RequestWasAborted
                else:
                    StateMemo = "None"
                item.setText(1, StateMemo)  # 设置内容
                item.setText(2, TaskInfo[i]["TaskMemo"])  # 设置内容
                item.setText(3, str(TaskInfo[i]["ID"]))  # 设置内容
                item.setText(4, str(TaskInfo[i]["State"]))  # 设置内容
                item.setTextAlignment(
                    0, Qt.AlignHCenter | Qt.AlignVCenter
                )  # 设置item字体居中
                item.setTextAlignment(
                    1, Qt.AlignHCenter | Qt.AlignVCenter
                )  # 设置item字体居中
                item.setTextAlignment(
                    2, Qt.AlignHCenter | Qt.AlignVCenter
                )  # 设置item字体居中
                TaskItems.append(item)  # 添加到item list
            self.TaskTree.insertTopLevelItems(0, TaskItems)  # 添加到标签列表

    # 移除所有已完成的
    def RemoveFinish(self):
        Items = self.TaskTree.SelectItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                ID = int(Items[i].text(3))
                ItemState = int(Items[i].text(4))
                if ItemState == 3:
                    DirFileAction().DelOfflineTask(ID)
                    self.TaskTree.RemoveItems(Items[i])

    def AddTaskWindow(self):
        self.AddTaskWindowObj = AddTaskWindow()
        self.AddTaskWindowObj.ActionSignal.connect(self.InsertTreeData)
        self.AddTaskWindowObj.show()

    def TaskTreeRightContextMenuExec(self, pos):
        self.TaskTreeMenu = BaseMenu()  # 实例化基础Menu
        self.TaskTreeMenu.setStyleSheet(
            self.Style.Object.Download_Tree_Menu())  # 设置样式
        # 获取当前点击的item和坐标
        Item = self.TaskTree.currentItem()
        ItemAt = self.TaskTree.itemAt(pos)
        # 焦点判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:
            self.TaskTreeMenu.AddAction(
                self.Lang.Delete, lambda: self.Delete())  # 批量删除
        else:
            return
        self.TaskTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.TaskTreeMenu.show()  # 展示

    def Delete(self):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            Item = self.TaskTree.currentItem()
            Result = DirFileAction().DelOfflineTask(Item.text(3))
            if Result["State"] != True:
                MSGBOX().ERROR(self.Lang.OperationFailed)


class AddTaskWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()  # 设置信号

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setMinimumSize(600, 100)  # 初始化窗口大小

        Layout = QVBoxLayout()
        Layout.setContentsMargins(5, 5, 5, 5)

        self.URLInput = QLineEdit()
        self.URLInput.setPlaceholderText("URL")
        self.URLInput.clearFocus()
        self.URLInput.setFixedHeight(30)
        self.URLInput.setStyleSheet(
            self.Style.Object.Offline_Task_Line_Input())

        self.MemoInput = QTextEdit()
        self.MemoInput.setPlaceholderText(self.Lang.Remark)
        self.MemoInput.setStyleSheet(
            self.Style.Object.Offline_Task_Text_Input())

        BtnLayout = QHBoxLayout()

        self.AddBtn = QPushButton(self.Lang.Submit)
        self.AddBtn.setFixedHeight(30)
        self.AddBtn.clicked.connect(self.AddTaskAction)
        self.AddBtn.setStyleSheet(self.Style.Object.Offline_Task_Btn())

        self.ClearBtn = QPushButton(self.Lang.Clear)
        self.ClearBtn.setFixedSize(150, 30)
        self.ClearBtn.clicked.connect(self.CleanInputAction)
        self.ClearBtn.setStyleSheet(self.Style.Object.Offline_Task_Btn())

        BtnLayout.addWidget(self.AddBtn)
        BtnLayout.addWidget(self.ClearBtn)

        Layout.addWidget(self.URLInput)
        Layout.addWidget(self.MemoInput)
        Layout.addLayout(BtnLayout)
        self.setLayout(Layout)

    def AddTaskAction(self):
        URLStr = self.URLInput.text()
        Memo = self.MemoInput.toPlainText()
        Result = DirFileAction().CreateOfflineTask(URLStr, Memo)
        if Result["State"] == True:
            self.ActionSignal.emit()
            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)

    def CleanInputAction(self):
        self.URLInput.clear()
        self.MemoInput.clear()
