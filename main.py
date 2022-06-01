from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import MySQLdb


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('main.ui', self)
        self.db_connect()
        self.show_all_books()
        self.handle_buttons()
        self.tabWidget.tabBar().setVisible(False)
        self.show()

    def db_connect(self):
        self.db = MySQLdb.connect(host='localhost', user='root', passwd='', db='library')
        self.cur = self.db.cursor()

    def handle_buttons(self):
        self.pushButton.clicked.connect(self.add_book)
        self.pushButton_6.clicked.connect(self.show_books_tab)
        self.pushButton_2.clicked.connect(self.show_daily_movements_tab)
        self.pushButton_3.clicked.connect(self.show_authors_tab)
        self.pushButton_4.clicked.connect(self.show_settings_tab)
        self.pushButton_7.clicked.connect(self.delete_book)
        self.pushButton_9.clicked.connect(self.search_book)
        self.pushButton_8.clicked.connect(self.update_book)

    def show_all_books(self):
        self.tableWidget.setRowCount(0)
        self.cur.execute('select * from books')
        data = self.cur.fetchall()
        for row, form in enumerate(data):
            self.tableWidget.insertRow(row)
            for col, item in enumerate(form):
                self.tableWidget.setItem(row, col, QTableWidgetItem(str(item)))

    def add_book(self):
        name = self.lineEdit_1.text()
        barcode = self.lineEdit_2.text()
        author = self.lineEdit_3.text()
        publisher = self.lineEdit_4.text()
        self.cur.execute('insert into books (name, barcode, author, publisher) values(%s, %s, %s, %s)',
                         (name, barcode, author, publisher))
        self.db.commit()
        QMessageBox.information(self, 'Add book', 'Book is added successfully')
        self.show_all_books()
        self.lineEdit_1.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')

    def delete_book(self):
        del_msg = QMessageBox.question(self, 'Delete a book', 'Are you sure?', QMessageBox.Yes | QMessageBox.No,
                                       defaultButton=QMessageBox.No)
        if del_msg == QMessageBox.Yes:
            id = self.lineEdit_5.text()
            self.cur.execute('delete from books where id = %s', id)
            self.db.commit()
            QMessageBox.information(self, 'Delete book', 'Book is deleted successfully')
            self.show_all_books()
            self.lineEdit_5.setText('')

    def show_books_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def show_daily_movements_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def show_authors_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def show_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def search_book(self):
        id = self.lineEdit_10.text()
        self.cur.execute('select * from books where id = %s', id)
        data = self.cur.fetchone()
        self.lineEdit_6.setText(data[1])
        self.lineEdit_7.setText(data[2])
        self.lineEdit_8.setText(data[3])
        self.lineEdit_9.setText(data[4])

    def update_book(self):
        id = self.lineEdit_10.text()
        name = self.lineEdit_6.text()
        barcode = self.lineEdit_7.text()
        author = self.lineEdit_8.text()
        publisher = self.lineEdit_9.text()
        self.cur.execute('''update books set name = %s, barcode = %s, author = %s, publisher = %s 
        where id = %s''', (name, barcode, author, publisher, id))
        self.db.commit()
        self.show_all_books()
        QMessageBox.information(self, 'Update book', 'Book is updated successfully')
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_8.setText('')
        self.lineEdit_9.setText('')
        self.lineEdit_10.setText('')


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
