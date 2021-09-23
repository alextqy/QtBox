# -*- coding:utf-8 -*-
from controller._base import *


class DepartmentAction(BaseController):
    def __init__(self):
        super().__init__()

    # 创建部门
    def CreateDepartment(self, DepartmentName, ParentID):
        Param = {
            "DepartmentName": DepartmentName,
            "ParentID": ParentID,
        }
        Result = self.Post(Param, "/Create/Department")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除部门
    def DeleteDepartment(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Department")
        if self.Debug == True:
            print(Result)
        return Result

    # 部门状态开关
    def ToggleDepartment(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Toggle/Department")
        if self.Debug == True:
            print(Result)
        return Result

    # 修改部门信息
    def ModifyDepartment(self, ID, DepartmentName, ParentID):
        Param = {
            "ID": ID,
            "DepartmentName": DepartmentName,
            "ParentID": ParentID,
        }
        Result = self.Post(Param, "/Modify/Department")
        if self.Debug == True:
            print(Result)
        return Result

    # 部门详情
    def DepartmentInfo(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Department/Info")
        if self.Debug == True:
            print(Result)
        return Result

    # 遍历部门
    def SelectDepartment(self, ParentID=0, State=0, DepartmentName=""):
        Param = {
            "ParentID": ParentID,
            "State": State,
            "DepartmentName": DepartmentName,
        }
        Result = self.Post(Param, "/Select/Department")
        if self.Debug == True:
            print(Result)
        return Result

    # 添加部门扩展信息
    def CreateDepartmentExtra(self, DepartmentID, ExtraDesc, ExtraType, ExtraValue):
        Param = {
            "DepartmentID": DepartmentID,
            "ExtraDesc": ExtraDesc,
            "ExtraType": ExtraType,
            "ExtraValue": ExtraValue,
        }
        Result = self.Post(Param, "/Create/Department/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 删除部门扩展信息
    def DeleteDepartmentExtra(self, ID):
        Param = {
            "ID": ID,
        }
        Result = self.Post(Param, "/Delete/Department/Extra")
        if self.Debug == True:
            print(Result)
        return Result

    # 遍历部门扩展信息
    def SelectDepartmentExtra(self, DepartmentID=0, ExtraType=0):
        Param = {
            "DepartmentID": DepartmentID,
            "ExtraType": ExtraType,
        }
        Result = self.Post(Param, "/Select/Department/Extra")
        if self.Debug == True:
            print(Result)
        return Result
