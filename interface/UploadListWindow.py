# -*- coding:utf-8 -*-
from interface._base import *


class UploadListWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal(str)  # 设置信号

    def __init__(self):
        super().__init__()
        self.UploadDirPath = self.Cache.Get("UserUploadPath")  # 上传临时目录
        self.FileSliceSize = 0
        ConfigInfo = ConfigAction().CheckConfig(2)  # 获取文件分片大小限制
        if ConfigInfo["State"] != True:
            self.FileSliceSize = FILESLICESIZE
        else:
            self.FileSliceSize = ConfigInfo["Data"]["ConfigValue"]
        self.UCache = Cache(self.UploadDirPath)  # 实例化下载缓存
        self.setMinimumSize(700, 400)  # 初始化窗口大小
        self.ThreadPool = QThreadPool()  # 创建线程池
        self.ThreadPool.setMaxThreadCount(10000)  # 最大线程数
        self.ThreadPool.globalInstance()  # 全局设定
        self.NoneMode()  # 更改Dialog交互状态
        self.UploadThread = QThread()  # 上传操作线程
        self.DeleteUploadThread = QThread()  # 删除操作线程

        Layout = QVBoxLayout()  # 设置布局
        Layout.setContentsMargins(5, 5, 5, 5)  # 设置布局内边距

        self.UploadTree = BaseTreeWidget()  # 设置tree控件
        self.UploadTree.SetSelectionMode(2)  # 设置为多选模式
        self.UploadTree.setStyleSheet(
            self.Style.Object.Upload_Tree())  # 设置tree控件样式
        self.UploadTree.setColumnCount(6)  # 设置tree控件列数
        self.UploadTree.setHeaderLabels([
            self.Lang.UploadSourcePath,
            "FileID",
            self.Lang.UploadDestinationFolder,
            "DirID",
            self.Lang.UploadProgress,
            "State"
        ])  # 设置标题栏

        # 设置列宽度
        self.UploadTree.setColumnWidth(0, 150)
        self.UploadTree.setColumnWidth(2, 200)
        self.UploadTree.setColumnWidth(4, 300)

        # 隐藏列
        self.UploadTree.hideColumn(1)
        self.UploadTree.hideColumn(3)
        self.UploadTree.hideColumn(5)

        self.UploadTree.Connect(self.UploadTreeRightContextMenuExec)  # 右键菜单

        Layout.addWidget(self.UploadTree)
        self.setLayout(Layout)
        self.ReadyToUpload()

    # 未完成的上传
    def ReadyToUpload(self):
        Result = DirFileAction().FileList(0, 1)
        if Result["ResultStatus"] != True:
            MSGBOX().WARNING(self.Lang.UnableToObtainNotBeenUploaded)
            return
        Files = Result["Data"]
        if len(Files) > 0:
            for i in range(len(Files)):
                FilePath = Files[i]["UploadPath"]
                FileID = Files[i]["ID"]
                DirID = Files[i]["DirID"]
                UploadSize = Files[i]["UploadBlockSize"]
                TotalSize = Files[i]["BlockSize"]

                DirInfo = DirFileAction().DirInfo(DirID)
                if DirInfo["State"] != True:
                    DestDirName = ""
                else:
                    DestDirName = DirInfo["Data"]["DirName"]
                self.InsertUploadItem(
                    FilePath, FileID, DestDirName, DirID, UploadSize, TotalSize, 0)

    # 新增上传线程方法
    def DOUploadInThread(self, FilesPath, DirID):
        self.DoUploadWorker = DoUploadWorker(
            FilesPath, DirID, self.UploadDirPath)

        self.DoUploadWorker.ActionSignal.connect(self.InsertUploadItem)
        self.DoUploadWorker.BreakSignal.connect(self.ShowError)
        self.DoUploadWorker.FinishSignal.connect(
            self.KillThread(self.UploadThread))
        self.DoUploadWorker.moveToThread(self.UploadThread)
        self.UploadThread.started.connect(
            self.DoUploadWorker.Run)  # 设置执行方法
        self.UploadThread.start()  # 线程启动

    # 添加上传数据
    def InsertUploadItem(self, FilePath, FileID, DirName, DirID, UploadedSize=0, TotalSize=0, State=0):
        if TotalSize == 0:
            MSGBOX().ERROR(FilePath + " " + self.Lang.OperationFailed)
            return

        UploadBar = QProgressBar()  # 实例化进度条控件
        UploadBar.setStyleSheet(self.Style.Object.Bar())  # 设置样式
        UploadBar.setMinimum(0)  # 设置最小值
        UploadBar.setMaximum(100)  # 设置最大值
        UploadBar.setValue((int(UploadedSize)/int(TotalSize))*100)  # 初始化进度条百分比

        Item = QTreeWidgetItem()  # 实例化item控件

        # 设置item控件内容
        Item.setText(0, FilePath)  # 来源路径
        Item.setText(1, str(FileID))  # 文件ID
        Item.setText(2, DirName)  # 目标文件夹名称
        Item.setText(3, str(DirID))  # 文件夹ID
        Item.setText(4, "")  # 进度条
        Item.setText(5, str(State))  # 设置下载状态 0初始 1停止 2开始

        # tiem控件内容居中
        Item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(3, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(4, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(5, Qt.AlignHCenter | Qt.AlignVCenter)

        FileName = self.File.CheckFileName(
            FilePath) + self.File.CheckFileType(FilePath)

        # 设置鼠标提示
        Item.setToolTip(0, FileName)
        Item.setToolTip(1, FileName)
        Item.setToolTip(2, FileName)
        Item.setToolTip(3, FileName)
        Item.setToolTip(4, FileName)
        Item.setToolTip(5, FileName)

        # 添加item到列表
        self.UploadTree.addTopLevelItem(Item)

        # 添加进度条到item控件
        self.UploadTree.setItemWidget(Item, 4, UploadBar)

        if State != 0:
            self.MoveToThreadPool(Item)

    # 右键功能
    def UploadTreeRightContextMenuExec(self, pos):
        self.UploadTreeMenu = BaseMenu()  # 实例化基础Menu
        self.UploadTreeMenu.setStyleSheet(
            self.Style.Object.Upload_Tree_Menu())  # 设置样式

        # 获取当前点击的item和坐标
        Item = self.UploadTree.currentItem()
        ItemAt = self.UploadTree.itemAt(pos)

        # 焦点判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:
            self.UploadTreeMenu.AddAction(
                self.Lang.Start, lambda: self.Start())
            self.UploadTreeMenu.AddAction(self.Lang.Stop, lambda: self.Stop())
            self.UploadTreeMenu.AddAction(
                self.Lang.Delete, lambda: self.Delete())  # 批量删除
        else:
            self.UploadTreeMenu.AddAction(
                self.Lang.RemoveAllCompletedTasks, lambda: self.RemoveFinish())  # 清理上传完成的数据

        self.UploadTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.UploadTreeMenu.show()  # 展示

    # 开始 / 继续
    def Start(self):
        Items = self.UploadTree.selectedItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                Items[i].setText(5, str(2))
                self.MoveToThreadPool(Items[i])

    # 停止
    def Stop(self):
        Items = self.UploadTree.selectedItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                Items[i].setText(5, str(1))

    # 删除任务
    def Delete(self):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:

            Items = self.UploadTree.selectedItems()
            self.DoDeleteWorker = DoDeleteWorker(
                Items, self.UploadDirPath, self.UploadTree)

            self.DoDeleteWorker.BreakSignal.connect(self.ShowError)
            self.DoDeleteWorker.RemoveItemsSignal.connect(
                self.UploadTree.RemoveItems)
            self.DoDeleteWorker.FinishSignal.connect(
                self.KillThread(self.DeleteUploadThread))
            self.DoDeleteWorker.moveToThread(self.DeleteUploadThread)
            self.DeleteUploadThread.started.connect(
                self.DoDeleteWorker.Run)  # 设置执行方法
            self.DeleteUploadThread.start()  # 线程启动

    # 移除所有已完成的
    def RemoveFinish(self):
        Items = self.UploadTree.SelectItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                Bar = self.UploadTree.itemWidget(Items[i], 4)  # 获取进度条控件
                if Bar != None and Bar.value() == 100 or Bar == None:  # 上传完毕只移除任务
                    self.UploadTree.RemoveItems(Items[i])

    # 移动到线程池
    def MoveToThreadPool(self, Item):
        GoUpload = UploadHandler(Item, self.UploadDirPath)  # 实例化上传操作类
        GoUpload.ErrorSignal.connect(self.ShowError)
        GoUpload.SetBarBusySwitchSignal.connect(self.SetBarBusySwitch)
        GoUpload.SetBarValueSignal.connect(self.SetBarValue)

        # 实例化工作类
        Worker = UploadWorker(GoUpload)

        # 把工作类放入到线程池内 并启动任务
        self.ThreadPool.start(Worker)

    # 错误提示
    def ShowError(self, Content):
        MSGBOX().ERROR(Content)

    # 设置进度条状态
    def SetBarBusySwitch(self, Item, Min=0, Max=100):
        ProgressBar = self.UploadTree.itemWidget(Item, 4)  # 获取进度条控件
        ProgressBar.setMinimum(Min)
        ProgressBar.setMaximum(Max)

    # 更新进度条
    def SetBarValue(self, Item, Value):
        ProgressBar = self.UploadTree.itemWidget(Item, 4)  # 获取进度条控件
        if ProgressBar != None:
            ProgressBar.setValue(Value)

# 连接池线程类


class UploadWorker(QRunnable):
    def __init__(self, UploadObject):
        super(UploadWorker, self).__init__()
        self.UploadObject = UploadObject

    # 启动 run 为小写
    @Slot()
    def run(self):
        self.UploadObject.Run()

# 上传处理


class UploadHandler(BaseInterface, BaseObject):
    ErrorSignal = Signal(str)
    SetBarBusySwitchSignal = Signal(QObject, int, int)
    SetBarValueSignal = Signal(QObject, int)

    def __init__(self, Item, UploadDirPath):
        super().__init__()
        self.Item = Item
        self.UploadDirPath = UploadDirPath

    def Run(self):
        # 设置进度条忙碌状态
        self.SetBarBusySwitchSignal.emit(self.Item, 0, 0)

        # 获取文件信息
        FileName = self.File.CheckFileName(self.Item.text(0))
        ID = self.Item.text(1)
        Result = DirFileAction().CheckFile(ID)
        if Result["ResultStatus"] != True:
            self.ErrorSignal.emit(FileName + " " + self.Lang.OperationFailed)
            return
        FileInfo = Result["Data"]
        FileName = FileInfo["FileName"]
        State = FileInfo["State"]
        FileSize = FileInfo["FileSize"]
        BlockSize = FileInfo["BlockSize"]  # 总分片数
        UploadBlockSize = FileInfo["UploadBlockSize"]  # 已上传的分片数
        DirID = FileInfo["DirID"]
        FileMD5 = FileInfo["MD5"]
        UploadPath = FileInfo["UploadPath"]
        Createtime = FileInfo["Createtime"]

        # 解析并修改文件MD5信息
        if FileMD5 == "":
            FileMD5 = self.File.CheckFileMD5(UploadPath)
            ModifyFileResult = DirFileAction().ModifyFile(
                ID, FileName, State, FileSize, BlockSize, UploadBlockSize, DirID, FileMD5)
            if ModifyFileResult["ResultStatus"] != True:
                self.ErrorSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                return

        # 设置临时上传文件夹
        TempUploadDir = self.UploadDirPath + FileName + "." + str(Createtime)
        if self.File.DirIsExist(TempUploadDir) != True:
            self.File.MkDir(TempUploadDir)

        # 获取该目录下的文件
        _, FileSlice = self.File.SelectDir(TempUploadDir)
        FileSliceLen = len(FileSlice)

        # 是否需要从新切片
        if FileSliceLen == 0:
            # 获取实体文件信息
            if self.File.FileIsExist(UploadPath) != True:
                self.ErrorSignal.emit(self.Lang.FileDoesNotExist)
                return

            # 文件切片
            SliceState, _ = self.File.CutFile(
                UploadPath, TempUploadDir, FILESLICESIZE)
            if SliceState != True:
                self.ErrorSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                return

            # 再次获取文件分片数
            _, FileSlice = self.File.SelectDir(TempUploadDir)

        ReadyToUploadArr = FileSlice[UploadBlockSize:BlockSize]

        # 还原进度条显示
        self.SetBarBusySwitchSignal.emit(self.Item, 0, 100)

        self.SetBarValueSignal.emit(
            self.Item, ceil((UploadBlockSize/BlockSize)*100))

        PerPos = UploadBlockSize  # 上传刻度
        for i in range(len(ReadyToUploadArr)):
            if int(self.Item.text(5)) == 1:
                return

            # 每个实体文件切片路径
            FileSlicePerPath = TempUploadDir + "/" + ReadyToUploadArr[i]
            PerPos = PerPos + 1

            # 上传实体文件
            Result1 = DirFileAction().UploadFileEntity(
                ID, ReadyToUploadArr[i], FileSlicePerPath)
            if Result1["State"] != True and Result1["Memo"] == "Nnoe":
                return
            if Result1["State"] != True and Result1["Memo"] != "Nnoe":
                self.ErrorSignal.emit(
                    FileInfo["FileName"] + " " + self.Lang.OperationFailed)
                return

            self.SetBarValueSignal.emit(
                self.Item, floor((PerPos/BlockSize)*100))

        ResultForComplete = DirFileAction().CheckFile(ID)
        if ResultForComplete["State"] != True:
            self.ErrorSignal.emit(self.Lang.FailedToDeleteTempDir)
            return
        InfoForComplete = ResultForComplete["Data"]

        # 删除上传临时目录
        if InfoForComplete["UploadBlockSize"] == InfoForComplete["BlockSize"]:
            self.File.DirRemoveAll(TempUploadDir)


# 新建上传处理线程类


class DoUploadWorker(BaseInterface, BaseObject):
    ActionSignal = Signal(str, int, str, int, int, int, int)
    BreakSignal = Signal(str)

    def __init__(self, FileList=[], DirID=0, UploadDirPath=""):
        super().__init__()
        self.FileList = FileList
        self.DirID = DirID
        self.UploadDirPath = UploadDirPath

    def Run(self):
        if len(self.FileList) == 0:
            self.FinishSignal.emit()
            return

        if self.DirID == 0:
            self.FinishSignal.emit()
            return

        if self.UploadDirPath == "":
            self.FinishSignal.emit()
            return

        for i in range(len(self.FileList)):
            # 获取上传目标文件夹信息
            Result1 = DirFileAction().DirInfo(self.DirID)
            if Result1["State"] != True:
                self.BreakSignal.emit(self.Lang.WrongFolderData)
                return
            DirData = Result1["Data"]
            DestDirName = DirData["DirName"]
            if DirData["ParentID"] == 0:
                DestDirName = self.Lang.RootDirectory

            # 新建文件
            FileName = self.File.CheckFileName(self.FileList[i])
            FileType = self.File.CheckFileType(self.FileList[i])
            FileSize = self.File.CheckFileSize(self.FileList[i])

            if FileName == "":
                self.BreakSignal.emit(self.Lang.WrongFileNameFormat)
                return

            # 新建文件
            Result2 = DirFileAction().CreateFile(
                FileName, FileType, FileSize, self.FileList[i], self.DirID, "")
            if Result2["State"] != True:
                if Result2["Memo"] == "FileType error":
                    self.BreakSignal.emit(
                        FileName + " " + self.Lang.WrongFileType)
                else:
                    self.BreakSignal.emit(
                        FileName + " " + self.Lang.OperationFailed)
                return

            # 获取文件详情
            Result3 = DirFileAction().CheckFile(Result2["ID"])
            if Result3["State"] != True:
                self.BreakSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                return

            FileID = Result3["Data"]["ID"]
            UploadSize = Result3["Data"]["UploadBlockSize"]  # 已上传分片数
            TotalSize = Result3["Data"]["BlockSize"]  # 总分片数

            # 加入上传列表
            self.ActionSignal.emit(
                self.FileList[i], FileID, DestDirName, self.DirID, UploadSize, TotalSize, 2)

# 删除任务


class DoDeleteWorker(BaseInterface, BaseObject):
    BreakSignal = Signal(str)
    RemoveItemsSignal = Signal(QObject)

    def __init__(self, Items, UploadDirPath="", UploadTree=None):
        super().__init__()
        self.Items = Items
        self.UploadDirPath = UploadDirPath
        self.UploadTree = UploadTree

    def Run(self):
        if len(self.Items) == 0:
            self.FinishSignal.emit()
            return

        if self.UploadDirPath == "":
            self.BreakSignal.emit(self.Lang.OperationFailed)
            self.FinishSignal.emit()
            return

        if self.UploadTree == None:
            self.BreakSignal.emit(self.Lang.OperationFailed)
            self.FinishSignal.emit()
            return

        for i in range(len(self.Items)):
            ID = self.Items[i].text(1)
            FileName = self.Items[i].text(0)

            Bar = self.UploadTree.itemWidget(self.Items[i], 4)  # 获取进度条控件
            if Bar != None and Bar.value() == 100 or Bar == None:  # 上传完毕只移除任务
                self.RemoveItemsSignal.emit(self.Items[i])
            else:
                # 获取文件详情
                Result1 = DirFileAction().CheckFile(ID)
                if Result1["State"] != True:
                    self.BreakSignal.emit(
                        FileName + " " + self.Lang.OperationFailed)
                    break
                FileInfo = Result1["Data"]

                try:
                    # 删除临时上传文件夹
                    self.File.DirRemoveAll(
                        self.UploadDirPath + FileInfo["FileName"] + "." + str(FileInfo["Createtime"]))
                except Exception as e:
                    self.BreakSignal.emit(
                        FileName + " " + self.Lang.OperationFailed)
                    break

                # 删除文件数据
                Result2 = DirFileAction().DeleteFile(ID)
                if Result2["State"] != True:
                    self.BreakSignal.emit(
                        FileName + " " + self.Lang.OperationFailed)
                    break

                self.RemoveItemsSignal.emit(self.Items[i])
        self.FinishSignal.emit()
