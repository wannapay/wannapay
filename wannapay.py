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

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from wannapay_ui import Ui_Dialog
import time
import pyautogui
from db import pps, param

GPLv3 = "This program is free software: you can redistribute it and/or modify \
it under the terms of the GNU General Public License as published by \
the Free Software Foundation, either version 3 of the License, or \
(at your option) any later version. \
This program is distributed in the hope that it will be useful, \
but WITHOUT ANY WARRANTY; without even the implied warranty of \
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the \
GNU General Public License for more details. \
You should have received a copy of the GNU General Public License \
along with this program.  If not, see <https://www.gnu.org/licenses/>."


def calc_amount(total, paid, amount):
    if round(paid + (2*amount), 1) > total:
        if round(total - paid - amount, 1) >= 1:
            return amount
        else:
            return round(total-paid, 1)
    else:
        return amount


def locate_n_act(action):
    import pyautogui
    import time
    for img in action['imgs']:
        location = pyautogui.locateOnScreen(img['name'], grayscale=img['grayscale'], confidence=img['confidence'])
        if location:
            x, y = pyautogui.center(location)
            pyautogui.moveTo(x+action['offset']['x'], y+action['offset']['y'], param['t mouse'], pyautogui.easeOutQuad)
            pyautogui.click()
            if 'keys' in action:
                pyautogui.typewrite(action['keys'], interval=param['t key'])
                pyautogui.press('enter')
            if 't_wait' in action:
                time.sleep(action['t_wait']*param['wait factor'])
            return True
    return False


class Worker(QThread):
    status = pyqtSignal(int, float)
    ending = pyqtSignal()

    def __init__(self):
        super().__init__()


    def on_init_data(self, total, amount, actions):
        self.total = total
        self.amount = amount
        self.actions = actions
        self.paid = 0


    def run(self):
        self.running = True
        try:
            while self.running and (self.paid < self.total):
                real_amount = calc_amount(self.total, self.paid, self.amount)
                #print(self.total, self.paid, real_amount)
                for action in self.actions:
                    #print(action)
                    if 'amount_keys' in action:
                        action['keys'] = str(real_amount)
                    if locate_n_act(action) == False:
                        break
                else:
                    self.paid = round(self.paid + real_amount, 1)
                    self.status.emit(int(100*self.paid/self.total), self.paid)
            else:
                self.status.emit(100, self.paid)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        self.ending.emit()


class Payment_Dialog(Ui_Dialog, QObject):
    sig_init_data = pyqtSignal(float, float, list)

    def __init__(self):
        super().__init__()
        self.bill = None
        self.actions = None
        self.total = 0
        self.amount = 0
        self.thread = Worker()
        self.thread.ending.connect(self.on_ending)
        self.thread.status.connect(self.on_status)
        self.sig_init_data.connect(self.thread.on_init_data)


    def on_dialog_close(self, event):
        self.thread.running = False


    def on_ending(self):
        import os
        os.remove('t.png')


    def on_real(self):
        if self.lineEditTotal.text():
            self.total = round(float(self.lineEditTotal.text()), 1)
        if self.lineEditAmount.text():
            self.amount = round(float(self.lineEditAmount.text()), 1)
        if (self.total >= self.amount >= 1) and self.bill:
            self.radioButtonWSD.setEnabled(False)
            self.radioButtonTax1.setEnabled(False)
            self.radioButtonTax2.setEnabled(False)
            self.radioButtonGRR.setEnabled(False)
            self.lineEditTotal.setEnabled(False)
            self.lineEditAmount.setEnabled(False)
            self.pushButtonDemo.setEnabled(False)
            self.pushButtonReal.setEnabled(False)
            self.actions = pps['real'][self.bill]
            self.actions[2]['offset'] = {'x':self.pay_x, 'y':self.pay_y}
            self.sig_init_data.emit(self.total, self.amount, self.actions)
            self.thread.start()


    def on_demo(self):
        if self.lineEditTotal.text():
            self.total = round(float(self.lineEditTotal.text()), 1)
        if self.lineEditAmount.text():
            self.amount = round(float(self.lineEditAmount.text()), 1)
        if (self.total >= self.amount >= 1) and self.bill:
            self.radioButtonWSD.setEnabled(False)
            self.radioButtonTax1.setEnabled(False)
            self.radioButtonTax2.setEnabled(False)
            self.radioButtonGRR.setEnabled(False)
            self.lineEditTotal.setEnabled(False)
            self.lineEditAmount.setEnabled(False)
            self.pushButtonDemo.setEnabled(False)
            self.pushButtonReal.setEnabled(False)
            self.actions = pps['demo'][self.bill]
            self.actions[2]['offset'] = {'x':self.pay_x, 'y':self.pay_y}
            self.sig_init_data.emit(self.total, self.amount, self.actions)
            self.thread.start()


    def on_status(self, progress, paid):
        self.progressBar.setValue(progress)
        self.lcdNumber.display(paid)


    def on_radio_wsd(self):
        if self.radioButtonWSD.isChecked():
            self.bill = 'wsd'
        self.start_position_dialog('08 水務署')


    def on_radio_tax1(self):
        if self.radioButtonTax1.isChecked():
            self.bill = 'tax1'
        self.start_position_dialog('10 稅務局')


    def on_radio_tax2(self):
        if self.radioButtonTax2.isChecked():
            self.bill = 'tax2'
        self.start_position_dialog('10 稅務局')


    def on_radio_grr(self):
        if self.radioButtonGRR.isChecked():
            self.bill = 'grr'
        self.start_position_dialog('09 差餉及地租')


    def on_terms_and_conditions(self):
        from PyQt5.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(GPLv3)
        msg.setWindowTitle("Terms and Conditions")
        msg.exec_()


    def start_position_dialog(self, bill):
        from position import Position
        dialog = QtWidgets.QDialog()
        ui = Position(dialog)
        ui.setupUi(dialog)
        ui.labelBill.setText(bill)
        ui.connect()
        dialog.finished.connect(ui.on_dialog_close)
        dialog.setModal(True)
        dialog.show()
        dialog.exec()
        self.pay_x, self.pay_y = ui.x, ui.y


    def connect(self):
        self.pushButtonDemo.clicked.connect(self.on_demo)
        self.pushButtonReal.clicked.connect(self.on_real)
        self.radioButtonWSD.clicked.connect(self.on_radio_wsd)
        self.radioButtonTax1.clicked.connect(self.on_radio_tax1)
        self.radioButtonTax2.clicked.connect(self.on_radio_tax2)
        self.radioButtonGRR.clicked.connect(self.on_radio_grr)
        self.pushButtonTnC.clicked.connect(self.on_terms_and_conditions)


if __name__ == "__main__":
    import sys
    import images
    images.prepare_images()
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Payment_Dialog()
    ui.setupUi(Dialog)
    ui.connect()
    Dialog.finished.connect(ui.on_dialog_close)
    Dialog.show()
    sys.exit(app.exec_())
