import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from edit import Ui_Dialog


class EditingForm(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_7.hide()
        self.send_btn.clicked.connect(self.correct_data)

    def correct_data(self):
        if self.kind.text() != "" and self.degree.text() != ""\
                and self.type.text() != "" and self.desc.text() != "" and\
                self.price.text() != "" and self.volume.text() != "":
            return 1
        else:
            self.label_7.show()
            return 0