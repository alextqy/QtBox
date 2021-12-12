# -*- coding:utf-8 -*-
from interface._base import *


class DownloadListWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()  # 设置信号

    def __init__(self):
        super().__init__()

        # 下载临时目录
        self.DownloadDirPath = self.Cache.Get("UserDownloadPath")
        # 设置文件最终存储目录
        self.UserTempDir = self.Cache.Get("UserTempDir")

        self.DCache = Cache(self.DownloadDirPath)  # 实例化上传缓存
        self.setMinimumSize(700, 400)  # 初始化窗口大小
        self.ThreadPool = QThreadPool()  # 创建线程池
        self.ThreadPool.setMaxThreadCount(10000)  # 最大线程数
        self.ThreadPool.globalInstance()  # 全局设定
        self.NoneMode()  # 更改Dialog交互状态
        self.DownloadThread = QThread()  # 上传操作线程
        self.DeleteDownloadThread = QThread()  # 删除操作线程

        Layout = QVBoxLayout()  # 设置布局
        Layout.setContentsMargins(5, 5, 5, 5)  # 设置布局内边距

        self.DownloadTree = BaseTreeWidget()  # 设置tree控件
        self.DownloadTree.SetSelectionMode(2)  # 设置为多选模式
        self.DownloadTree.setStyleSheet(
            self.Style.Object.Download_Tree())  # 设置tree控件样式
        self.DownloadTree.setColumnCount(4)  # 设置tree控件列数
        self.DownloadTree.setHeaderLabels(
            [self.Lang.FileName, "FileID", self.Lang.DownloadProgress, "State"])  # 设置标题栏

        # 设置列宽度
        self.DownloadTree.setColumnWidth(0, 150)

        # 隐藏列
        self.DownloadTree.hideColumn(1)
        self.DownloadTree.hideColumn(3)
        self.DownloadTree.Connect(
            self.DownloadTreeRightContextMenuExec)  # 右键菜单
        Layout.addWidget(self.DownloadTree)
        self.setLayout(Layout)

        self.CleanUpException()
        self.ReadyToDownload()

    # 清理异常任务
    def CleanUpException(self):
        # 检查失效缓存
        FilesCache = self.DCache.Select()
        if len(FilesCache) > 0:
            for K, _ in FilesCache.items():
                if self.File.DirIsExist(self.DownloadDirPath + K) != True:
                    self.DCache.Delete(K)

        # 检查失效临时目录
        Dirs = self.File.SelectDirDirs(self.DownloadDirPath)
        if len(Dirs) > 0:
            for i in range(len(Dirs)):
                if self.DCache.Get(Dirs[i]) is None:
                    self.File.DirRemoveAll(self.DownloadDirPath + Dirs[i])

    # 未完成的下载
    def ReadyToDownload(self):
        FilesCache = self.DCache.Select()
        if len(FilesCache) > 0:
            for K, V in FilesCache.items():
                VList = self.Common.Explode("_", V)
                FileName = K
                FileID = VList[0]
                FileBlockSize = VList[1]
                POS = VList[2]
                self.InsertDownloadItem(FileName, FileID, POS, FileBlockSize)

    # 新建下载
    def DODownloadInThread(self, FileIDList):
        self.DoDownloadWorker = DoDownloadWorker(
            FileIDList, self.DownloadDirPath, self.DCache)
        self.DoDownloadWorker.ActionSignal.connect(self.InsertDownloadItem)
        self.DoDownloadWorker.BreakSignal.connect(self.ShowError)
        self.DoDownloadWorker.FinishSignal.connect(
            self.KillThread(self.DownloadThread))
        self.DoDownloadWorker.moveToThread(self.DownloadThread)
        self.DownloadThread.started.connect(
            self.DoDownloadWorker.Run)  # 设置执行方法
        self.DownloadThread.start()  # 线程启动

    # 加入下载列表
    def InsertDownloadItem(self, FileName, FileID, DownloadSize=0, TotalSize=0, State=0):
        if TotalSize == 0:
            MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
            return

        DownloadBar = QProgressBar()  # 实例化进度条控件
        DownloadBar.setStyleSheet(self.Style.Object.Bar())  # 设置样式
        DownloadBar.setMinimum(0)  # 设置最小值
        DownloadBar.setMaximum(100)  # 设置最大值
        DownloadBar.setValue(
            (int(DownloadSize)/int(TotalSize))*100)  # 初始化进度条百分比

        Item = QTreeWidgetItem()  # 实例化item控件

        # 设置item控件内容
        Item.setText(0, FileName)  # 文件名
        Item.setText(1, str(FileID))  # 文件ID
        Item.setText(2, "")  # 进度条
        Item.setText(3, str(State))  # 设置下载状态 0初始 1停止 2开始

        # tiem控件内容居中
        Item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)
        Item.setTextAlignment(3, Qt.AlignHCenter | Qt.AlignVCenter)

        # 设置鼠标提示
        Item.setToolTip(0, Item.text(0))
        Item.setToolTip(1, Item.text(0))
        Item.setToolTip(2, Item.text(0))
        Item.setToolTip(3, Item.text(0))

        # 添加item到列表
        self.DownloadTree.addTopLevelItem(Item)

        # 添加进度条到item控件
        self.DownloadTree.setItemWidget(Item, 2, DownloadBar)

        if State != 0:
            self.MoveToThreadPool(Item)

    # 右键
    def DownloadTreeRightContextMenuExec(self, pos):
        self.DownloadTreeMenu = BaseMenu()  # 实例化基础Menu
        self.DownloadTreeMenu.setStyleSheet(
            self.Style.Object.Download_Tree_Menu())  # 设置样式

        # 获取当前点击的item和坐标
        Item = self.DownloadTree.currentItem()
        ItemAt = self.DownloadTree.itemAt(pos)

        # 焦点判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:
            self.DownloadTreeMenu.AddAction(
                self.Lang.Start, lambda: self.Start())
            self.DownloadTreeMenu.AddAction(
                self.Lang.Stop, lambda: self.Stop())
            self.DownloadTreeMenu.AddAction(
                self.Lang.Delete, lambda: self.Delete())  # 批量删除
        else:
            self.DownloadTreeMenu.AddAction(
                self.Lang.RemoveAllCompletedTasks, lambda: self.RemoveFinish())  # 清理上传完成的数据

        self.DownloadTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.DownloadTreeMenu.show()  # 展示

    # 开始
    def Start(self):
        Items = self.DownloadTree.selectedItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                Items[i].setText(3, str(2))
                self.MoveToThreadPool(Items[i])

    # 停止
    def Stop(self):
        Items = self.DownloadTree.selectedItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                FileName = Items[i].text(0)
                FileID = Items[i].text(1)
                FileCache = self.Common.Explode("_", self.DCache.Get(FileName))
                FileBlockSize = FileCache[1]
                POS = len(self.File.SelectDirFiles(
                    self.DownloadDirPath + FileName))
                self.DCache.Set(FileName, FileID + "_" +
                                FileBlockSize + "_" + str(POS + 1))
                Items[i].setText(3, str(1))  # 设置下载状态 0初始 1停止 2开始

    # 删除任务
    def Delete(self):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            Items = self.DownloadTree.selectedItems()
            self.DoDeleteWorker = DoDeleteWorker(
                Items, self.DownloadDirPath, self.DownloadTree)
            self.DoDeleteWorker.BreakSignal.connect(self.ShowError)
            self.DoDeleteWorker.DeleteCacheSignal.connect(
                self.DCache.Delete)
            self.DoDeleteWorker.RemoveItemsSignal.connect(
                self.DownloadTree.RemoveItems)
            self.DoDeleteWorker.FinishSignal.connect(
                self.KillThread(self.DeleteDownloadThread))
            self.DoDeleteWorker.moveToThread(self.DeleteDownloadThread)
            self.DeleteDownloadThread.started.connect(
                self.DoDeleteWorker.Run)  # 设置执行方法
            self.DeleteDownloadThread.start()  # 线程启动

    # 移除所有已完成的
    def RemoveFinish(self):
        Items = self.DownloadTree.SelectItems()
        if len(Items) > 0:
            for i in range(len(Items)):
                Bar = self.DownloadTree.itemWidget(Items[i], 2)  # 获取进度条控件
                if Bar != None and Bar.value() == 100 or Bar == None:  # 上传完毕只移除任务
                    self.DownloadTree.RemoveItems(Items[i])

    # 移动到线程池
    def MoveToThreadPool(self, Item):
        GoUpload = DownloadHandler(
            Item, self.DownloadDirPath, self.UserTempDir, self.DCache)  # 实例化上传操作类
        GoUpload.ErrorSignal.connect(self.ShowError)
        GoUpload.SetBarBusySwitchSignal.connect(self.SetBarBusySwitch)
        GoUpload.SetBarValueSignal.connect(self.SetBarValue)

        # 实例化工作类
        Worker = DownloadWorker(GoUpload)

        # 把工作类放入到线程池内 并启动任务
        self.ThreadPool.start(Worker)

    # 错误提示
    def ShowError(self, Content):
        MSGBOX().ERROR(Content)

    # 设置进度条状态
    def SetBarBusySwitch(self, Item, Min=0, Max=100):
        ProgressBar = self.DownloadTree.itemWidget(Item, 2)  # 获取进度条控件
        ProgressBar.setMinimum(Min)
        ProgressBar.setMaximum(Max)

    # 更新进度条
    def SetBarValue(self, Item, Value):
        ProgressBar = self.DownloadTree.itemWidget(Item, 2)  # 获取进度条控件
        if ProgressBar != None:
            ProgressBar.setValue(Value)

