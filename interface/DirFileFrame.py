# -*- coding:utf-8 -*-
from interface._base import *


class DirFileFrame(BaseInterface, BaseFrame):
    UploadSignal = Signal(list, int)
    DownloadSignal = Signal(list)
    RefreshFileTagListSignal = Signal()

    def __init__(self):
        super().__init__()

        # =========================================== Ready ===========================================
        self.RecycleBinState = False  # 回收站状态

        # 获取个人根文件夹数据
        SelectDirData = DirFileAction().SelectDir()
        if SelectDirData["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        self.DirData = SelectDirData["Data"]
        self.CurrentDirID = SelectDirData["ID"]

        self.PasteFileThread = QThread()
        self.FileSyncThread = QThread()
        self.PromptPopUpsThread = QThread()

        self.PromptPopUpsWindow = PromptPopUpsWindow()

        self.TCache = Cache(self.Cache.Get("TempDir"))  # 在线预览缓存

        # =========================================== 文件夹 ===========================================
        self.DirVS = self.VS()

        # 文件夹标题栏
        self.DirHeader = RootDirectoryLabel(self.Lang.RootDirectory)
        self.DirHeader.setFixedHeight(20)
        self.DirHeader.setAlignment(Qt.AlignCenter)  # 字体居中
        self.DirHeader.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Header())  # 设置样式
        self.DirHeader.ActionSignal.connect(self.ShowRootFiles)  # 连接槽函数

        # 文件夹列表
        self.DirTree = BaseTreeWidget()  # 实例化树形控件
        self.DirTree.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Tree_Widget())  # 设置样式
        self.DirTree.HideVScroll()  # 隐藏纵向滚动条
        self.DirTree.setColumnCount(3)  # 设置列数
        self.DirTree.hideColumn(1)  # 隐藏列
        self.DirTree.hideColumn(2)  # 隐藏列
        self.DirTree.setHeaderLabels(["DirName", "ID", "ParentID"])  # 设置标题栏
        self.DirTree.setHeaderHidden(True)  # 隐藏标题栏
        self.DirTree.setAcceptDrops(True)  # 开启接收拖动
        self.DirTree.MoveSignal.connect(self.CheckMoveTreeItems)  # 链接槽函数

        DirTreeItems = []
        if len(self.DirData) > 0:
            for i in range(len(self.DirData)):
                item = QTreeWidgetItem()  # 设置item控件
                item.setText(0, self.DirData[i]["DirName"])  # 设置内容
                item.setText(1, str(self.DirData[i]["ID"]))  # 设置内容
                item.setText(2, str(self.DirData[i]["ParentID"]))  # 文件夹上级目录ID
                item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                DirTreeItems.append(item)  # 添加到item list
            self.DirTree.insertTopLevelItems(0, DirTreeItems)  # 添加到文件夹列表

        # 鼠标左键点击事件
        self.DirTree.clicked.connect(self.DirItemClicked)

        # 鼠标右键 链接槽函数
        self.DirTree.Connect(self.DirRightContextMenuExec)

        # 文件夹列表下方按钮
        self.DirListBtnFrame = QFrame()
        self.DirListBtnFrame.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_List_Btn_Frame())
        # self.DirListBtnFrame.setFixedHeight(65)
        self.DirListBtnFrame.setFixedHeight(30)
        self.DirListBtnFrame.setContentsMargins(0, 0, 0, 0)

        self.DirListBtnLayout = QVBoxLayout()
        self.DirListBtnLayout.setContentsMargins(0, 0, 0, 0)

        # self.DirListBtnLayout.addStretch()

        self.NewDirBtn = QPushButton(self.Lang.NewFolder)
        self.NewDirBtn.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_List_Btn())
        self.NewDirBtn.setContentsMargins(1, 1, 1, 1)
        self.NewDirBtn.setFixedHeight(30)
        self.NewDirBtn.clicked.connect(self.CreateTopDirWindow)

        self.DownloadDir = QPushButton(self.Lang.DownloadedFiles)
        self.DownloadDir.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_List_Btn())
        self.DownloadDir.setContentsMargins(1, 1, 1, 1)
        self.DownloadDir.setFixedHeight(30)
        self.DownloadDir.clicked.connect(self.OpenDownloadDirWindow)

        self.HBtnLayout = QHBoxLayout()
        self.HBtnLayout.setContentsMargins(0, 0, 0, 0)

        # self.FilesSyncBtn = QPushButton(self.Lang.SynchronizeModifiedFiles)
        # self.FilesSyncBtn.setStyleSheet(
        #     self.Style.Object.MainFrame_Mid_Dir_List_Btn())
        # self.FilesSyncBtn.setContentsMargins(1, 1, 1, 1)
        # self.FilesSyncBtn.setFixedHeight(30)
        # self.FilesSyncBtn.clicked.connect(self.FileSync)

        self.HBtnLayout.addWidget(self.NewDirBtn)
        self.HBtnLayout.addWidget(self.DownloadDir)
        self.DirListBtnLayout.addLayout(self.HBtnLayout)
        # self.DirListBtnLayout.addWidget(self.FilesSyncBtn)
        self.DirListBtnFrame.setLayout(self.DirListBtnLayout)

        self.DirVS.addWidget(self.DirHeader)
        self.DirVS.addWidget(self.DirTree)
        self.DirVS.addWidget(self.DirListBtnFrame)

        # =========================================== 文件 ===========================================
        self.FileVS = self.VS()

        # 文件标题栏
        self.FileHeaderFrame = QFrame()
        self.FileHeaderFrame.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Header_Frame())
        self.FileHeaderFrame.setFixedHeight(20)

        self.FileHeaderLayout = QHBoxLayout()
        self.FileHeaderLayout.setContentsMargins(0, 0, 0, 0)  # 设置边距

        self.FileHeader = QLabel(self.Lang.FileList)
        self.FileHeader.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Top_Label())  # 设置样式
        self.FileHeader.setAlignment(Qt.AlignCenter)  # 字体居中

        self.FileHeaderList = FileListLabel("List")
        self.FileHeaderList.setScaledContents(True)  # 图片自适应
        self.FileHeaderList.setPixmap(self.SetIMG(FLIST))
        self.FileHeaderList.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Top_Label())  # 设置样式
        self.FileHeaderList.setAlignment(Qt.AlignCenter)  # 字体居中
        self.FileHeaderList.setFixedWidth(20)
        self.FileHeaderList.ActionSignal.connect(self.ShowFileListAction)  # 连接槽函数

        self.FileHeaderGrid = FileGridLabel("Grid")
        self.FileHeaderGrid.setScaledContents(True)  # 图片自适应
        self.FileHeaderGrid.setPixmap(self.SetIMG(FGRID))
        self.FileHeaderGrid.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Top_Label())  # 设置样式
        self.FileHeaderGrid.setAlignment(Qt.AlignCenter)  # 字体居中
        self.FileHeaderGrid.setFixedWidth(20)
        self.FileHeaderGrid.ActionSignal.connect(self.ShowFileGridAction)  # 连接槽函数

        self.FileHeaderLayout.addWidget(self.FileHeader)
        self.FileHeaderLayout.addWidget(self.FileHeaderList)
        self.FileHeaderLayout.addWidget(self.FileHeaderGrid)

        self.FileHeaderFrame.setLayout(self.FileHeaderLayout)
        self.FileVS.addWidget(self.FileHeaderFrame)

        self.FileFrame = QFrame()
        self.FileFrame.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Frame())
        self.FileLayout = QVBoxLayout()
        self.FileLayout.setContentsMargins(0, 0, 0, 0)

        self.FileTree = BaseTreeWidget()
        self.FileTree.SetSelectionMode(2)  # 设置多选模式
        self.FileTree.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Tree_Widget())  # 设置样式
        self.FileTree.HideVScroll()  # 隐藏纵向滚动条
        self.FileTree.HideHScroll()  # 隐藏横向滚动条
        self.FileTree.setColumnCount(3)  # 设置列数
        self.FileTree.hideColumn(1)  # 隐藏列
        self.FileTree.setHeaderLabels(["FILE", "ID", "CreateTime"])  # 设置标题栏
        self.FileTree.setHeaderHidden(True)  # 隐藏标题栏
        self.FileTree.setColumnWidth(0, 450)  # 设置列宽
        self.FileTree.setAcceptDrops(True)  # 设置接收拖动
        self.FileTree.setDragEnabled(True)  # 设置item可拖动
        # self.FileTree.DragDirSignal.connect(self.DoUploadDir)  # 获取被拖动的文件夹路径
        self.FileTree.itemDoubleClicked.connect(self.FOpen)  # 鼠标左键双击事件 在线打开文件

        self.GridSA = QScrollArea()
        # SA.setWidgetResizable(True)  # 自适应宽度
        # SA.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏竖向滚动条
        # SA.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏横向滚动条
        self.GridSA.setContentsMargins(0, 0, 0, 0)
        self.GridSA.setStyleSheet(self.Style.Object.BaseScrollArea())

        self.FileFrame.setLayout(self.FileLayout)
        self.FileVS.addWidget(self.FileFrame)

        # 文件列表下方按钮
        self.FileListBtnFrame = QFrame()
        self.FileListBtnFrame.setStyleSheet(self.Style.Object.MainFrame_Mid_File_List_Btn_Frame())
        self.FileListBtnFrame.setFixedHeight(30)
        self.FileListBtnFrame.setContentsMargins(0, 0, 0, 0)

        self.FileListBtnLayout = QHBoxLayout()
        self.FileListBtnLayout.setContentsMargins(0, 0, 0, 0)

        self.UploadFilesBtn = QPushButton(self.Lang.UploadFiles)
        self.UploadFilesBtn.setStyleSheet(self.Style.Object.MainFrame_Mid_File_List_Btn())
        self.UploadFilesBtn.setContentsMargins(1, 1, 1, 1)
        self.UploadFilesBtn.setFixedHeight(30)
        self.UploadFilesBtn.clicked.connect(self.DoUpload)

        self.UploadFolderBtn = QPushButton(self.Lang.UploadFolder)
        self.UploadFolderBtn.setStyleSheet(self.Style.Object.MainFrame_Mid_File_List_Btn())
        self.UploadFolderBtn.setContentsMargins(1, 1, 1, 1)
        self.UploadFolderBtn.setFixedHeight(30)
        self.UploadFolderBtn.clicked.connect(self.DoUploadDir)

        self.DownloadBtn = QPushButton(self.Lang.Download)
        self.DownloadBtn.setStyleSheet(self.Style.Object.MainFrame_Mid_File_List_Btn())
        self.DownloadBtn.setContentsMargins(1, 1, 1, 1)
        self.DownloadBtn.setFixedHeight(30)
        self.DownloadBtn.clicked.connect(self.DoDownload)

        self.RecycleBtn = QPushButton(self.Lang.RecycleBin)
        self.RecycleBtn.setStyleSheet(self.Style.Object.MainFrame_Mid_File_List_Btn())
        self.RecycleBtn.setContentsMargins(1, 1, 1, 1)
        self.RecycleBtn.setFixedHeight(30)
        self.RecycleBtn.clicked.connect(self.RecycleBin)

        self.FileListBtnLayout.addWidget(self.UploadFilesBtn)
        self.FileListBtnLayout.addWidget(self.UploadFolderBtn)
        self.FileListBtnLayout.addWidget(self.DownloadBtn)
        self.FileListBtnLayout.addWidget(self.RecycleBtn)
        self.FileListBtnFrame.setLayout(self.FileListBtnLayout)
        self.FileVS.addWidget(self.FileListBtnFrame)

        # ============================================================================================
        # 分割线
        self.MidRS = self.HS()
        self.MidRS.addWidget(self.DirVS)
        self.MidRS.addWidget(self.FileVS)
        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.MidRS)
        self.setLayout(MainLayout)

        # ============================================================================================

        self.ShowFileList()
        self.ShowFileGrid()
        self.FileHeader.setText(self.Lang.FileList)
        self.GridSA.hide()

        # ============================================================================================
        self.FileTimingSync()

    # 列表
    def ShowFileListAction(self):
        self.FileHeader.setText(self.Lang.FileList)
        self.FileTree.show()
        self.GridSA.hide()

    # 阵列
    def ShowFileGridAction(self):
        self.FileHeader.setText(self.Lang.FileGrid)
        self.GridSA.show()
        self.FileTree.hide()

    # 根目录文件列表
    def ShowRootFiles(self):
        self.FileHeader.setText(self.Lang.FileList)
        SelectDirData = DirFileAction().SelectDir()
        if SelectDirData["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        self.CurrentDirID = SelectDirData["ID"]
        self.ShowFileList()
        self.ShowFileGrid()

    # 文件列表
    def ShowFileList(self):
        self.RecycleBinState = False
        self.InsertFileTree(self.CurrentDirID)  # 获取当前文件夹下的文件列表

    # 写入文件树列表
    def InsertFileTree(self, DirID, State=2):
        Result = DirFileAction().FileList(DirID, State)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        Files = Result["Data"]
        self.FileTree.clear()
        FileTreeItems = []
        if len(Files) > 0:
            for i in range(len(Files)):
                item = QTreeWidgetItem()  # 设置item控件
                item.setText(0, Files[i]["FileName"])  # 设置内容
                item.setText(1, str(Files[i]["ID"]))  # 设置内容
                item.setText(2, self.Common.TimeToStr(Files[i]["Createtime"]))  # 设置内容
                item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                FileTreeItems.append(item)  # 添加到item list
            self.FileTree.insertTopLevelItems(0, FileTreeItems)  # 添加到文件夹列表
        # 鼠标右键 链接槽函数
        self.FileTree.Connect(self.FileRightContextMenuExec)
        self.FileLayout.addWidget(self.FileTree)

    # 获取被拖拽的items
    def CheckMoveTreeItems(self, DirID):
        if DirID == 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        Items = self.FileTree.selectedItems()
        for i in range(len(Items)):
            Name = Items[i].text(0)
            FileID = Items[i].text(1)
            Result = DirFileAction().MoveFile(FileID, DirID)
            if Result["State"] != True:
                MSGBOX().ERROR(Name + " " + self.Lang.OperationFailed)
                return
            self.DeleteFileItem(Items[i])

    # 文件网格
    def ShowFileGrid(self):
        self.RecycleBinState = False
        self.InsertFileGrid(self.CurrentDirID)

    # 写入文件阵列
    def InsertFileGrid(self, DirID, State=2):
        Result = DirFileAction().FileList(DirID, State)
        if Result["State"] != True:
            return
        Files = Result["Data"]

        GridFrame = QFrame()
        GridFrame.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Grid_Frame())
        GridItemLayout = QGridLayout()
        GridItemLayout.setContentsMargins(0, 0, 0, 0)
        # GridItemLayout.setHorizontalSpacing(0)
        # GridItemLayout.setVerticalSpacing(0)
        # GridItemLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.ClearLayout(GridItemLayout)

        FileCount = len(Files)
        if FileCount > 0:
            for i in range(len(Files)):
                Col = 8
                Row = int(FileCount / Col)
                Row_ = FileCount % Col
                if Row_ > 0:
                    Row += Row + 1
                FileArr = []
                for i in range(len(Files)):
                    FileArr.append({"Name": Files[i]["FileName"], "ID": Files[i]["ID"]})
                Positions = [(i, j) for i in range(Row) for j in range(Col)]  # 创建位置列表 n行5列
                for Position, File in zip(Positions, FileArr):
                    FileLabel = FileGridItemLabel()
                    FileLabel.setText(FileLabel.FM.elidedText(File["Name"], Qt.ElideRight, 150))  # 省略过长的内容
                    FileLabel.setAlignment(Qt.AlignTop)  # 从头显示文本
                    FileLabel.setWordWrap(True)  # 自动换行
                    FileLabel.setToolTip(File["Name"])
                    FileLabel.ActionSignal.connect(self.FOpenAction)
                    FileLabel.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Grid_Item())
                    FileLabel.setWhatsThis(str(File["ID"]))
                    FileLabel.setFixedWidth(150)
                    FileLabel.setFixedHeight(60)
                    GridItemLayout.addWidget(FileLabel, *Position)
        GridFrame.setLayout(GridItemLayout)
        self.GridSA.setWidget(GridFrame)
        self.FileLayout.addWidget(self.GridSA)

    # ============================================================================================

    # 新建顶级文件夹
    def CreateTopDirWindow(self):
        self.CreateTopDirWindowObject = CreateTopDirWindow()
        self.CreateTopDirWindowObject.ActionSignal.connect(self.CreateTopDirAction)
        self.CreateTopDirWindowObject.show()

    # 新建顶级文件夹方法
    def CreateTopDirAction(self, DirName, DirID):
        Item = QTreeWidgetItem()  # 设置item控件
        Item.setText(0, DirName)  # 设置内容
        Item.setText(1, str(DirID))
        Item.setText(2, str(self.CurrentDirID))
        Item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        Item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        Item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
        self.DirTree.insertTopLevelItem(0, Item)

    # 打开下载文件夹
    def OpenDownloadDirWindow(self):
        self.File.OpenLocalDir(self.Cache.Get("UserTempDir"))

    # 文件定时同步
    def FileTimingSync(self):
        self.FileTimingSyncWorker = FileTimingSyncWorker()
        self.FileTimingSyncWorker.ActionSignal.connect(self.DoFileSync)
        self.FileTimingSyncWorker.FinishSignal.connect(self.KillThread(self.FileSyncThread))
        self.FileTimingSyncWorker.moveToThread(self.FileSyncThread)
        self.FileSyncThread.started.connect(self.FileTimingSyncWorker.Run)
        self.FileSyncThread.start()

    # 文件同步
    def FileSync(self):  # 文件同步
        if self.Cache.Get("Sync") == True:
            MSGBOX().CUE(self.Lang.FileSyncing)
            return
        self.DoFileSync()
        MSGBOX().COMPLETE(self.Lang.Complete)

    # 文件同步操作
    def DoFileSync(self):
        if self.Cache.Get("Sync") == True:
            return
        FilesCache = self.TCache.Select()
        if len(FilesCache) > 0:
            self.Cache.Set("Sync", True)  # 开启上传状态
            TempDir = self.Cache.Get("TempDir")  # 获取临时文件夹
            for K, V in FilesCache.items():
                _K = self.Common.Explode("_", K)
                ID = _K[0]
                MD5 = _K[1]
                FileEntityPath = TempDir + V
                NewMD5 = self.File.CheckFileMD5(FileEntityPath)  # 获取文件当前MD5信息
                if MD5 != NewMD5:  # 文件有改动则上传
                    # 同步前置操作
                    Result1 = DirFileAction().FileEntitySyncPrefix(ID)
                    if Result1["State"] != True:
                        DirFileAction().FileEntitySyncFail(ID)
                        break

                    FileInfo = DirFileAction().CheckFile(ID)["Data"]

                    FileName = FileInfo["FileName"]
                    State = FileInfo["State"]
                    FileSize = self.File.CheckFileSize(FileEntityPath)
                    BlockSize = FileInfo["BlockSize"]  # 总分片数
                    UploadBlockSize = FileInfo["UploadBlockSize"]  # 已上传的分片数
                    DirID = FileInfo["DirID"]
                    FileMD5 = FileInfo["MD5"]
                    Createtime = FileInfo["Createtime"]

                    # 新建临时存储路径
                    FileTempDir = TempDir + FileName + "." + str(Createtime)
                    try:
                        self.File.MkDir(FileTempDir)
                    except Exception as e:
                        break

                    # 文件切片
                    SliceState, SliceNum = self.File.CutFile(FileEntityPath, FileTempDir, FILESLICESIZE)
                    if SliceState != True:
                        break

                    # 上传切片
                    if SliceNum > 0:
                        # 获取切片文件
                        _, FileSlice = self.File.SelectDir(FileTempDir)
                        for i in range(len(FileSlice)):
                            Result2 = DirFileAction().FileEntitySync(ID, FileSlice[i], FileTempDir + "/" + FileSlice[i])
                            if Result2["State"] != True:
                                DirFileAction().FileEntitySyncFail(ID)
                                self.Cache.Set("Sync", False)
                                return

                    # 同步后置操作
                    Result3 = DirFileAction().FileEntitySyncDefer(ID)
                    if Result3["State"] != True:
                        DirFileAction().FileEntitySyncFail(ID)
                        break

                    Result4 = DirFileAction().ModifyFile(ID, FileName, State, FileSize, len(FileSlice), UploadBlockSize, DirID, NewMD5)
                    if Result4["State"] != True:
                        break

            self.Cache.Set("Sync", False)

    # 单击文件夹
    def DirItemClicked(self):
        self.FileHeader.setText(self.Lang.FileList)
        CurrentDirItem = self.DirTree.currentItem()  # 获取当前item对象

        # 获取目录ID
        DirID = int(CurrentDirItem.text(1))
        self.CurrentDirID = DirID

        # 清除子节点 防止重复
        i = 0
        while i < CurrentDirItem.childCount():
            CurrentDirItem.removeChild(CurrentDirItem.child(i))

        # 获取子文件夹和文件
        Result = DirFileAction().SelectDir(DirID)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        # 设置公共文件夹数据
        SubDirList = Result["Data"]

        SubDirItemList = []  # 设置子文件夹数组
        if len(SubDirList) > 0:
            for i in range(len(SubDirList)):
                Item = QTreeWidgetItem()  # 设置item控件
                Item.setText(0, SubDirList[i]["DirName"])  # 设置内容
                Item.setText(1, str(SubDirList[i]["ID"]))  # 设置内容
                Item.setText(2, str(SubDirList[i]["ParentID"]))  # 设置内容
                Item.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                Item.setTextAlignment(1, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                Item.setTextAlignment(2, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
                SubDirItemList.append(Item)  # 添加到item list
                CurrentDirItem.addChildren(SubDirItemList)  # 添加到文件夹列表

        self.ShowFileList()
        self.ShowFileGrid()

    # 文件夹右键
    def DirRightContextMenuExec(self, pos):
        self.DirTreeMenu = BaseMenu()  # 左侧文件夹列表鼠标右键菜单
        self.DirTreeMenu.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_File_Tree_Menu())  # 设置样式
        Item = self.DirTree.currentItem()  # 获取被点击行控件
        ItemAt = self.DirTree.itemAt(pos)  # 获取点击焦点

        # 展示判断
        if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
            self.DirTreeMenu.AddAction(self.Lang.Rename, lambda: self.DirRenameWindow(Item))  # 重命名
            self.DirTreeMenu.AddAction(self.Lang.AddSubFolder, lambda: self.CreateSubDirWindow(Item))  # 创建子文件夹
            self.DirTreeMenu.AddAction(self.Lang.Delete, lambda: self.DelDir(self.DirTree, Item))  # 删除文件夹
            if self.Cache.Get("PasteFilesID") is not None:
                self.DirTreeMenu.AddAction(self.Lang.PasteFiles, lambda: self.PasteFiles(Item))  # 粘贴文件
        else:  # 焦点外
            return

        self.DirTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.DirTreeMenu.show()  # 展示

    # 重命名文件夹
    def DirRenameWindow(self, Item):
        self.DirRenameWindowObject = DirRenameWindow(Item)
        self.DirRenameWindowObject.show()

    # 添加子文件夹
    def CreateSubDirWindow(self, Item):
        self.CreateSubDirWindowObject = CreateSubDirWindow(Item)
        self.CreateSubDirWindowObject.show()

    # 删除文件夹
    def DelDir(self, DirTree, Item):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            ID = Item.text(1)
            Result = DirFileAction().DeleteDir(ID)
            if Result["State"] == True:
                DirTree.RemoveItems(Item)
                MSGBOX().COMPLETE(self.Lang.Complete)
            else:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return

    # 粘贴文件
    def PasteFiles(self, Item):
        FilesIDStr = self.Cache.Get("PasteFilesID")
        FilesID = self.Common.Explode(",", FilesIDStr)
        DirID = Item.text(1)
        self.PasteFileWorker = PasteFileWorker(DirID, FilesID)
        self.PasteFileWorker.ErrorSignal.connect(self.ShowError)
        self.PasteFileWorker.FinishSignal.connect(self.Cache.Delete("PasteFilesID"))
        self.PasteFileWorker.FinishSignal.connect(self.KillThread(self.PasteFileThread))
        self.PasteFileWorker.moveToThread(self.PasteFileThread)
        self.PasteFileThread.started.connect(self.PasteFileWorker.Run)
        self.PasteFileThread.start()

    # 文件右键
    def FileRightContextMenuExec(self, pos):
        self.FileTreeMenu = BaseMenu()  # 左侧文件夹列表鼠标右键菜单
        self.FileTreeMenu.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_File_Tree_Menu())  # 设置样式
        Item = self.FileTree.currentItem()  # 获取被点击行控件
        ItemAt = self.FileTree.itemAt(pos)  # 获取点击焦点

        if self.RecycleBinState == True:
            if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
                self.FileTreeMenu.AddAction(self.Lang.MoveToTheRootFolder, lambda: self.MoveToTheRootFolder())  # 移动到根目录
            else:
                self.FileTreeMenu.AddAction(self.Lang.EmptyTheRecycleBin, lambda: self.EmptyTheRecycleBin())  # 清空
        else:
            # 展示判断
            if type(Item) == QTreeWidgetItem and type(ItemAt) == QTreeWidgetItem:  # 焦点内
                self.FileTreeMenu.AddAction(self.Lang.FileDetails, lambda: self.FileInfoWindow(Item))  # 重命名
                self.FileTreeMenu.AddAction(self.Lang.CopyFiles, lambda: self.CopyFiles())  # 复制
                self.FileTreeMenu.AddAction(self.Lang.MoveToRecycleBin, lambda: self.MoveToRecycleBin())  # 移动到回收站
                self.FileTreeMenu.AddAction(self.Lang.Delete, lambda: self.DelFiles())  # 删除文件
                self.FileTreeMenu.AddAction(self.Lang.FileSharing, lambda: self.FileSharing())  # 分享给其他用户
                self.FileTreeMenu.AddAction(self.Lang.ShareFilesToDepartment, lambda: self.ShareFilesToDepartment())  # 发送到部门
                self.FileTreeMenu.AddAction(self.Lang.FavoritesToFilesTag, lambda: self.FavoritesToFilesTag())  # 收藏到文件标签
            else:  # 焦点外
                self.FileTreeMenu.AddAction(self.Lang.Refresh, lambda: self.Refresh())  # 刷新列表

        self.FileTreeMenu.move(QtGui.QCursor().pos())  # 移动到焦点
        self.FileTreeMenu.show()  # 展示

    # 移动到根目录
    def MoveToTheRootFolder(self):
        Files = self.FileTree.selectedItems()
        if len(Files) > 0:
            self.PromptPopUpsAction(self.Lang.PleaseWait)
            # 获取用户根文件夹信息
            SelectDirData = DirFileAction().SelectDir()
            if SelectDirData["State"] != True:
                MSGBOX().ERROR(self.Lang.OperationFailed)
                return
            RootDirID = SelectDirData["CurrentDirID"]
            for i in range(len(Files)):
                self.DeleteFileItem(Files[i])
                ID = Files[i].text(1)
                FileName = Files[i].text(0)
                Result1 = DirFileAction().CheckFile(ID)
                if Result1["State"] != True:
                    MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                    break
                FileInfo = Result1["Data"]
                State = 2
                FileSize = FileInfo["FileSize"]
                BlockSize = FileInfo["BlockSize"]
                UploadBlockSize = FileInfo["UploadBlockSize"]
                DirID = RootDirID
                FileMD5 = FileInfo["MD5"]
                Result2 = DirFileAction().ModifyFile(ID, FileName, State, FileSize, BlockSize, UploadBlockSize, DirID, FileMD5)
                if Result2["State"] != True:
                    MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                    break

    # 清空回收站
    def EmptyTheRecycleBin(self):
        Files = self.FileTree.SelectItems()
        if len(Files) > 0:
            YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
            if YesOrNo == QtWidgets.QMessageBox.Yes:
                for i in range(len(Files)):
                    self.DeleteFileItem(Files[i])
                    Name = Files[i].text(0)
                    ID = Files[i].text(1)
                    Result = DirFileAction().DeleteFile(ID)
                    if Result["State"] != True:
                        MSGBOX().ERROR(Name + " " + self.Lang.OperationFailed)
                        break

    # 文件详情
    def FileInfoWindow(self, Item):
        ID = Item.text(1)
        self.FileInfoWindowObject = FileInfoWindow(ID)
        self.FileInfoWindowObject.ActionSignal.connect(self.ShowFileList)
        self.FileInfoWindowObject.show()

    # 文件分享
    def FileSharing(self):
        Files = self.FileTree.selectedItems()
        self.FileSharingWindow = FileSharingWindow(Files)
        self.FileSharingWindow.show()

    # 分享文件到部门
    def ShareFilesToDepartment(self):
        Files = self.FileTree.selectedItems()
        if len(Files) > 0:
            for i in range(len(Files)):
                ID = Files[i].text(1)
                FileName = Files[i].text(0)
                Result = UserAction().ShareFilesToDepartment(ID)
                if Result["State"] != True:
                    if Result["Memo"] == "Data is exists":
                        MSGBOX().WARNING(FileName + " " + self.Lang.AlreadyInTheList)
                    else:
                        MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                    return
            MSGBOX().COMPLETE(self.Lang.Complete)

    # 收藏到文件标签
    def FavoritesToFilesTag(self):
        Files = self.FileTree.selectedItems()
        self.TagListWindow = TagListWindow(Files)
        self.TagListWindow.show()

    # 复制文件
    def CopyFiles(self):
        Files = self.FileTree.selectedItems()
        IDList = []
        if len(Files) > 0:
            for i in range(len(Files)):
                IDList.append(Files[i].text(1))
            FilesID = self.Common.Implode(",", IDList)
            self.Cache.Set("PasteFilesID", FilesID)

    # 移动到回收站
    def MoveToRecycleBin(self):
        Files = self.FileTree.selectedItems()
        if len(Files) > 0:
            self.PromptPopUpsAction(self.Lang.PleaseWait)
            for i in range(len(Files)):
                self.DeleteFileItem(Files[i])
                Name = Files[i].text(0)
                ID = Files[i].text(1)
                FileData = DirFileAction().CheckFile(ID)
                if FileData["State"] != True:
                    MSGBOX.ERROR(Name + " " + self.Lang.OperationFailed)
                    break
                FileInfo = FileData["Data"]
                FileName = FileInfo["FileName"]
                State = 4
                FileSize = FileInfo["FileSize"]
                BlockSize = FileInfo["BlockSize"]
                UploadBlockSize = FileInfo["UploadBlockSize"]
                DirID = 0
                FileMD5 = FileInfo["MD5"]
                Result = DirFileAction().ModifyFile(ID, FileName, State, FileSize, BlockSize, UploadBlockSize, DirID, FileMD5)
                if Result["State"] != True:
                    MSGBOX.ERROR(Name + " " + self.Lang.OperationFailed)
                    return
                else:
                    self.RefreshFileTagListSignal.emit()

    # 文件网格详情
    def FileGridInfo(self, ID):
        pass

    # 删除文件
    def DelFiles(self):
        YesOrNo = MSGBOX().ASK(self.Lang.Confirm)
        if YesOrNo == QtWidgets.QMessageBox.Yes:
            Files = self.FileTree.selectedItems()
            if len(Files) > 0:
                self.PromptPopUpsAction(self.Lang.PleaseWait)
                for i in range(len(Files)):
                    self.DeleteFileItem(Files[i])
                    Name = Files[i].text(0)
                    ID = Files[i].text(1)
                    Result = DirFileAction().DeleteFile(ID)
                    if Result["State"] != True:
                        MSGBOX().ERROR(Name + " " + self.Lang.OperationFailed)
                        return
                    else:
                        self.RefreshFileTagListSignal.emit()

    # 刷新文件列表
    def Refresh(self):
        self.ShowFileList()
        self.ShowFileGrid()

    # 选择文件上传
    def DoUpload(self):
        Files, _ = QFileDialog.getOpenFileNames(self)  # 文件选择框
        if len(Files) == 0:
            return
        self.UploadSignal.emit(Files, self.CurrentDirID)
        self.PromptPopUpsAction(self.Lang.AddedToUploadTaskList)

    # 获取拖拽文件夹路径
    # def DoUploadDir(self, DirPath=""):
    #     if DirPath == "":
    #         return
    #     Files = self.File.SelectDirFiles(DirPath)
    #     if len(Files) == 0:
    #         return
    #     FilesArr = []
    #     for i in range(len(Files)):
    #         FileName = self.File.CheckFileName(Files[i])
    #         FileType = self.File.CheckFileType(Files[i])
    #         if FileName.lower() + "." + FileType.lower() != "desktop":
    #             FilesArr.append(Files[i])
    #     self.UploadSignal.emit(FilesArr, self.CurrentDirID)

    # 选择文件夹上传
    def DoUploadDir(self):
        FolderPath = QFileDialog.getExistingDirectoryUrl(self).toDisplayString().replace("file:///", "")  # 文件夹选择框
        if FolderPath != "":
            Files = self.File.SelectDirFiles(FolderPath)
            if len(Files) > 0:
                for i in range(len(Files)):
                    Files[i] = FolderPath + "/" + Files[i]
                self.UploadSignal.emit(Files, self.CurrentDirID)
                self.PromptPopUpsAction(self.Lang.AddedToUploadTaskList)

    # 下载文件
    def DoDownload(self):
        Files = self.FileTree.selectedItems()
        if (len(Files) > 0):
            FileIDList = []
            for i in range(len(Files)):
                FileInfo = {}
                FileInfo["FileName"] = Files[i].text(0)
                FileInfo["ID"] = Files[i].text(1)
                FileIDList.append(FileInfo)
            self.DownloadSignal.emit(FileIDList)
            self.PromptPopUpsAction(self.Lang.AddedToDownloadTaskList)

    # 回收站
    def RecycleBin(self):
        self.RecycleBinState = True
        self.FileHeader.setText(self.Lang.RecycleBin)
        self.InsertFileTree(0, 4)
        self.InsertFileGrid(0, 4)

    # 删除文件Item
    def DeleteFileItem(self, Item):
        self.FileTree.RemoveItems(Item)

    # 错误提示
    def ShowError(self, Content):
        MSGBOX().ERROR(Content)

    # 在线编辑预览(tree)
    def FOpen(self):
        Item = self.FileTree.currentItem()
        FileName = Item.text(0)
        FileID = Item.text(1)
        self.FOpenAction(FileName, FileID)

    # 在线编辑预览公共方法
    def FOpenAction(self, FileName, FileID):
        if self.RecycleBinState == True:
            return

        # 文件详情
        Result1 = DirFileAction().CheckFile(FileID)
        if Result1["State"] != True:
            MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
            return
        FileInfo = Result1["Data"]
        if FileInfo["State"] != 2:
            MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
            return

        FileMD5 = FileInfo["MD5"]

        if self.TCache.Get(FileID + "_" + FileMD5) is not None:
            self.File.FileNativeCall(self.Cache.Get("TempDir") + FileName + "." + FileInfo["FileType"])  # 打开文件
            return

        # 是否超出预览大小限制
        Result2 = ConfigAction().CheckConfig(3)
        if Result2["State"] != True:
            CheckPreviewSizeLimit = PREVIEWSIZELIMIT
        else:
            CheckPreviewSizeLimit = Result2["Data"]["ConfigValue"]

        if int(FileInfo["FileSize"]) > int(CheckPreviewSizeLimit):
            MSGBOX().ERROR(FileName + " " + self.Lang.PreviewSizeLimitExceeded + "(" + self.File.FileSizeFormat(int(CheckPreviewSizeLimit)) + ")")
            return

        # 锁定文件
        Result3 = DirFileAction().FileLockSwitch(FileID)
        if Result3["State"] != True:
            MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
            return

        # 缓存文件
        FileTempDirPath = self.Cache.Get("TempDir") + FileName  # 缓存路径
        if self.File.DirIsExist(FileTempDirPath):
            self.File.DirRemoveAll(FileTempDirPath)

        # 建立文件缓存目录
        try:
            self.File.MkDir(FileTempDirPath)
        except Exception as e:
            DirFileAction().FileLockSwitch(FileID)
            MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
            return

        # 读取文件分片
        BlockSize = FileInfo["BlockSize"]
        for i in range(BlockSize):
            Result = DirFileAction().DownloadFileEntity(FileID, i + 1)
            if Result["State"] != True:
                DirFileAction().FileLockSwitch(FileID)
                MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                return
            FileEntityName = Result["Data"]["FileEntityName"]
            FilePart = FileTempDirPath + "/" + FileEntityName
            try:
                self.File.MkFile(FilePart)
            except Exception as e:
                DirFileAction().FileLockSwitch(FileID)
                MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                return

            # 内容转换
            Content = self.Common.Base64ToBytes(self.Common.StringToBytes(Result["Data"]["Data"]))

            # 写入分片数据
            try:
                self.File.WFileInByte(FilePart, Content)
            except Exception as e:
                DirFileAction().FileLockSwitch(FileID)
                MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                return

        # 删除相同文件
        NewFile = self.Cache.Get("TempDir") + FileName + \
            "." + FileInfo["FileType"]
        if self.File.FileIsExist(NewFile) == True:
            try:
                self.File.DeleteFile(NewFile)
            except Exception as e:
                DirFileAction().FileLockSwitch(FileID)
                MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)

        try:
            # 文件合并
            if self.File.MergeFile(FileTempDirPath, self.Cache.Get("TempDir"), FileName + "." + FileInfo["FileType"]) == False:
                DirFileAction().FileLockSwitch(FileID)
                MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                return
        except Exception as e:
            DirFileAction().FileLockSwitch(FileID)
            MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
            return

        # 删除临时目录
        self.File.DirRemoveAll(FileTempDirPath)

        # 打开文件
        self.File.FileNativeCall(self.Cache.Get("TempDir") + FileName + "." + FileInfo["FileType"])

        # 记录打开的文件并保存MD5
        self.TCache.Set(FileID + "_" + FileMD5, FileName + "." + FileInfo["FileType"])

        # 解锁文件
        DirFileAction().FileLockSwitch(FileID)

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


class RootDirectoryLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


class FileListLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


class FileGridLabel(QLabel):
    ActionSignal = Signal()  # 设置信号

    def __init__(self, Text):
        super().__init__()
        self.setText(Text)

    # 重构鼠标事件
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit()  # 发送信号


class FileGridItemLabel(QLabel):
    ActionSignal = Signal(str, str)  # 设置信号

    def __init__(self, Text=""):
        super().__init__()
        self.FM = self.fontMetrics()
        self.setText(Text)

    # 重构鼠标双击事件
    def mouseDoubleClickEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 鼠标左键
            self.ActionSignal.emit(self.text(), str(self.whatsThis()))  # 发送信号

    # def mousePressEvent(self, event):
    #     if event.buttons() == Qt.LeftButton:  # 鼠标左键
    #         self.ActionSignal.emit()  # 发送信号


class CreateTopDirWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal(str, int)  # 设置信号

    def __init__(self):
        super().__init__()

        self.AppMode()
        self.setFixedSize(200, 80)
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.DirNameInput = QLineEdit()
        self.DirNameInput.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.DirNameInput.setFixedHeight(30)
        self.DirNameInput.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Win_Input())

        self.Btn = QPushButton(self.Lang.Submit)
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Win_Btn())
        self.Btn.clicked.connect(self.CreateAction)

        self.VLayout.addWidget(self.DirNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def CreateAction(self):
        if self.DirNameInput.text() == "":
            MSGBOX().ERROR(self.Lang.WrongFolderName)
            return
        Result = DirFileAction().CreateDir(self.DirNameInput.text(), 0)
        if Result["State"] == True:
            self.ActionSignal.emit(self.DirNameInput.text(), Result["ID"])
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return


class DirRenameWindow(BaseInterface, BaseDialog):

    def __init__(self, Item):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.Item = Item
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.DirNameInput = QLineEdit()
        self.DirNameInput.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.DirNameInput.setFixedHeight(30)
        self.DirNameInput.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Win_Input())
        self.DirNameInput.setText(self.Item.text(0))

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Win_Btn())
        self.Btn.clicked.connect(self.DoRename)

        self.VLayout.addWidget(self.DirNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def DoRename(self):
        ID = self.Item.text(1)
        DirName = self.DirNameInput.text()
        ParentID = self.Item.text(2)
        if DirName == self.Item.text(0):
            return
        elif DirName == "":
            MSGBOX().ERROR(self.Lang.WrongFolderName)
            return
        else:
            Result = DirFileAction().ModifyDir(ID, DirName, ParentID)
            if Result["State"] == True:
                self.Item.setText(0, DirName)
                self.close()
                MSGBOX().COMPLETE(self.Lang.Complete)
            else:
                MSGBOX().ERROR(self.Lang.OperationFailed)


class CreateSubDirWindow(BaseInterface, BaseDialog):

    def __init__(self, Item):
        super().__init__()
        self.AppMode()
        self.setFixedSize(200, 80)
        self.Item = Item
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.DirNameInput = QLineEdit()
        self.DirNameInput.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.DirNameInput.setFixedHeight(30)
        self.DirNameInput.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Win_Input())

        self.Btn = QPushButton("OK")
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_Dir_Win_Btn())
        self.Btn.clicked.connect(self.DoCreateSubDirAction)

        self.VLayout.addWidget(self.DirNameInput)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    def DoCreateSubDirAction(self):
        DirName = self.DirNameInput.text()
        ParentID = self.Item.text(1)
        Result = DirFileAction().CreateDir(DirName, ParentID)
        if DirName == "":
            MSGBOX().ERROR(self.Lang.WrongFolderName)
            return
        if Result["State"] == True:
            node = QTreeWidgetItem(self.Item)  # 设置Item控件
            node.setTextAlignment(0, Qt.AlignHCenter | Qt.AlignVCenter)  # 设置item字体居中
            node.setText(0, DirName)  # 写入文件名
            node.setText(1, str(Result["ID"]))  # 写入文件ID
            node.setText(2, str(ParentID))  # 写入文件上级ID
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)
        else:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return


class FileInfoWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()

    def __init__(self, ID):
        super().__init__()
        self.AppMode()
        if ID == 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        Result = DirFileAction().CheckFile(ID)
        if Result["State"] == False:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        self.FileInfo = Result["Data"]

        self.setFixedSize(300, 180)
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.FileNameInput = QLineEdit()
        self.FileNameInput.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.FileNameInput.setFixedHeight(30)
        self.FileNameInput.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Info_Win_Input())
        self.FileNameInput.setText(self.FileInfo["FileName"])
        self.FileNameInput.setToolTip(self.Lang.FileName)

        self.FileSizeInput = QLineEdit()
        self.FileSizeInput.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.FileSizeInput.setEnabled(False)  # 禁止输入
        self.FileSizeInput.setFixedHeight(30)
        self.FileSizeInput.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Info_Win_Input())
        self.FileSizeInput.setText(self.File.FileSizeFormat(self.FileInfo["FileSize"]))
        self.FileSizeInput.setToolTip(self.Lang.FileSize)

        self.FileTypeInput = QLineEdit()
        self.FileTypeInput.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.FileTypeInput.setEnabled(False)  # 禁止输入
        self.FileTypeInput.setFixedHeight(30)
        self.FileTypeInput.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Info_Win_Input())
        self.FileTypeInput.setText(self.FileInfo["FileType"])
        self.FileTypeInput.setToolTip(self.Lang.FileType)

        self.FileMD5Input = QLineEdit()
        self.FileMD5Input.setAlignment(Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.FileMD5Input.setEnabled(False)  # 禁止输入
        self.FileMD5Input.setFixedHeight(30)
        self.FileMD5Input.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Info_Win_Input())
        self.FileMD5Input.setText(self.FileInfo["MD5"])
        self.FileMD5Input.setToolTip("MD5")

        self.Btn = QPushButton(self.Lang.Submit)
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Info_Win_Btn())
        self.Btn.clicked.connect(self.Rename)

        self.VLayout.addWidget(self.FileNameInput)
        self.VLayout.addWidget(self.FileSizeInput)
        self.VLayout.addWidget(self.FileTypeInput)
        self.VLayout.addWidget(self.FileMD5Input)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)

    # 重命名
    def Rename(self):
        FileName = self.FileNameInput.text()
        State = self.FileInfo["State"]
        FileSize = self.FileInfo["FileSize"]
        BlockSize = self.FileInfo["BlockSize"]
        UploadBlockSize = self.FileInfo["UploadBlockSize"]
        DirID = self.FileInfo["DirID"]
        FileMD5 = self.FileInfo["MD5"]
        Result = DirFileAction().ModifyFile(self.FileInfo["ID"], FileName, State, FileSize, BlockSize, UploadBlockSize, DirID, FileMD5)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.OperationFailed)
        else:
            self.close()
            MSGBOX().COMPLETE(self.Lang.Complete)
            self.ActionSignal.emit()


