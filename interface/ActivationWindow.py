# -*- coding:utf-8 -*-
from interface._base import *


class ActivationWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()

    def __init__(self):
        super().__init__()
        self.AppMode()
        self.setFixedSize(400, 300)

        Layout = QVBoxLayout()
        Layout.setContentsMargins(5, 5, 5, 5)

        self.Input1 = QTextEdit()
        self.Input1.setReadOnly(True)
        self.Input1.setStyleSheet(
            self.Style.Object.MainFrame_Activation_Window_Input())
        self.Input1.setPlaceholderText(
            self.Lang.GenerateSignatureVerificationCode)
        Layout.addWidget(self.Input1)

        self.Btn1 = QPushButton(
            "  " + self.Lang.GenerateSignatureVerificationCode)  # 验签码按钮
        self.Btn1.setFixedHeight(30)  # 设置固定高度
        self.Btn1.setStyleSheet(
            self.Style.Object.MainFrame_Activation_Window_Btn())
        self.Btn1.clicked.connect(self.GenerateSecretKey)  # 连接槽函数
        self.Btn1.setIcon(QIcon(GCODE))
        Layout.addWidget(self.Btn1)

        self.Input2 = QTextEdit()
        self.Input2.setStyleSheet(
            self.Style.Object.MainFrame_Activation_Window_Input())
        self.Input2.setPlaceholderText(self.Lang.InputActivationCode)
        Layout.addWidget(self.Input2)

        self.Btn2 = QPushButton("  " + self.Lang.InputActivationCode)  # 激活按钮
        self.Btn2.setFixedHeight(30)  # 设置固定高度
        self.Btn2.setStyleSheet(
            self.Style.Object.MainFrame_Activation_Window_Btn())
        self.Btn2.clicked.connect(self.CheckActivationCode)  # 连接槽函数
        self.Btn2.setIcon(QIcon(ACODE))
        Layout.addWidget(self.Btn2)

        self.setLayout(Layout)

    # 生成验签码
    def GenerateSecretKey(self):
        Result = ConfigAction().GetHardwareCode()
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        HardwareCode = Result["Data"]
        self.Input1.setText(HardwareCode)

    # 验证激活码
    def CheckActivationCode(self):
        ActivationCode = self.Input2.toPlainText()
        Result = ConfigAction().ProductActivation(ActivationCode)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.ActivationFails)
        else:
            self.ActionSignal.emit()
            self.close()
            MSGBOX().COMPLETE(
                self.Lang.ActivatedSuccessfully + " " + self.Lang.MaxAccounts + " " + str(Result["ID"]))
