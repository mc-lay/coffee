import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from m import Ui_MainWindow
from editing import EditingForm


class DBSample(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.select_data()

        self.pushButton.clicked.connect(self.new_form_to_add)
        self.pushButton_2.clicked.connect(self.new_form_to_correct)

        self.additional_form = EditingForm()
        self.additional_form.accepted.connect(self.change_db)
        self.additional_form.send_btn.clicked.connect(self.accept_wd)

        self.id_to_change = None

        self.to_change = False

    def select_data(self):
        res = self.connection.cursor().execute("""SELECT * FROM coffee""").fetchall()
        titles = self.connection.cursor().execute('PRAGMA table_info("coffee")')
        titles = [i[1] for i in titles]
        res.insert(0, titles)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
    def new_form_to_add(self):
        self.to_change = False
        self.additional_form.label_7.hide()
        self.additional_form.kind.clear()
        self.additional_form.degree.clear()
        self.additional_form.type.clear()
        self.additional_form.desc.clear()
        self.additional_form.price.clear()
        self.additional_form.volume.clear()
        self.additional_form.exec()
    def new_form_to_correct(self):
        cur_i = self.tableWidget.currentItem()
        if cur_i is not None:
            cur_row = cur_i.row()
            data_to_fill = []
            for col in range(7):
                data_to_fill.append(self.tableWidget.item(cur_row, col).text())
            self.id_to_change = data_to_fill[0]
            self.additional_form.label_7.hide()
            self.additional_form.kind.setText(data_to_fill[1])
            self.additional_form.degree.setText(data_to_fill[2])
            self.additional_form.type.setText(data_to_fill[3])
            self.additional_form.desc.setText(data_to_fill[4])
            self.additional_form.price.setText(data_to_fill[5])
            self.additional_form.volume.setText(data_to_fill[6])
            self.to_change = True
            self.additional_form.exec()
    def accept_wd(self):
        if self.additional_form.correct_data():
            self.additional_form.accept()
    def change_db(self):
        kind, degree, coffee_type, desc, price, volume = self.additional_form.kind.text(),\
                                                         self.additional_form.degree.text(),\
                                                         self.additional_form.type.text(),\
                                                         self.additional_form.desc.text(),\
                                                         self.additional_form.price.text(),\
                                                         self.additional_form.volume.text()

        if not self.to_change:

            self.connection.cursor().execute(f"""
                INSERT INTO coffee('kind', 'degree of roast', 'ground / in grains',
                 'taste description', 'price', 'packing volume')
                VALUES('{kind}', '{degree}', '{coffee_type}', '{desc}', '{price}', '{volume}')
                    """)

        else:
            self.connection.cursor().execute(f"""
                            Update coffee
                            set 'kind' = '{kind}',
                            'degree of roast' = '{degree}',
                            'ground / in grains' = '{coffee_type}',
                            'taste description' = '{desc}',
                            'price' = '{price}',
                            'packing volume' = '{volume}'
                            where id = {self.id_to_change}
                                """)
            self.to_change = False

        self.connection.commit()
        self.select_data()
    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
