# import sys
# import traceback
#
# def exception_hook(exctype, value, tb):
#     traceback.print_exception(exctype, value, tb)
#
# sys.excepthook = exception_hook
import sys

from PyQt5.QtWidgets import (
    QApplication
)

from ui.main_window import (
    MainWindow
)

app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec_())




######KHI CÓ MỘT LỖI CÓ QUÁ NHIỀU THÌ CỘT PPM KHÔNG TỰ CHIA LẠI ĐƯỢC BƯỚC (ĐANG MẶC ĐỊNH 2000)Ở CÁC BIEU DO CHO 4 HANDLER

