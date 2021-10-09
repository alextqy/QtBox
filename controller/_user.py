# -*- coding:utf-8 -*-
from controller._base import *


class UserAction(BaseController):
    def __init__(self):
        super().__init__()

    # 登陆
    def SignIn(self, Account, Password, Type, URL):
        Param = {
            "Account": Account,
            "Password": Password,
            "Type": Type,
        }
        Result = self.Post(Param, "/Sign/In", URL)
        if self.Debug == True:
            print(Result)
        return Result

    # 退出
    def SignOut(self):
        Param = {}
        Result = self.Post(Param, "/Sign/Out")
        if self.Debug == True:
            print(Result)
        return Result

    # 登录状态
    def TokenRunningState(self):
        Param = {}
        Result = self.Post(Param, "/Token/Running/State")
        if self.Debug == True:
            print(Result)
        return Result

    # 个人信息
    def CheckSelf(self):
        Param = {}
        Result = self.Post(Param, "/Check/Self")
        if self.Debug == True:
            print(Result)
        return Result

    # 修改个人信息
    # "", "", "", "", "", 0, "", 0, 0, 0
    def UserModify(self, Name, Password, Avatar, Wallpaper, Admin, Status, Permission, Master, DepartmentID, ID=0):
        Param = {
            "Name": Name,
            "Password": Password,
            "Avatar": Avatar,
            "Wallpaper": Wallpaper,
            "Admin": Admin,
            "Status": Status,
            "Permission": Permission,
            "Master": Master,
            "DepartmentID": DepartmentID,
            "ID": ID,
        }
        Result = self.Post(Param, "/User/Modify")
        if self.Debug == True:
            print(Result)
        return Result

    # 是否超级管理员
    def IsMaster(self):
        Param = {}
        Result = self.Post(Param, "/Is/Master")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加用户
    def CreateUser(self, Account, Name, Password, Avatar="", Wallpaper="", Admin=1, Status=1, Permission="1,2,3,4,5,6,7,8,9", Master=1, DepartmentID=0):
        Param = {
            "Account": Account,
            "Name": Name,
            "Password": Password,
            "Avatar": Avatar,
            "Wallpaper": Wallpaper,
            "Admin": Admin,
            "Status": Status,
            "Permission": Permission,
            "Master": Master,
            "DepartmentID": DepartmentID,
        }
        Result = self.Post(Param, "/Create/User")
        if self.Debug == True:
            print(Result)
        return Result

    # 移除用户
    def RemoveUser(self, UserID):
        Param = {
            "UserID": UserID,
        }
        Result = self.Post(Param, "/Remove/User")
        if self.Debug == True:
            print(Result)
        return Result

    # 用户详情
    def UserInfo(self, UserID):
        Param = {
            "UserID": UserID,
        }
        Result = self.Post(Param, "/User/Info")
        if self.Debug == True:
            print(Result)
        return Result

    # 用户列表
    def SelectUser(self, DepartmentID=0, State=1, Master=0, Admin=0, Account="", Name=""):
        Param = {
            "Account": Account,
            "Name": Name,
            "State": State,
            "Admin": Admin,
            "Master": Master,
            "DepartmentID": DepartmentID,
        }
        Result = self.Post(Param, "/Select/User")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加用户扩展信息
    def CreateUserExtra(self, ExtraDesc, ExtraType, ExtraValue, UserID=0):
        Param = {
            "UserID": UserID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Create/User/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除用户扩展信息
    def DeleteUserExtra(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/User/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 遍历用户扩展信息
    def SelectUserExtra(self, ExtraDesc="", ExtraType=0, ExtraValue="", UserID=0):
        Param = {
            "UserID": UserID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Select/User/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 日志列表
    def SelectLog(self, IP="", ActionType=0):
        Param = {
            "IP": IP,
            "ActionType": ActionType,
        }
        Result = self.Post(Param, "/Select/Log")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除日志
    def DeleteLog(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Log")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加外部Token
    def CreateOuterToken(self, OuterToken, TokenDesc):
        Param = {
            "OuterToken": OuterToken,
            "TokenDesc": TokenDesc,
        }
        Result = self.Post(Param, "/Create/Outer/Token")
        if self.Debug == True:
            print(Result)
        return Result

    # 获取外部Token
    def CheckOuterToken(self, OuterToken):
        Param = {
            "OuterToken": OuterToken,
        }
        Result = self.Post(Param, "/Check/Outer/Token")
        if self.Debug == True:
            print(Result)
        return Result

    # 发送数据
    def CreateMessage(self, Content, ReceiverID, Title="None"):
        Param = {
            "Content": Content,
            "ReceiverID": ReceiverID,
            "Title": Title,
        }
        Result = self.Post(Param, "/Create/Message")
        if self.Debug == True:
            print(Result)
        return Result

    # 查看信息
    def CheckMessage(self, ID):
        Param = {
            "ID", ID,
        }
        Result = self.Post(Param, "/Check/Message")
        if self.Debug == True:
            print(Result)
        return Result

    # 信息列表 1 收到的信息 2 发送的信息
    def MessageList(self, MessageType, UserID, State, StartPoint=0, EndPoint=0):
        Param = {
            "MessageType": MessageType,
            "UserID": UserID,
            "State": State,
            "StartPoint": StartPoint,
            "EndPoint": EndPoint,
        }
        Result = self.Post(Param, "/Message/List")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除信息
    def DeleteMessage(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Message")
        if self.Debug == True:
            print(Result)
        return Result

    # 设置为已读
    def SetMessage(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Set/Message")
        if self.Debug == True:
            print(Result)
        return Result

    # 分享文件到部门
    def ShareFilesToDepartment(self, FileID):
        Param = {
            "FileID": FileID,
        }
        Result = self.Post(Param, "/Share/Files/To/Department")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除分享的文件
    def DeleteDepartmentFile(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Department/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 部门文件列表
    def SelectDepartmentFile(self, DepartmentID=0, FileID=0, UserID=0):
        Param = {
            "DepartmentID": DepartmentID,
            "FileID": FileID,
            "UserID": UserID,
        }
        Result = self.Post(Param, "/Select/Department/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 查看用户导入Demo
    def CheckImportUsersDemo(self, LangType):
        Param = {
            "LangType": LangType,
        }
        Result = self.Post(Param, "/Download/Demo")
        if self.Debug == True:
            print(Result)
        return Result
