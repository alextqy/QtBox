# -*- coding:utf-8 -*-
from controller._base import *


class ConfigAction(BaseController):

    def __init__(self):
        super().__init__()

    # 查看系统配置
    def CheckConfig(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Check/Config")
        if self.Debug == True:
            print(Result)
        return Result

    # 修改配置
    def ModifyConfig(self, ID, ConfigKey="", ConfigDesc="", ConfigType=0, ConfigValue=""):
        Param = {
            "ID": ID,
            "ConfigKey": ConfigKey,
            "ConfigDesc": ConfigDesc,
            "ConfigType": ConfigType,
            "ConfigValue": ConfigValue,
        }
        Result = self.Post(Param, "/Modify/Config")
        if self.Debug == True:
            print(Result)
        return Result

    # 获取磁盘空间信息
    def GetHardDiskSpaceInfo(self):
        Result = self.Post({}, "/Get/HardDisk/Space/Info")
        if self.Debug == True:
            print(Result)
        return Result

    # 获取验签码
    def GetHardwareCode(self):
        Result = self.Post({}, "/Get/Hardware/Code")
        if self.Debug == True:
            print(Result)
        return Result

    # 产品激活
    def ProductActivation(self, EncryptedCode):
        Param = {"EncryptedCode": EncryptedCode}
        Result = self.Post(Param, "/Product/Activation")
        if self.Debug == True:
            print(Result)
        return Result

    # 账号统计
    def AccountNumberStatistics(self):
        Result = self.Post({}, "/Account/Number/Statistics")
        if self.Debug == True:
            print(Result)
        return Result

    # 系统日志
    def CheckSysLog(self, TimeStamp):
        Param = {"TimeStamp": TimeStamp}
        Result = self.Post(Param, "/Check/Sys/Log")
        if self.Debug == True:
            print(Result)
        return Result
