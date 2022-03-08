# -*- coding:utf-8 -*-
from interface._library import *
from public.zead import *
from style.zead import *
from controller.zead import *
from abc import ABCMeta, abstractmethod


class BaseInterface():  # 基础操作类

    def __init__(self, StyleType="default"):
        super().__init__()
        self.SW, self.SH = Tk().maxsize()  # 获取显示器的宽高

        self.Cache = Cache()  # 实例化公共缓存
        self.Common = Common()  # 公共方法
        self.File = File()  # 文件操作方法
        self.Lang = Lang()  # 语言包
        self.UDPTool = UDPTool()  # UDP
        self.Style = MainQSS(StyleType)  # 样式库

    def CheckWidgetPos(self, WidgetObject):  # 获取控件坐标
        PosList = []
        PosList.append(WidgetObject.geometry().x())
        PosList.append(WidgetObject.geometry().y())
        return PosList

    def ClearLayout(self, layout):  # 清理布局
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.ClearLayout(item.layout())

    def VS(self):  # 可拖动垂直控件
        VS = QSplitter(Qt.Vertical)
        VS.setStyleSheet(self.Style.Object.VS_Style())  # 设置分割线样式
        return VS

    def HS(self):  # 可拖动水平控件
        HS = QSplitter(Qt.Horizontal)
        HS.setStyleSheet(self.Style.Object.HS_Style())  # 设置分割线样式
        return HS

    def KillThread(self, ThreadObject):  # 退出线程
        ThreadObject.quit()
        ThreadObject.wait()

    def Quit(self):  # 退出系统
        if self.Cache.Get("Sync") == True:  # 是否有文件正在同步
            MSGBOX().WARNING(self.Lang.FileSyncing)
        else:
            if self.Cache.Get("Token") != "":
                UserAction().SignOut()
            self.CleanUpAction()
            os._exit(0)

    def CleanUpAction(self):  # 清理操作
        self.Cache.Set("Debug", False)
        self.Cache.Set("Token", "")
        self.Cache.Set("UserUploadPath", "")
        self.Cache.Set("UserDownloadPath", "")
        self.Cache.Set("UserTempDir", "")
        self.Cache.Set("TempDir", "")
        self.Cache.Set("Sync", False)
        if self.Cache.Get("PasteFilesID") is not None:
            self.Cache.Delete("PasteFilesID")

    def CleanUpDeferAction(self):  # 登录后的清理操作
        TempDir = self.Cache.Get("TempDir")
        # 清理缓存目录
        self.File.DirRemoveAll(TempDir)
        self.File.MkDir(TempDir)
        # 解锁已经锁定的文件数据
        Result = DirFileAction().FileLockList()
        if Result["State"] == True:
            Files = Result["Data"]
            if len(Files) > 0:
                for i in range(len(Files)):
                    ID = Files[i]["ID"]
                    DirFileAction().FileLockSwitch(ID)

    def SetWindowPalette(self, QtColorParam):  # 设置窗口背景颜色
        PaletteObject = QPalette()
        return PaletteObject.setColor(QPalette.Window, QtGui.QColor(QtColorParam))

    def SetButtonPalette(self, QtColorParam):  # 设置按钮背景颜色
        PaletteObject = QPalette()
        return PaletteObject.setColor(QPalette.Button, QtGui.QColor(QtColorParam))

    def SetIMG(self, IMGPath):  # 设置图片
        return QPixmap(IMGPath)


class BaseObject(QObject):  # 多线程基础对象
    FinishSignal = Signal()

    def __init__(self):
        super().__init__()


class BaseMainWindow(QMainWindow):  # 基础主窗口

    def __init__(self, Title=TITLE):
        super().__init__()
        self.setWindowTitle(Title)  # 窗口标题
        self.setWindowIcon(QtGui.QIcon(ICON))  # 设置ICON

    def HideTitleBar(self):  # 隐藏窗口标题栏
        self.setWindowFlags(Qt.FramelessWindowHint)

    def ShowMinMaxBtnOnly(self):  # 仅显示最小化最大化按钮
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)

    def ShowCloseBtnOnly(self):  # 仅显示关闭按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def closeEvent(self, event):
        self.Quit()
        # event.accept()
        # event.ignore()


class BaseFrame(QFrame):  # 基础结构窗

    def __init__(self):
        super().__init__()


