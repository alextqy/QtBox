# -*- coding:utf-8 -*-
from style._base import *


class DefaultQSS(BaseStyle):
    def __init__(self):
        super().__init__()

    # ======================================================= 公共 =======================================================

    def BaseDialog(self):
        return """
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        """

    def MSGQDialog(self):
        return """
        QDialog {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        """

    def MSGLabel(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            color: black;
            background-color: #e2e4db;
        }
        """

    def MSGBTNLabel(self):
        return """
        QLabel{
            font-family: Microsoft Yahei;
            color: black;
            border-style: solid;
        }
        """

    def BaseScrollArea(self):
        return """
        QScrollBar::handle{
            border-width: 0px;
        }

        QScrollBar:vertical{
            background-color: #b2b5ba;
        }
        QScrollBar::add-line:vertical{
            width: 0px;
        }
        QScrollBar::sub-line:vertical{
            width: 0px;
        }

        QScrollBar:horizontal{
            background-color: #b2b5ba;
        }
        QScrollBar::add-line:horizontal{
            width: 0px;
        }
        QScrollBar::sub-line:horizontal{
            width: 0px;
        }
        """

    def VS_Style(self):
        return """
        QSplitter::handle {
            background-color: #e2e4db;
            border: 0px solid black;
        }
        """

    def HS_Style(self):
        return """
        QSplitter::handle {
            background-color: #b2b5ba;
            border-width: 0px;
            margin: 5px;
        }
        """

    def MainWindow(self):
        return """
        QMainWindow {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
        }
        """

    def MainWindow_Login_Top_Logo(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
        }
        """

    def MainWindow_Login_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            margin: 0px;
            border: 0px;
            padding: 10px;
            background-color: #b2b5ba;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainWindow_Login_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #3f83ab;
            border-width: 0px;
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
        """

    def MainFrame_Lang_Box(self):
        return """
        QComboBox {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border: 3px solid #b2b5ba;
            /*border-width: 0px;*/
            border-radius: 5px;
        }
        /*
        QListView::item:hover{
            color: white;
            background: #9AB9F6;
        }
        */
        QListView{
            border: 3px solid #b2b5ba;
        }
        QListView::item:selected{
            color: white;
            background: #b2b5ba;
        }
        QComboBox QAbstractItemView {
            color: black;
            font-family: Microsoft Yahei;
            background: #e2e4db;
        }
        /* 去掉下拉右侧的箭头 */
        QComboBox::drop-down {
            font-family: Microsoft Yahei;
            border: 0px;
        }
        """

    def MainFrame_PromptPopUps_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
        }
        """

    def Upload_Tree(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 5px;
        }

        QHeaderView::section {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            padding-left: 10px;
            border: 1px solid #b2b5ba;
            margin-right: 3px;
        }

        QTreeWidget::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            margin-top: 3px;
            margin-right: 3px;
            height: 30px;
            border: 1px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border: 1px solid #9AB9F6;
            background-color: #9AB9F6;
            color: white;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border: 1px solid #9AB9F6;
            background-color: #9AB9F6;
            color: black;
        }
        """

    def Download_Tree(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 5px;
        }

        QHeaderView::section {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            padding-left: 10px;
            border: 1px solid #b2b5ba;
            margin-right: 3px;
        }

        QTreeWidget::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            margin-top: 3px;
            margin-right: 3px;
            height: 30px;
            border: 1px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border: 1px solid #9AB9F6;
            background-color: #9AB9F6;
            color: white;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border: 1px solid #9AB9F6;
            background-color: #9AB9F6;
            color: black;
        }
        """

    def Upload_Tree_Menu(self):
        return """
        QMenu {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            padding: 0px;
        }

        QMenu::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            padding: 5px 15px;
            /*设置菜单项的外边距*/
            /* margin: 1px 0px; */
            /* width: 100px; */
            border-width: 0px;
        }

        QMenu::item:selected {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: white;
            border-width: 0px;
        }

        QMenu::item:pressed {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-width: 0px;
        }
        """

    def Download_Tree_Menu(self):
        return """
        QMenu {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            padding: 0px;
        }

        QMenu::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            padding: 5px 15px;
            /*设置菜单项的外边距*/
            /* margin: 1px 0px; */
            /* width: 100px; */
            border-width: 0px;
        }

        QMenu::item:selected {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: white;
            border-width: 0px;
        }

        QMenu::item:pressed {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-width: 0px;
        }
        """

    def Bar(self):
        return """
        QProgressBar {
            font-family: Microsoft Yahei;
            text-align: center;
            color: black;
            background-color: #e2e4db;
            border-width: 0px;
        }
        
        QProgressBar::chunk {
            background-color: #8ecd91;
        }
        """

    # ======================================================= 主体 =======================================================

    def MainFrame_Top_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #36ABF1;
            color: black;
            border-radius: 5px;
            qproperty-alignment: AlignHCenter;
            padding: 5px;
        }
        QLabel:hover {
            color: white;
        }
        """

    def MainFrame_Top_Task_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 5px;
            border: 1px solid #b2b5ba;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 10px;
            padding-right: 10px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_Frame_L(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            border-radius: 0px;
            border-color: #b2b5ba;
            border-style: solid;
            border-width: 1px;
            background-color: #393f4d;
        }
        """

    def MainFrame_Mid_Frame_R(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            border-radius: 0px;
            border-color: #b2b5ba;
            border-style: solid;
            border-width: 0px;
            background-color: #e2e4db;
        }
        """

    def MainFrame_Mid_Banner_Btn(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-radius: 5px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
        }
        """

    def MainFrame_Btm_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #b2b5ba;
            color: black;
            border-radius: 5px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
        }
        """

    def MainFrame_CheckMyself_Avatar_Label(self):
        return """
        QLabel{
            font-family: Microsoft Yahei;
            color: black;
        }
        """

    def MainFrame_CheckMyself_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_CheckMyself_Label(self):
        return """
        QLabel{
            background-color: white;
            border-radius: 5px;
            border: 3px solid #b2b5ba;
        }
        """

    def MainFrame_CheckMyself_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #36ABF1;
            color: black;
            border-radius: 5px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Activation_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #f3051d;
            border-width: 0px;
        }
        QPushButton:hover {
            color: black;
            background-color: #41cd52;
        }
        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Activation_Btn_Pro(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #41cd52;
            border-width: 0px;
        }
        QPushButton:hover {
            color: black;
            background-color: #41cd52;
        }
        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Activation_Window_Input(self):
        return """
        QTextEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QTextEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Activation_Window_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #3f83ab;
            border-width: 0px;
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
        """

    def MainFrame_Feedback_Window_Input(self):
        return """
        QTextEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QTextEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Feedback_Window_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #3f83ab;
            border-width: 0px;
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
        """

    def MainFrame_Exit_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            color: white;
            border-radius: 5px;
            background-color: #3f83ab;
            border-width: 0px;
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
        """

    def MainFrame_AboutUS_Window_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            border: 1px solid #b2b5ba;
            border-radius: 5px;
        }
        """

    # ======================================================= 文件夹 文件 =======================================================

    def MainFrame_Mid_Dir_Header(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_Dir_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: #F1DB36;
            height: 45px;
            border-radius: 5px;
            color: black;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_Dir_List_Btn_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_Dir_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_Dir_Win_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_Dir_Win_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-radius: 5px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_File_Header_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
        }
        """

    def MainFrame_Mid_File_Top_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            qproperty-alignment: AlignHCenter;
            border-width: 0px;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_File_Frame(self):
        return """
        border-width: 0px;
        """

    def MainFrame_Mid_File_List_Btn_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_File_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_File_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: #ffe660;
            height: 30px;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_File_Grid_Item(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            background-color: #ffe660;
            color: black;
            qproperty-alignment: AlignHCenter;
            border: 2px solid #b2b5ba;
            padding: 10px;
        }
        QLabel:hover {
            color: black;
            background-color: #e2e4db;
            border: 2px solid #b2b5ba;
        }
        """

    def MainFrame_Mid_File_Grid_Frame(self):
        return """
        font-family: Microsoft Yahei;
        border-radius: 5px;
        background-color: #e2e4db;
        """

    def MainFrame_Mid_File_Info_Win_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_File_Info_Win_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-radius: 5px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_File_Sharing_Win_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_File_Sharing_Win_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-radius: 5px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_File_Sharing_Win_List(self):
        return """
        QListWidget {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            background-color: #e2e4db;
        }

        QListWidget::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: #e2e4db;
            height: 30px;
            color: black;
        }

        QListWidget::item:hover {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
        }

        QListWidget::item:selected {
            font-family: Microsoft Yahei;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_Dir_File_Tree_Menu(self):
        return """
        QMenu {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            padding: 0px;
        }

        QMenu::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            padding: 5px 15px;
            /*设置菜单项的外边距*/
            /* margin: 1px 0px; */
            /* width: 100px; */
            border-width: 0px;
        }

        QMenu::item:selected {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: white;
            border-width: 0px;
        }

        QMenu::item:pressed {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-width: 0px;
        }
        """

    # ======================================================= 文件标签 =======================================================

    def MainFrame_Mid_Tag_Header(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_Tag_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            height: 45px;
            border-radius: 5px;
            color: black;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_Tag_List_Btn_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_Tag_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    # ======================================================= 用户 =======================================================

    def MainFrame_Mid_User_Header(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_User_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            height: 30px;
            border-radius: 5px;
            color: black;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_User_Message_List(self):
        return """
        QListWidget {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            background-color: #e2e4db;
        }
        QListWidget::item {
            padding-right: 10px;
            padding-left: 10px;
        }
        """

    def MainFrame_Mid_User_Message_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_User_Conversation_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_User_Conversation_Label(self):
        return """
        font-family: Microsoft Yahei;
        background-color: #e2e4db;
        """

    def MainFrame_Mid_User_Message_Conversation_Received(self):
        return """
        QTextEdit {
            font-family: Microsoft Yahei;
            background-color: #9de04d;
            border-radius: 10px;
            border: 2px solid #b2b5ba;
        }
        """

    def MainFrame_Mid_User_Message_Conversation_Sent(self):
        return """
        QTextEdit {
            font-family: Microsoft Yahei;
            background-color: #faffbd;
            border-radius: 10px;
            border: 2px solid #b2b5ba;
        }
        """

    def MainFrame_Mid_User_List_Btn_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_User_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_User_Info_Win_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_User_Info_Win_Box(self):
        return """
        QComboBox {
            font-family: Microsoft Yahei;
            background-color: white;
            color: black;
            border: 1px solid #b2b5ba;
            /*border-width: 0px;*/
            border-radius: 5px;
        }
        /*
        QListView::item:hover{
            color: white;
            background: #9AB9F6;
        }
        */
        QListView{
            border: 1px solid #b2b5ba;
        }
        QListView::item:selected{
            color: white;
            background: #b2b5ba;
        }
        QComboBox QAbstractItemView {
            color: black;
            font-family: Microsoft Yahei;
            background: white;
        }
        /* 去掉下拉右侧的箭头 */
        QComboBox::drop-down {
            font-family: Microsoft Yahei;
            border: 0px;
        }
        """

    def MainFrame_Mid_User_Info_Win_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-radius: 5px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_Message_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_Message_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_Message_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            padding-top: 5px;
            padding-bottom: 5px;
            padding-left: 10px;
            padding-right: 10px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_User_Tree_Menu(self):
        return """
        QMenu {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            padding: 0px;
        }

        QMenu::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            padding: 5px 15px;
            /*设置菜单项的外边距*/
            /* margin: 1px 0px; */
            /* width: 100px; */
            border-width: 0px;
        }

        QMenu::item:selected {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: white;
            border-width: 0px;
        }

        QMenu::item:pressed {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-width: 0px;
        }
        """

    # ======================================================= 部门 =======================================================

    def MainFrame_Mid_Department_Header(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_Department_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            height: 45px;
            border-radius: 5px;
            color: black;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_Department_List_Btn_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_Department_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_Department_Win_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_Department_Win_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-radius: 5px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_Staff_Header_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
        }
        """

    def MainFrame_Mid_Staff_Top_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            qproperty-alignment: AlignHCenter;
            border-width: 0px;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_Staff_Frame(self):
        return """
        border-width: 0px;
        """

    def MainFrame_Mid_Staff_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            height: 30px;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_Staff_List_Btn_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 0px;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_Staff_List_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """

    def MainFrame_Mid_Department_Staff_Tree_Menu(self):
        return """
        QMenu {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            padding: 0px;
        }

        QMenu::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            padding: 5px 15px;
            /*设置菜单项的外边距*/
            /* margin: 1px 0px; */
            /* width: 100px; */
            border-width: 0px;
        }

        QMenu::item:selected {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: white;
            border-width: 0px;
        }

        QMenu::item:pressed {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-width: 0px;
        }
        """

    # ======================================================= 我的部门 =======================================================

    def MainFrame_Mid_My_Department_User_Header(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_My_Department_User_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            height: 30px;
            border-radius: 5px;
            color: black;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_My_Department_File_Header(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
            border-bottom-width: 2px;
            qproperty-alignment: AlignHCenter;
        }
        QLabel:hover {
            color: white;
            background-color: #9AB9F6;
        }
        """

    def MainFrame_Mid_My_Department_File_Tree_Widget(self):
        return """
        QTreeWidget {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QTreeWidget::item {
            margin-right: 3px;
            margin-left: 3px;
            margin-top: 5px;
            font-family: Microsoft Yahei;
            color: black;
            background-color: #ffe660;
            height: 30px;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
        }

        QTreeWidget::item:hover {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #b2b5ba;
            background-color: #e2e4db;
            color: black;
        }

        QTreeWidget::item:selected {
            font-family: Microsoft Yahei;
            border-radius: 5px;
            border: 2px solid #e2e4db;
            background-color: #b2b5ba;
            color: white;
        }
        """

    def MainFrame_Mid_My_Department_User_Tree_Menu(self):
        return """
        QMenu {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            padding: 0px;
        }

        QMenu::item {
            font-family: Microsoft Yahei;
            color: black;
            background-color: white;
            /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            padding: 5px 15px;
            /*设置菜单项的外边距*/
            /* margin: 1px 0px; */
            /* width: 100px; */
            border-width: 0px;
        }

        QMenu::item:selected {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: white;
            border-width: 0px;
        }

        QMenu::item:pressed {
            font-family: Microsoft Yahei;
            background-color: #9AB9F6;
            color: black;
            border-width: 0px;
        }
        """

    # ======================================================= 设置 =======================================================

    def MainFrame_Mid_SysConf_Frame(self):
        return """
        QFrame {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            border-radius: 5px;
            border: 1px solid #b2b5ba;
            padding: 10px;
        }
        """

    def MainFrame_Mid_SysConf_Label(self):
        return """
        QLabel {
            font-family: Microsoft Yahei;
            color: black;
            background-color: #e2e4db;
            border-width: 0px;
        }
        """

    def MainFrame_Mid_SysConf_Input(self):
        return """
        QLineEdit {
            font-family: Microsoft Yahei;
            color: black;
            border-radius: 5px;
            margin: 0px;
            border: 1px solid #b2b5ba;
            padding: 5px;
            background-color: white;
        }
        QLineEdit:hover {
            background-color: #faffbd;
            color: black;
        }
        """

    def MainFrame_Mid_SysConf_Btn(self):
        return """
        QPushButton {
            font-family: Microsoft Yahei;
            background-color: #e2e4db;
            color: black;
            border-radius: 0px;
            border-width: 0px;
        }

        QPushButton:hover {
            background-color: #9AB9F6;
            color: white;
        }

        QPushButton:pressed {
            color: black;
            background-color: #faffbd;
            padding-left: 3px;
            padding-top: 3px;
        }
        """
