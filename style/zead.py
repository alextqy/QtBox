# -*- coding:utf-8 -*-
from style._base import *
from style._default import *
from style._dark import *
from style._light import *


class MainQSS():

    def __init__(self, StyleType=""):
        super().__init__()
        if StyleType == "default":
            self.Object = DefaultQSS()
        elif StyleType == "light":
            self.Object = LightQSS()
        elif StyleType == "dark":
            self.Object = DarkQSS()
        else:
            self.Object = DefaultQSS()