class BaseDialog(QDialog):  # 交互窗口

    def __init__(self, Title=TITLE):
        super().__init__()
        self.setWindowTitle(Title)  # 窗口标题
        self.setWindowIcon(QtGui.QIcon(ICON))  # 设置ICON
        self.setWindowFlags(Qt.WindowCloseButtonHint)  # 关闭标题栏问号按钮

    def HideHeader(self):
        self.setWindowFlags(Qt.FramelessWindowHint)

    def NoneMode(self):  # Qt.NonModal:非模态,可以和程序的其他窗口进行交互
        self.setWindowModality(Qt.NonModal)

    def WindowMode(self):  # Qt.WindowModal:窗口模态,程序在未处理玩当前对话框时,将阻止和对话框的父窗口进行交互
        self.setWindowModality(Qt.WindowModal)

    def AppMode(self):  # Qt.ApplicationModal:应用程序模态,阻止和任何其他窗口进行交互
        self.setWindowModality(Qt.ApplicationModal)

    def Top(self):  # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)


class BaseTreeWidget(QTreeWidget):  # 基础树形控件
    MoveSignal = Signal(int)
    DragDirSignal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setRootIsDecorated(False)  # 隐藏左侧展开标志

        # 开启槽函数
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def SetSelectionMode(self, No=0):  # 设置多选模式
        if No == 1:  # 多选(不需按ctrl)
            self.setSelectionMode(QAbstractItemView.MultiSelection)
        elif No == 2:  # 按住ctrl一次选一项或者按住shift可多选
            self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        elif No == 3:  # 一次选择多项
            self.setSelectionMode(QAbstractItemView.ContiguousSelection)
        elif No == 4:  # 无法选择
            self.setSelectionMode(QAbstractItemView.NoSelection)
        else:  # 单选
            self.setSelectionMode(QAbstractItemView.SingleSelection)

    def Connect(self, Func):  # 链接槽函数
        self.customContextMenuRequested.connect(Func)

    def RemoveTopItem(self, Item):  # 删除根节点
        self.takeTopLevelItem(self.indexOfTopLevelItem(Item))

    def RemoveSubItem(self, Item):  # 删除子节点
        ParentNode = Item.parent()  # 获取父级item
        ParentNode.removeChild(Item)  # 删除下级

    def RemoveItems(self, Item):  # 删除节点
        if type(Item.parent()) == QtWidgets.QTreeWidgetItem:  # 如果为子节点
            self.RemoveSubItem(Item)
        else:
            self.RemoveTopItem(Item)

    def SelectItems(self):  # 获取所有item
        ItemsObj = QTreeWidgetItemIterator(self)
        List = []
        i = 0
        while ItemsObj.value():  # 遍历出item对象
            List.append(i)
            List[i] = ItemsObj.value()
            ItemsObj.__iadd__(1)
            i = i + 1
        return List

    def HideHScroll(self):  # 隐藏横向滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def HideVScroll(self):  # 隐藏纵向滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def dropEvent(self, event):  # 重写释放事件
        if event.source() == self:  # 拖动的控件是否来自外部
            # event.setDropAction(Qt.MoveAction)  # 移除当前方法
            # super().dropEvent(event)  # 调用父级同名方法
            return
        else:
            Item = self.itemAt(event.pos())  # 获取当前释放时的坐标
            if Item != None:
                ID = Item.text(1)  # 获取内容
                self.MoveSignal.emit(int(ID))

    # 判断拖拽动作 以防控件显示异常
    def dragEnterEvent(self, e):
        e.accept()

    # def dragEnterEvent(self, event):  # 拖拽文件夹
    #     if event.source() == self:  # 拖动的控件是否来自外部
    #         event.setDropAction(Qt.MoveAction)  # 移除当前方法
    #         super().dragEnterEvent(event)  # 调用父级同名方法
    #     else:
    #         DirPath = event.mimeData().text().replace("file:///", "")
    #         if self.File.DirIsExist(DirPath):
    #             self.DragDirSignal.emit(DirPath)
    #         else:
    #             self.dropEvent(event)


class BaseMenu(QMenu):  # 基础菜单控件

    def __init__(self):
        super().__init__()

    def AddAction(self, Title, Func):
        self.addAction(Title).triggered.connect(Func)