# 连接池线程类


class DownloadWorker(QRunnable):
    def __init__(self, DownloadObject):
        super(DownloadWorker, self).__init__()
        self.DownloadObject = DownloadObject

    # 启动 run 为小写
    @Slot()
    def run(self):
        self.DownloadObject.Run()

# 下载处理


class DownloadHandler(BaseInterface, BaseObject):
    ErrorSignal = Signal(str)
    SetBarBusySwitchSignal = Signal(QObject, int, int)
    SetBarValueSignal = Signal(QObject, int)

    def __init__(self, Item, DownloadDirPath, TempDir, DCache):
        super().__init__()
        self.Item = Item
        self.DownloadDirPath = DownloadDirPath
        self.TempDir = TempDir
        self.DCache = DCache

    def Run(self):
        # 设置进度条忙碌状态
        self.SetBarBusySwitchSignal.emit(self.Item, 0, 0)

        FileName = self.Item.text(0)

        # 获取缓存中已下载文件数
        CacheFiles = self.Common.Explode("_", self.DCache.Get(FileName))
        FileID = int(CacheFiles[0])
        FileBlockSize = int(CacheFiles[1])
        POS = int(CacheFiles[2])

        # 获取已下载文件数量
        Files = self.File.SelectDirFiles(self.DownloadDirPath + FileName)
        if len(Files) > 0:
            POS = len(Files)

        # 还原进度条状态
        self.SetBarBusySwitchSignal.emit(self.Item, 0, 100)

        # 数值初始化
        self.SetBarValueSignal.emit(
            self.Item, ceil((POS/FileBlockSize)*100))

        i = 1
        while True:
            _POS = POS + i

            # 停止 并且记录刻度
            if int(self.Item.text(3)) == 1:
                self.FinishSignal.emit()
                return

            # 是否下载完毕
            if _POS > FileBlockSize:
                self.FinishSignal.emit()
                break

            # 读取文件分片
            Result = DirFileAction().DownloadFileEntity(FileID, _POS)
            if Result["State"] != True:
                self.ErrorSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                self.FinishSignal.emit()
                return
            FileEntityName = Result["FileEntityName"]
            Data = Result["Data"]
            Content = self.Common.Base64ToBytes(
                self.Common.StringToBytes(Data))

            # 新建实体文件分片
            try:
                FileEntityPath = self.DownloadDirPath + FileName + "/" + FileEntityName
                self.File.MkFile(FileEntityPath)
            except Exception as e:
                self.ErrorSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                self.FinishSignal.emit()
                return

            # 写入数据
            try:
                self.File.WFileInByte(FileEntityPath, Content)
            except Exception as e:
                self.ErrorSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                self.FinishSignal.emit()
                return

            self.SetBarValueSignal.emit(
                self.Item, ceil((_POS/FileBlockSize)*100))

            i += 1

        self.SetBarBusySwitchSignal.emit(self.Item, 0, 0)

        # 获取文件信息
        CheckFile = DirFileAction().CheckFile(FileID)
        if CheckFile["State"] != True:
            self.ErrorSignal.emit(FileName + " " + self.Lang.OperationFailed)
            self.FinishSignal.emit()
            return

        # 删除同名文件
        NewFile = self.TempDir + FileName + \
            "." + CheckFile["Data"]["FileType"]
        if self.File.FileIsExist(NewFile) == True:
            try:
                self.File.DeleteFile(NewFile)
            except Exception as e:
                self.ErrorSignal.emit(
                    FileName + " " + self.Lang.TemporaryFileCleanupFailed)
                self.FinishSignal.emit()
                return

        # 文件合并
        if self.File.MergeFile(self.DownloadDirPath + FileName, self.TempDir, FileName + "." + CheckFile["Data"]["FileType"]) == False:
            self.ErrorSignal.emit(self.Lang.FileMergeFailed)
            self.FinishSignal.emit()
            return

        # 删除下载缓存
        self.DCache.Delete(FileName)

        # 删除临时文件分片文件夹
        try:
            self.File.DirRemoveAll(self.DownloadDirPath + FileName)
        except Exception as e:
            self.ErrorSignal.emit(
                self.DownloadDirPath + FileName + " " + self.Lang.TemporaryFileCleanupFailed)
            self.FinishSignal.emit()
            return

        self.SetBarBusySwitchSignal.emit(self.Item, 0, 100)
        self.SetBarValueSignal.emit(self.Item, 100)

        self.FinishSignal.emit()

