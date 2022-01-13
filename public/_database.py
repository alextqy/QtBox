# -*- coding:utf-8 -*-
from public._base import *
import sqlite3


class Database():
    # DBFileURL = os.path.join(os.getcwd()) + "/DBRoom.db"

    def __init__(self, DBRoomPath):
        super().__init__()
        self.Init()
        self.DBFileURL = DBRoomPath

    def Init(self):
        if not isfile(self.DBFileURL):
            file = open(self.DBFileURL, "w")
            file.close()
        self.SqlCon = sqlite3.connect(self.DBFileURL)
        self.Cur = self.SqlCon.cursor()

    def Cmd(self, CommandParam):
        return self.Cur.execute(CommandParam)

    def Tran(self):
        self.Cur.execute("BEGIN TRANSACTION")

    def Rollback(self):
        self.Cur.execute("ROLLBACK")

    def Commit(self):
        self.Cur.execute("COMMIT")
