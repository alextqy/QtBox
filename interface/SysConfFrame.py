# -*- coding:utf-8 -*-
from interface._base import *


class SysConfFrame(BaseInterface, BaseFrame):
    def __init__(self):
        super().__init__()

        # =========================================== Ready ===========================================

        Result = ConfigAction().CheckConfig(1)
        if Result["State"] != True:
            return

        self.FileType = Result["Data"]

        self.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Frame())
        self.SysConfLayout = QVBoxLayout()
        self.SysConfLayout.setContentsMargins(0, 0, 0, 0)

        self.FileTypeH1 = QHBoxLayout()

        self.FileTypeLabel = QLabel(self.Lang.UploadTypesSupported + " :")
        self.FileTypeLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.FileTypeLabel.setAlignment(Qt.AlignCenter)  # 字体居中

        self.FileTypeInput = QLineEdit()
        # self.FileTypeInput.setInputMask("<")
        self.FileTypeInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Input())
        self.FileTypeInput.setPlaceholderText(self.Lang.FileType)
        self.FileTypeInput.setText(self.FileType["ConfigValue"])

        self.FileTypeBtn = QPushButton(self.Lang.Submit)
        self.FileTypeBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Btn())
        self.FileTypeBtn.setFixedHeight(30)
        self.FileTypeBtn.setFixedWidth(80)
        self.FileTypeBtn.clicked.connect(self.FileTypeModifyAction)

        self.FileTypeCueLabel = QLabel(
            self.Lang.Tips + " : " + self.Lang.DifferentFileTypesSeparatedByCommas)
        self.FileTypeCueLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.FileTypeCueLabel.setAlignment(Qt.AlignRight)  # 字体居中

        self.FileTypeH1.addWidget(self.FileTypeLabel)
        self.FileTypeH1.addWidget(self.FileTypeInput)
        self.FileTypeH1.addWidget(self.FileTypeBtn)

        self.SysConfLayout.addLayout(self.FileTypeH1)
        self.SysConfLayout.addWidget(self.FileTypeCueLabel)

        # ============================================================================================

        self.FileTypeH2 = QHBoxLayout()

        self.FileSyncCycleLabel = QLabel(self.Lang.FileSyncFrequency + " :")
        self.FileSyncCycleLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.FileSyncCycleLabel.setAlignment(Qt.AlignCenter)  # 字体居中

        self.FileSyncCycleInput = QLineEdit()
        self.FileSyncCycleInput.setFixedWidth(80)
        self.FileSyncCycleInput.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Input())
        self.FileSyncCycleInput.setPlaceholderText(self.Lang.FileSyncFrequency)
        self.FileSyncCycleInput.setText(
            str(self.Cache.Get("SynchronizationCycle")))

        self.FileSyncCycleBtn = QPushButton(self.Lang.Submit)
        self.FileSyncCycleBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Btn())
        self.FileSyncCycleBtn.setFixedHeight(30)
        self.FileSyncCycleBtn.setFixedWidth(80)
        self.FileSyncCycleBtn.clicked.connect(self.SetSynchronizationCycle)

        self.FileSyncCycleCueLabel = QLabel(
            self.Lang.Tips + " : " + self.Lang.FileSyncCycleCue)
        self.FileSyncCycleCueLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.FileSyncCycleCueLabel.setAlignment(Qt.AlignRight)  # 字体居中

        self.FileTypeH2.addWidget(self.FileSyncCycleLabel)
        self.FileTypeH2.addWidget(self.FileSyncCycleInput)
        self.FileTypeH2.addStretch()
        self.FileTypeH2.addWidget(self.FileSyncCycleBtn)

        self.SysConfLayout.addLayout(self.FileTypeH2)
        self.SysConfLayout.addWidget(self.FileSyncCycleCueLabel)

        # ============================================================================================

        self.FileTypeH3 = QHBoxLayout()

        self.ServerDiskSpaceInformationLabel = QLabel(
            self.Lang.ServerDiskSpaceInformation + " :")
        self.ServerDiskSpaceInformationLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.ServerDiskSpaceInformationLabel.setAlignment(
            Qt.AlignCenter)  # 字体居中

        # 总空间
        self.DiskSpaceLabel = QLabel("Disk space")
        self.DiskSpaceLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.DiskSpaceLabel.setAlignment(
            Qt.AlignCenter)  # 字体居中
        self.ServerDiskSpaceInformationInput1 = QLineEdit()
        self.ServerDiskSpaceInformationInput1.setFixedWidth(150)
        self.ServerDiskSpaceInformationInput1.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Input())
        self.ServerDiskSpaceInformationInput1.setEnabled(False)

        # 剩余空间
        self.FreeDiskSpaceLabel = QLabel("Free disk space")
        self.FreeDiskSpaceLabel.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Label())
        self.FreeDiskSpaceLabel.setAlignment(
            Qt.AlignCenter)  # 字体居中
        self.ServerDiskSpaceInformationInput2 = QLineEdit()
        self.ServerDiskSpaceInformationInput2.setFixedWidth(150)
        self.ServerDiskSpaceInformationInput2.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Input())
        self.ServerDiskSpaceInformationInput2.setEnabled(False)

        self.ServerDiskSpaceInformationBtn = QPushButton(self.Lang.Submit)
        self.ServerDiskSpaceInformationBtn.setStyleSheet(
            self.Style.Object.MainFrame_Mid_SysConf_Btn())
        self.ServerDiskSpaceInformationBtn.setFixedHeight(30)
        self.ServerDiskSpaceInformationBtn.setFixedWidth(80)
        self.ServerDiskSpaceInformationBtn.clicked.connect(
            self.GetHardDiskSpaceInfo)

        self.FileTypeH3.addWidget(self.ServerDiskSpaceInformationLabel)
        self.FileTypeH3.addWidget(self.DiskSpaceLabel)
        self.FileTypeH3.addWidget(self.ServerDiskSpaceInformationInput1)
        self.FileTypeH3.addWidget(self.FreeDiskSpaceLabel)
        self.FileTypeH3.addWidget(self.ServerDiskSpaceInformationInput2)
        self.FileTypeH3.addStretch()
        self.FileTypeH3.addWidget(self.ServerDiskSpaceInformationBtn)

        self.SysConfLayout.addLayout(self.FileTypeH3)

        # ============================================================================================

        self.SysConfLayout.addStretch()
        self.setLayout(self.SysConfLayout)

    def FileTypeModifyAction(self):
        ConfigKey = self.FileType["ConfigKey"]
        ConfigDesc = self.FileType["ConfigDesc"]
        ConfigType = self.FileType["ConfigType"]
        ConfigValue = self.FileTypeInput.text()
        if ConfigValue == "":
            MSGBOX().ERROR(self.Lang.WrongInput)
            return
        ConfigValue = ConfigValue.lower()
        Result = ConfigAction().ModifyConfig(
            1, ConfigKey, ConfigDesc, ConfigType, ConfigValue)
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        else:
            MSGBOX().COMPLETE(self.Lang.Complete)

    def SetSynchronizationCycle(self):
        Data = int(self.FileSyncCycleInput.text())
        if Data <= 0:
            MSGBOX().ERROR(self.Lang.OperationFailed)
            return
        if Data >= 10:
            Data = 10
        self.Cache.Set("SynchronizationCycle", Data)
        self.FileSyncCycleInput.setText(
            str(self.Cache.Get("SynchronizationCycle")))

    def GetHardDiskSpaceInfo(self):
        Result = ConfigAction().GetHardDiskSpaceInfo()
        if Result["State"] != True:
            MSGBOX().ERROR(self.Lang.RequestWasAborted)
        else:
            Data = self.Common.Explode("_", Result["Data"])
            self.ServerDiskSpaceInformationInput1.setText(Data[0] + " GB")
            self.ServerDiskSpaceInformationInput2.setText(Data[1] + " GB")
