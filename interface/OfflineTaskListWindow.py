from interface._base import *


class OfflineTaskListWindow(BaseInterface, BaseDialog):
    ActionSignal = Signal()  # 设置信号

    def __init__(self):
        super().__init__()
