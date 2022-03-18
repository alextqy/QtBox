# -*- coding:utf-8 -*-
from controller._library import *

from public.zead import *
from style.zead import *
from controller.zead import *
import urllib3


class BaseController():

    def __init__(self):
        super().__init__()
        self.Cache = Cache()
        self.Debug = self.Cache.Get("Debug")
        self.SwitchHttps = self.Cache.Get("SwitchHttps")
        if self.SwitchHttps == False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    '''
    参数:
        1 Param       数据
        2 Func        方法名
        3 URL         url地址
        4 Token
        5 TokenType   token类型
        6 Files       上传文件
        7 Headers     浏览器header信息
    '''

    def Post(self, Param={}, Func="", URL="", Token="", TokenType="", Files=None, Headers=None):
        if Func == "":
            return False
        if self.Cache.Get("URL") != "":
            URL = self.Cache.Get("URL")
        Token = self.Cache.Get("Token")
        TokenType = self.Cache.Get("TokenType")
        BaseData = {
            "Token": Token,
            "TokenType": TokenType,
        }
        PostData = {**BaseData, **Param}  # 数据合并
        try:
            JsonResult = post(URL + Func, PostData, files=Files, headers=Headers, verify=self.SwitchHttps)  # 返回json数据
            return loads(JsonResult.text)
        except OSError as e:
            return {"State": False, "Memo": "error"}

    def Get(self, URL="", **args):
        return get(URL, **args)
