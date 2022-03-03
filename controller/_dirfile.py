# -*- coding:utf-8 -*-
from controller._base import *


class DirFileAction(BaseController):

    def __init__(self):
        super().__init__()

    # 添加文件夹
    def CreateDir(self, DirName, ParentID):
        Param = {
            "DirName": DirName,
            "ParentID": ParentID,
        }
        Result = self.Post(Param, "/Create/Dir")
        if self.Debug == True:
            print(Result)
        return Result

    # 文件夹详情
    def DirInfo(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Dir/Info")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除文件夹
    def DeleteDir(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Dir")
        if self.Debug == True:
            print(Result)
        return Result

    # 修改文件夹信息
    def ModifyDir(self, ID, DirName, ParentID):
        Param = {
            "ID": ID,
            "DirName": DirName,
            "ParentID": ParentID,
        }
        Result = self.Post(Param, "/Modify/Dir")
        if self.Debug == True:
            print(Result)
        return Result

    # 遍历目录列表
    def SelectDir(self, ParentID=0, DirName="", UserID=0):
        Param = {
            "ParentID": ParentID,
            "DirName": DirName,
            "UserID": UserID,
        }
        Result = self.Post(Param, "/Select/Dir")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加文件夹扩展数据
    def CreateDirExtra(self, DirID, ExtraDesc, ExtraType, ExtraValue):
        Param = {
            "DirID": DirID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Create/Dir/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除文件夹扩展信息
    def DeleteDirExtra(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Dir/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 遍历文件夹扩展信息
    def SelectDirExtra(self, DirID=0, ExtraDesc="", ExtraType=0, ExtraValue=""):
        Param = {
            "DirID": DirID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Select/Dir/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 文件列表
    def FileList(self, DirID=0, State=2, UserID=0):
        Param = {
            "DirID": DirID,
            "State": State,
            "UserID": UserID,
        }
        Result = self.Post(Param, "/File/List")
        if self.Debug == True:
            print(Result)
        return Result

    # 新建文件
    def CreateFile(self, FileName, FileType, FileSize, UploadPath, DirID, MD5):
        Param = {
            "FileName": FileName,
            "FileType": FileType,
            "FileSize": FileSize,
            "UploadPath": UploadPath,
            "DirID": DirID,
            "MD5": MD5,
        }
        Result = self.Post(Param, "/Create/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 上传文件分片实体
    def UploadFileEntity(self, ID, FileSectionName, FileEntityPath):
        try:
            Param = {
                "ID": ID,
                "FileSectionName": FileSectionName,
            }
            FileEntityByte = {"FileEntity": open(FileEntityPath, "rb").read()}
            Result = self.Post(Param, "/Upload/File/Entity", "", "", "", FileEntityByte)
            if self.Debug == True:
                print(Result)
            return Result
        except Exception as e:
            return {"State": False, "Memo": "Nnoe"}

    # 下载文件分片实体
    def DownloadFileEntity(self, ID, POS):
        Param = {
            "ID": ID,
            "POS": POS,
        }
        Result = self.Post(Param, "/Download/File/Entity")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除文件
    def DeleteFile(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 重命名文件
    def ModifyFile(self, ID, FileName, State, FileSize, BlockSize, UploadBlockSize, DirID, MD5):
        Param = {
            "ID": ID,
            "FileName": FileName,
            "State": State,
            "FileSize": FileSize,
            "BlockSize": BlockSize,
            "UploadBlockSize": UploadBlockSize,
            "DirID": DirID,
            "MD5": MD5,
        }
        Result = self.Post(Param, "/Modify/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 移动文件
    def MoveFile(self, ID, DirID):
        Param = {
            "ID": ID,
            "DirID": DirID,
        }
        Result = self.Post(Param, "/Move/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 文件详情
    def CheckFile(self, FileID):
        Param = {
            "FileID": FileID,
        }
        Result = self.Post(Param, "/Check/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加文件扩展信息
    def CreateFileExtra(self, FileID, ExtraDesc, ExtraType, ExtraValue):
        Param = {
            "FileID": FileID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Create/File/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除文件扩展信息
    def DeleteFileExtra(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/File/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 遍历文件扩展信息
    def SelectFileExtra(self, FileID=0, ExtraDesc="", ExtraType=0, ExtraValue=""):
        Param = {
            "FileID": FileID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Select/File/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 复制文件
    def CopyFile(self, DirID, FileID):
        Param = {"DirID": DirID, "FileID": FileID}
        Result = self.Post(Param, "/Copy/File")
        if self.Debug == True:
            print(Result)
        return Result

    # 文件锁定开关
    def FileLockSwitch(self, FileID):
        Param = {"FileID": FileID}
        Result = self.Post(Param, "/File/Lock/Switch")
        if self.Debug == True:
            print(Result)
        return Result

    # 已锁定的文件列表
    def FileLockList(self):
        Param = {}
        Result = self.Post(Param, "/File/Lock/List")
        if self.Debug == True:
            print(Result)
        return Result

    # 同步前置操作
    def FileEntitySyncPrefix(self, FileID):
        Param = {"FileID": FileID}
        Result = self.Post(Param, "/File/Entity/Sync/Prefix")
        if self.Debug == True:
            print(Result)
        return Result

    # 同步操作
    def FileEntitySync(self, FileID, FileSectionName, FileEntity):
        Param = {
            "FileID": FileID,
            "FileSectionName": FileSectionName,
        }
        FileEntityByte = {"FileEntity": open(FileEntity, "rb").read()}
        Result = self.Post(Param, "/File/Entity/Sync", "", "", "", FileEntityByte)
        if self.Debug == True:
            print(Result)
        return Result

    # 同步后置操作
    def FileEntitySyncDefer(self, FileID):
        Param = {
            "FileID": FileID,
        }
        Result = self.Post(Param, "/File/Entity/Sync/Defer")
        if self.Debug == True:
            print(Result)
        return Result

    # 同步失败后的操作
    def FileEntitySyncFail(self, FileID):
        Param = {
            "FileID": FileID,
        }
        Result = self.Post(Param, "/File/Entity/Sync/Fail")
        if self.Debug == True:
            print(Result)
        return Result

    # 发送文件
    def SendFileToUser(self, FileID, UserID):
        Param = {
            "FileID": FileID,
            "UserID": UserID,
        }
        Result = self.Post(Param, "/Send/File/To/User")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加标签
    def CreateTag(self, TagName, TagMemo):
        Param = {
            "TagName": TagName,
            "TagMemo": TagMemo,
        }
        Result = self.Post(Param, "/Create/Tag")
        if self.Debug == True:
            print(Result)
        return Result

    # 修改标签
    def ModifyTag(self, ID, TagName, TagMemo):
        Param = {
            "ID": ID,
            "TagName": TagName,
            "TagMemo": TagMemo,
        }
        Result = self.Post(Param, "/Modify/Tag")
        if self.Debug == True:
            print(Result)
        return Result

    # 标签信息
    def TagInfo(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Tag/Info")
        if self.Debug == True:
            print(Result)
        return Result

    # 标签列表
    def TagList(self):
        Param = {}
        Result = self.Post(Param, "/Tag/List")
        if self.Debug == True:
            print(Result)
        return Result

    # 修改标签名称
    def TagRename(self, ID, TagName):
        Param = {
            "ID": ID,
            "TagName": TagName,
        }
        Result = self.Post(Param, "/Tag/Rename")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除标签
    def DelTag(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Del/Tag")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加文件标签
    def CreateFileTag(self, TagID, FileID):
        Param = {
            "TagID": TagID,
            "FileID": FileID,
        }
        Result = self.Post(Param, "/Create/File/Tag")
        if self.Debug == True:
            print(Result)
        return Result

    # 文件标签列表
    def FileTagList(self, TagID):
        Param = {
            "TagID": TagID,
        }
        Result = self.Post(Param, "/File/Tag/List")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除文件标签
    def DelFileTag(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Del/File/Tag")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加离线任务
    def CreateOfflineTask(self, URL, TaskMemo):
        Param = {
            "URL": URL,
            "TaskMemo": TaskMemo,
        }
        Result = self.Post(Param, "/Create/Offline/Task")
        if self.Debug == True:
            print(Result)
        return Result

    # 离线任务列表
    def OfflineTaskList(self):
        Param = {}
        Result = self.Post(Param, "/Offline/Task/List")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除离线任务
    def DelOfflineTask(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Del/Offline/Task")
        if self.Debug == True:
            print(Result)
        return Result

    # 设置离线任务状态
    def SetOfflineTaskState(self, ID, State):
        Param = {"ID": ID, "State": State}
        Result = self.Post(Param, "/Set/Offline/Task/State")
        if self.Debug == True:
            print(Result)
        return Result
