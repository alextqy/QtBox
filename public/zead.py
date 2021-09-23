# -*- coding:utf-8 -*-
from public._base import *
from public._cache import Cache
from public._common import Common
from public._file import File
from public._lang import Lang
from public._udptool import UDPTool

TITLE = "BITBOX"
UPLOADDIR = "/temp/BITBOX_UPLOAD_FOLDER"
DOWNLOADDIR = "/temp/BITBOX_DOWNLOAD_FOLDER"
DOWNLOADTEMP = "/temp/BITBOX_DOWNLOAD_TEMP"
TEMPDIR = "/temp/BITBOX_TEMP"
FILESLICESIZE = 1024 * 1024 * 2
PREVIEWSIZELIMIT = 1024 * 1024 * 5

ICON = os.getcwd() + "/source/bitbox.png"
TOPLOGO = os.getcwd() + "/source/toplogo.png"
SIGNIN = os.getcwd() + "/source/signin.png"
FLIST = os.getcwd() + "/source/list.png"
FGRID = os.getcwd() + "/source/grid.png"
UPLOAD = os.getcwd() + "/source/upload.png"
DOWNLOAD = os.getcwd() + "/source/download.png"
UNLOCK = os.getcwd() + "/source/unlock.png"
GCODE = os.getcwd() + "/source/gcode.png"
ACODE = os.getcwd() + "/source/acode.png"
FEEDBACK = os.getcwd() + "/source/feedback.png"
SUBMIT = os.getcwd() + "/source/submit.png"
CLEAR = os.getcwd() + "/source/clear.png"
SIGNOUT = os.getcwd() + "/source/signout.png"
