# -*- coding:utf-8 -*-
from email.charset import QP
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
        self.TaskTree.setColumnCount(3)  # 设置tree控件列数
        self.TaskTree.setHeaderLabels(
            ["URL", self.Lang.TaskStatus, self.Lang.Remark])  # 设置标题栏
        self.TaskTree.setColumnWidth(0, 300)  # 设置列宽度
        # self.TaskTree.Connect(self.TaskTreeRightContextMenuExec)  # 右键菜单

        BtnLayout = QHBoxLayout()
        BtnLayout.setContentsMargins(0, 0, 0, 0)  # 设置布局内边距

        self.AddTaskBtn = QPushButton(self.Lang.AddTask)
        self.AddTaskBtn.setFixedHeight(30)
        # self.AddTaskBtn.setStyleSheet()
        self.AddTaskBtn.clicked.connect(self.AddTaskWindow)

        self.RefreshBtn = QPushButton(self.Lang.Refresh)
        self.RefreshBtn.setFixedSize(150, 30)
        # self.RefreshBtn.setStyleSheet()

        Layout.addWidget(self.TaskTree)
        BtnLayout.addWidget(self.AddTaskBtn)
        BtnLayout.addWidget(self.RefreshBtn)
        Layout.addLayout(BtnLayout)
        self.setLayout(Layout)

    def AddTaskWindow(self):
        self.AddTaskWindowObj = AddTaskWindow()
        self.AddTaskWindowObj.show()


class AddTaskWindow(BaseInterface, BaseDialog):
    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setMinimumSize(600, 100)  # 初始化窗口大小

        Layout = QVBoxLayout()
        Layout.setContentsMargins(5, 5, 5, 5)

        self.URLInput = QLineEdit()
        self.URLInput.setPlaceholderText("URL")
        self.URLInput.clearFocus()
        # self.URLInput.setAlignment(
        #     Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        # )  # 内容居中
        self.URLInput.setFixedHeight(30)
        # self.URLInput.setStyleSheet()

        self.MemoInput = QTextEdit()
        self.MemoInput.setPlaceholderText(self.Lang.Remark)
        # self.MemoInput.setAlignment(
        #     Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter
        # )  # 内容居中

        BtnLayout = QHBoxLayout()

        self.AddBtn = QPushButton(self.Lang.Submit)
        self.AddBtn.setFixedHeight(30)
        self.AddBtn.clicked.connect(self.AddTaskAction)

        self.ClearBtn = QPushButton(self.Lang.Clear)
        self.ClearBtn.setFixedSize(150, 30)
        self.ClearBtn.clicked.connect(self.CleanInputAction)

        BtnLayout.addWidget(self.AddBtn)
        BtnLayout.addWidget(self.ClearBtn)

        Layout.addWidget(self.URLInput)
        Layout.addWidget(self.MemoInput)
        Layout.addLayout(BtnLayout)
        self.setLayout(Layout)

    def AddTaskAction(self):
        print("Add task")

    def CleanInputAction(self):
        self.URLInput.clear()
        self.MemoInput.clear()