class MSGBOX(BaseInterface, QMessageBox):  # 自定义问询窗口

    def __init__(self):
        super().__init__()
        self.Cache = Cache()  # 设置缓存
        self.Title = "NULL"
        if self.Cache.Get("Title") != "":
            self.Title = self.Cache.Get("Title")  # 设置标题
        self.setWindowIcon(QtGui.QIcon(ICON))  # 设置ICON

    def ERROR(self, Content):
        self.setStyleSheet('''
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #ef5f5d;
            height: 25px;
            width: 50px;
        }
        QPushButton:hover {
            color: black;
            background-color: #ef5f5d;
        }
        QPushButton:pressed {
            color: black;
            background-color: #ef5f5d;
            padding-left: 3px;
            padding-top: 3px;
        }
        ''')
        return self.critical(self, self.Title, Content)

    def WARNING(self, Content):
        self.setStyleSheet('''
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #f6ca0d;
            height: 25px;
            width: 50px;
        }
        QPushButton:hover {
            color: black;
            background-color: #f6ca0d;
        }
        QPushButton:pressed {
            color: black;
            background-color: #f6ca0d;
            padding-left: 3px;
            padding-top: 3px;
        }
        ''')
        return self.warning(self, self.Title, Content)

    def COMPLETE(self, Content):
        self.setStyleSheet('''
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #9eca75;
            height: 25px;
            width: 50px;
        }
        QPushButton:hover {
            color: black;
            background-color: #9eca75;
        }
        QPushButton:pressed {
            color: black;
            background-color: #9eca75;
            padding-left: 3px;
            padding-top: 3px;
        }
        ''')
        return self.about(self, self.Title, Content)

    def CUE(self, Content):
        self.setStyleSheet('''
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #3f83ab;
            height: 25px;
            width: 50px;
        }
        QPushButton:hover {
            color: black;
            background-color: #2787cc;
        }
        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        ''')
        return self.information(self, self.Title, Content)

    def ASK(self, Content):
        self.setStyleSheet('''
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #3f83ab;
            height: 25px;
            width: 50px;
        }
        QPushButton:hover {
            color: black;
            background-color: #2787cc;
        }
        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        ''')
        return self.question(self, self.Title, Content)


class PromptPopUpsWindow(BaseInterface, BaseDialog):  # 静态公共提示弹窗

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.Top()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(280, 100)

        self.Layout = QVBoxLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.Label = QLabel()
        self.Label.setAlignment(Qt.AlignCenter)
        self.Label.setStyleSheet(self.Style.Object.MainFrame_PromptPopUps_Label())

        self.Layout.addWidget(self.Label)
        self.setLayout(self.Layout)


class TooltipWindow(BaseInterface, BaseDialog):  # 动态公共提示弹窗

    def __init__(self):
        super().__init__()
        self.NoneMode()
        self.Top()
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        self.setFixedSize(280, 100)

        self.Layout = QVBoxLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)

        self.Label = QLabel()
        self.Label.setAlignment(Qt.AlignCenter)
        self.Label.setStyleSheet(self.Style.Object.MainFrame_PromptPopUps_Label())

        self.Layout.addWidget(self.Label)
        self.setLayout(self.Layout)


class CalendarWindow(BaseInterface, BaseDialog):

    def __init__(self):
        super().__init__()
        # self.AppMode()
        self.setFixedSize(450, 300)
        self.Layout = QVBoxLayout()
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.CalendarLayout = QHBoxLayout()
        self.CalendarLayout.setContentsMargins(0, 0, 0, 0)
        self.BtnLayout = QHBoxLayout()
        self.BtnLayout.setContentsMargins(0, 0, 0, 0)
        self.CalendarWidget = QCalendarWidget()
        self.CalendarLayout.addWidget(self.CalendarWidget)
        self.Btn = QPushButton(self.Lang.Confirm)
        self.Btn.setStyleSheet(self.Style.Object.MainFrame_Mid_Message_List_Btn())
        self.Btn.setFixedHeight(30)
        self.Btn.clicked.connect(self.CalendarAction)
        self.BtnLayout.addWidget(self.Btn)
        self.Layout.addLayout(self.CalendarLayout)
        self.Layout.addLayout(self.BtnLayout)
        self.setLayout(self.Layout)
        self.show()

    @abstractmethod
    def CalendarAction(self):
        # DateStr = self.CalendarWidget.selectedDate().toString("yyyy-MM-dd 00:00:00")
        pass


class PromptPopUpsWorker(BaseInterface, BaseObject):
    ActionSignal = Signal()
    HideSignal = Signal()

    def __init__(self):
        super().__init__()

    def Run(self):
        self.ActionSignal.emit()
        sleep(3)
        self.HideSignal.emit()
