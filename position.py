##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from position_ui import Ui_dialog
import pyautogui
import time
import PIL.ImageQt
import zlib
from db import param


class Worker(QThread):

    im = pyqtSignal(PIL.ImageQt.ImageQt)
    xy = pyqtSignal(int, int)
    pb = pyqtSignal(int)
    we = pyqtSignal(int, int)
    

    def __init__(self):
        super().__init__()


    def run(self):
        xsz, ysz = pyautogui.size()
        confirm_delay = max(xsz * ysz / param['pixel per sec'], param['t confirm min'])
        last_chksum = last_update = 0
        last_x = last_y = 0
        self.running = True
        while self.running:
            x, y = pyautogui.position()
            im = pyautogui.screenshot(region=(x-49/2, y-23/2, 49, 23))
            chksum = zlib.crc32(im.tobytes())
            if last_chksum != chksum or last_x != x or last_y != y:
                last_x = x
                last_y = y
                last_chksum = chksum
                last_update = time.time()
                self.im.emit(PIL.ImageQt.ImageQt(im))
                self.pb.emit(0)
            else:
                logo_location = pyautogui.locateOnScreen('logo.png', grayscale=True, confidence=0.8)
                if logo_location:
                    logo_x, logo_y = pyautogui.center(logo_location)
                    self.xy.emit(x - logo_x, y - logo_y)
                    t = time.time()
                    if t < last_update + confirm_delay:
                        self.pb.emit(100*(t-last_update)/confirm_delay)
                    else:
                        tx, ty, tw, th = param['text region']
                        pyautogui.screenshot('t.png', region=(x+tx-tw/2, y+ty-th/2, tw, th))
                        self.pb.emit(100)
                        self.we.emit(x - logo_x, y - logo_y)
                        break


class Position(Ui_dialog):
    
    x = 0
    y = 0
    signal_stop = pyqtSignal()


    def __init__(self, dialog):
        super().__init__()
        self.dialog = dialog
        self.thread = Worker()
        self.thread.im.connect(self.on_update_image)
        self.thread.xy.connect(self.on_update_lcds)
        self.thread.pb.connect(self.on_update_progress)
        self.thread.we.connect(self.on_work_end)


    def on_scan(self):
        self.pushButtonScan.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
        self.pushButtonConfirm.setEnabled(False)
        self.thread.start()
        

    def on_stop(self):
        self.thread.running = False
        time.sleep(1)
        self.pushButtonScan.setEnabled(True)
        self.pushButtonStop.setEnabled(False)

    def on_confirm(self):
        self.thread.running = False
        self.dialog.close()

    def on_update_image(self, im):
        pixMap = QtGui.QPixmap.fromImage(im)
        self.labelImage.setPixmap(pixMap)


    def on_update_lcds(self, x, y):
        self.lcdNumberX.display(x)
        self.lcdNumberY.display(y)


    def on_update_progress(self, p):
        self.progressBar.setValue(p)


    def on_work_end(self, x, y):
        self.pushButtonScan.setEnabled(True)
        self.pushButtonStop.setEnabled(False)
        self.pushButtonConfirm.setEnabled(True)
        self.x, self.y = x, y


    def on_dialog_close(self, result):
        self.thread.running = False


    def connect(self):
        self.pushButtonScan.clicked.connect(self.on_scan)
        self.pushButtonStop.clicked.connect(self.on_stop)
        self.pushButtonConfirm.clicked.connect(self.on_confirm)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Position(dialog)
    ui.setupUi(dialog)
    ui.connect()
    dialog.finished.connect(ui.on_dialog_close)
    dialog.show()
    sys.exit(app.exec_())
