# -*- coding:utf-8 -*-
from interface._base import *


class FileTagFrame(BaseInterface, BaseFrame):
    def __init__(self):
        super().__init__()

        # =========================================== Ready ===========================================

        SelectTagData = DirFileAction().TagList()
        if SelectTagData["State"] != True:
            return

        self.TagData = SelectTagData["Data"]
        self.CurrentTagID = 0
        print(self.TagData)