class FileSharingWindow(BaseInterface, BaseDialog):

    def __init__(self, FilesItem):
        super().__init__()
        self.AppMode()

        self.FilesItem = FilesItem
        if len(self.FilesItem) <= 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        Result = UserAction().SelectUser(-1)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return
        self.UserList = Result["Data"]
        if len(self.UserList) <= 0:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
            return

        self.setFixedSize(300, 200)
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.HLayout = QHBoxLayout()

        self.SearchBar = QLineEdit()
        self.SearchBar.setFixedHeight(30)
        self.SearchBar.setPlaceholderText(self.Lang.Name)
        # self.SearchBar.setAlignment(
        #     Qt.AlignCenter | Qt.AlignBottom | Qt.AlignHCenter)  # 内容居中
        self.SearchBar.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Sharing_Win_Input())

        self.Btn1 = QPushButton(self.Lang.SearchName)
        self.Btn1.setFixedWidth(100)
        self.Btn1.setFixedHeight(30)
        self.Btn1.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Sharing_Win_Btn())
        self.Btn1.clicked.connect(self.SearchName)

        self.UserTree = QListWidget()
        # self.UserTree.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置多选
        self.UserTree.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Sharing_Win_List())
        self.UserTree.setFocusPolicy(Qt.NoFocus)

        self.Btn2 = QPushButton(self.Lang.Send)
        self.Btn2.setFixedHeight(30)
        self.Btn2.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Sharing_Win_Btn())
        self.Btn2.clicked.connect(self.Send)

        self.HLayout.addWidget(self.SearchBar)
        self.HLayout.addWidget(self.Btn1)
        self.VLayout.addLayout(self.HLayout)
        self.VLayout.addWidget(self.UserTree)
        self.VLayout.addWidget(self.Btn2)
        self.setLayout(self.VLayout)

        self.AddItemAction()

    # 加入数据
    def AddItemAction(self):
        for i in range(len(self.UserList)):
            if self.UserList[i]["Account"] != self.Cache.Get("Account"):
                Item = QListWidgetItem()
                Item.setSizeHint(QtCore.QSize(200, 30))
                Item.setText(self.UserList[i]["Name"])
                Item.setWhatsThis(str(self.UserList[i]["ID"]))
                self.UserTree.addItem(Item)

    # 搜索人员
    def SearchName(self):
        Name = self.SearchBar.text()
        if Name == "":
            self.AddItemAction()
        else:
            SearchList = self.UserTree.findItems(Name, Qt.MatchContains)
            if len(SearchList) > 0:
                for i in range(len(SearchList)):
                    if SearchList[i].text() != self.Cache.Get("Account"):
                        self.UserTree.setCurrentItem(SearchList[i])

    # 发送文件
    def Send(self):
        User = self.UserTree.currentItem()
        if User is None:
            return
        UserID = User.whatsThis()
        if len(self.FilesItem) > 0:
            for i in range(len(self.FilesItem)):
                FileName = self.FilesItem[i].text(0)
                FileID = self.FilesItem[i].text(1)
                Result = DirFileAction().SendFileToUser(FileID, UserID)
                if Result["State"] != True:
                    MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                    return
            MSGBOX().COMPLETE(self.Lang.Complete)