# 新建下载


class DoDownloadWorker(BaseInterface, BaseObject):
    ActionSignal = Signal(str, int, int, int, int)
    BreakSignal = Signal(str)

    def __init__(self, FilesIDList, DownloadDirPath, DCache):
        super().__init__()
        self.FilesIDList = FilesIDList
        self.DownloadDirPath = DownloadDirPath
        self.DCache = DCache

    def Run(self):
        if len(self.FilesIDList) == 0:
            self.BreakSignal.emit(self.Lang.OperationFailed)
            self.FinishSignal.emit()
            return

        if self.DownloadDirPath == "":
            self.BreakSignal.emit(self.Lang.OperationFailed)
            self.FinishSignal.emit()
            return

        for i in range(len(self.FilesIDList)):
            Result = DirFileAction().CheckFile(
                int(self.FilesIDList[i]["ID"]))
            if Result["State"] != True:
                self.BreakSignal.emit(
                    self.FilesIDList["FileName"] + " " + self.Lang.OperationFailed)
                self.FinishSignal.emit()
                return
            FileInfo = Result["Data"]
            ID = FileInfo["ID"]
            FileName = FileInfo["FileName"]
            # FileType = FileInfo["FileType"]
            FileBlockSize = FileInfo["BlockSize"]
            DownloadSize = 0
            # Createtime = FileInfo["Createtime"]

            if FileInfo["State"] != 2:
                self.BreakSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                self.FinishSignal.emit()
                return

            if self.DCache.Get(FileName) is not None:
                self.BreakSignal.emit(
                    FileName + " " + self.Lang.AlreadyInTheList)
                self.FinishSignal.emit()
                return

            # 如果存在相同目录 则删除
            if self.File.DirIsExist(self.DownloadDirPath + FileName) == True:
                try:
                    self.File.DirRemoveAll()
                except Exception as e:
                    self.BreakSignal.emit(
                        FileName + " " + self.Lang.OperationFailed)
                    self.FinishSignal.emit()
                    return

            # 建立临时下载目录
            try:
                self.File.MkDir(self.DownloadDirPath + FileName)
            except Exception as e:
                self.BreakSignal.emit(
                    FileName + " " + self.Lang.OperationFailed)
                self.FinishSignal.emit()
                return

            self.DCache.Set(
                FileName, str(ID) + "_" + str(FileBlockSize) + "_" + str(DownloadSize))

            # 开始下载
            self.ActionSignal.emit(
                FileName, ID, DownloadSize, FileBlockSize, 2)

        self.FinishSignal.emit()