class TagListWindow(BaseInterface, BaseDialog):

    def __init__(self, Items):
        super().__init__()
        self.AppMode()
        self.Items = Items
        if len(self.Items) <= 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        SelectTagData = DirFileAction().TagList()
        self.TagList = SelectTagData["Data"]
        if len(self.TagList) <= 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return

        self.setFixedSize(300, 260)
        self.VLayout = QVBoxLayout()
        self.VLayout.setContentsMargins(5, 5, 5, 5)

        self.TagListTree = QListWidget()
        # self.UserTree.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 设置多选
        self.TagListTree.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Tag_Win_List())
        self.TagListTree.setFocusPolicy(Qt.NoFocus)

        self.Btn = QPushButton(self.Lang.Submit)
        self.Btn.setFixedHeight(30)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_File_Tag_Win_Btn())
        self.Btn.clicked.connect(self.Send)

        self.VLayout.addWidget(self.TagListTree)
        self.VLayout.addWidget(self.Btn)
        self.setLayout(self.VLayout)
        self.AddItemAction()

    def AddItemAction(self):
        for i in range(len(self.TagList)):
            Item = QListWidgetItem()
            Item.setSizeHint(QtCore.QSize(200, 30))
            Item.setText(self.TagList[i]["TagName"])
            Item.setWhatsThis(str(self.TagList[i]["ID"]))
            Item.setToolTip(self.TagList[i]["TagMemo"])
            self.TagListTree.addItem(Item)

    def Send(self):
        Tag = self.TagListTree.currentItem()
        if Tag is None:
            return
        TagID = Tag.whatsThis()
        if (len(self.Items) > 0) and (int(TagID) > 0):
            for i in range(len(self.Items)):
                FileName = self.Items[i].text(0)
                FileID = self.Items[i].text(1)
                Result = DirFileAction().CreateFileTag(TagID, FileID)
                if Result["State"] != True:
                    MSGBOX().ERROR(FileName + " " + self.Lang.OperationFailed)
                    return
            MSGBOX().COMPLETE(self.Lang.Complete)


class PasteFileWorker(BaseInterface, BaseObject):
    ErrorSignal = Signal(str)

    def __init__(self, DirID, FilesID):
        super().__init__()
        self.DirID = DirID
        self.FilesID = FilesID

    def Run(self):
        if len(self.FilesID) > 0:
            for i in range(len(self.FilesID)):
                Result1 = DirFileAction().CheckFile(self.FilesID[i])
                if Result1["State"] != True:
                    self.ErrorSignal.emit(self.Lang.OperationFailed)
                    break
                FileInfo = Result1["Data"]
                Result2 = DirFileAction().CopyFile(self.DirID, self.FilesID[i])
                if Result2["State"] != True:
                    self.ErrorSignal.emit(FileInfo["FileName"] + " " + self.Lang.OperationFailed)
                    break
            self.FinishSignal.emit()


class FileTimingSyncWorker(BaseInterface, BaseObject):
    ActionSignal = Signal()

    def __init__(self):
        super().__init__()

    def Run(self):
        while True:
            sleep(self.Cache.Get("SynchronizationCycle"))
            self.ActionSignal.emit()