# 删除任务


class DoDeleteWorker(BaseInterface, BaseObject):
    BreakSignal = Signal(str)
    DeleteCacheSignal = Signal(str)
    RemoveItemsSignal = Signal(QObject)

    def __init__(self, Items, DownloadDirPath, DownloadTree):
        super().__init__()
        self.Items = Items
        self.DownloadDirPath = DownloadDirPath
        self.DownloadTree = DownloadTree

    def Run(self):
        if len(self.Items) == 0:
            self.FinishSignal.emit()
            return

        if self.DownloadDirPath == "":
            self.BreakSignal.emit(self.Lang.OperationFailed)
            self.FinishSignal.emit()
            return

        if self.DownloadTree == None:
            self.BreakSignal.emit(self.Lang.OperationFailed)
            return

        for i in range(len(self.Items)):
            FileName = self.Items[i].text(0)

            Bar = self.DownloadTree.itemWidget(self.Items[i], 2)  # 获取进度条控件
            if Bar != None and Bar.value() != 100 or Bar == None:  # 未上传完毕则移除临时文件夹
                self.File.DirRemoveAll(self.DownloadDirPath + FileName)

            self.RemoveItemsSignal.emit(self.Items[i])
            self.DeleteCacheSignal.emit(FileName)

        self.FinishSignal.emit()
