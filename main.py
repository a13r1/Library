"""
@Author: Ali Rihan
@Link: github.com/a13r1/Library
"""

import sys

import MySQLdb
from PyQt5 import uic
from PyQt5.QtWidgets import *


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi('main.ui', self)
        # connect to library database
        self.db = MySQLdb.connect(host='localhost', user='root', passwd='', db='library')
        self.cursor = self.db.cursor()
        # GUI preprocessing
        self.show_all_books()
        self.handle_buttons()
        self.tabWidget.tabBar().setVisible(False)
        self.show()

    def show_books_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def show_daily_movements_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def show_authors_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def show_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def show_all_books(self):
        """
        fetch and display all books in the GUI table
        :return: None
        """
        self.tableWidget.setRowCount(0)  # clear the table
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        for i, record in enumerate(books):
            self.tableWidget.insertRow(i)
            for j, field in enumerate(record):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(field)))

    def insert_book(self):
        """
        insert a new book in books table
        :return: None
        """
        # prepare query string
        name = self.add_name.text()
        barcode = self.add_barcode.text()
        author = self.add_author.text()
        publisher = self.add_publisher.text()
        query_str = f"INSERT INTO books (name, barcode, author, publisher) VALUES" \
                    f"('{name}', '{barcode}', '{author}', '{publisher}')"
        self.cursor.execute(query_str)
        self.db.commit()
        QMessageBox.information(self, 'Add a new book', 'Book is added successfully!')
        self.show_all_books()  # update GUI table
        # clear input
        self.add_name.setText('')
        self.add_barcode.setText('')
        self.add_author.setText('')
        self.add_publisher.setText('')

    def search_book(self):
        """
        search for a book and display its information
        :return: None
        """
        book_id = self.update_id.text()
        query_str = f'SELECT * FROM books WHERE id = {book_id}'
        self.cursor.execute(query_str)
        record = self.cursor.fetchone()
        # display information to be modified
        self.update_name.setText(record[1])
        self.update_barcode.setText(record[2])
        self.update_author.setText(record[3])
        self.update_publisher.setText(record[4])

    def update_book(self):
        """
        update existing book information
        :return: None
        """
        # prepare query string
        book_id = self.update_id.text()
        name = self.update_name.text()
        barcode = self.update_barcode.text()
        author = self.update_author.text()
        publisher = self.update_publisher.text()
        query_str = f"UPDATE books SET name = '{name}', barcode = '{barcode}', author = '{author}'," \
                    f"publisher = '{publisher}' WHERE id = {book_id}"
        self.cursor.execute(query_str)
        self.db.commit()
        self.show_all_books()  # update GUI table
        QMessageBox.information(self, 'Update a book', 'Book is updated successfully!')
        # clear input
        self.update_id.setText('')
        self.update_name.setText('')
        self.update_barcode.setText('')
        self.update_author.setText('')
        self.update_publisher.setText('')

    def delete_book(self):
        """
        delete an existing book from books table
        :return: None
        """
        del_msg = QMessageBox.question(self, 'Delete a book', 'Are you sure you want to delete the book?',
                                       QMessageBox.Yes | QMessageBox.No,
                                       defaultButton=QMessageBox.No)
        if del_msg == QMessageBox.Yes:
            book_id = self.delete_id.text()
            query_str = f'DELETE FROM books WHERE id = {book_id}'
            self.cursor.execute(query_str)
            self.db.commit()
            QMessageBox.information(self, 'Delete a book', 'Book is deleted successfully!')
            self.show_all_books()  # update GUI table
            self.delete_id.setText('')  # clear input

    def handle_buttons(self):
        """
        connect buttons click events to their corresponding actions
        :return: None
        """
        self.add_button.clicked.connect(self.insert_book)
        self.search_button.clicked.connect(self.search_book)
        self.update_button.clicked.connect(self.update_book)
        self.delete_button.clicked.connect(self.delete_book)
        self.books_button.clicked.connect(self.show_books_tab)
        self.daily_movements_button.clicked.connect(self.show_daily_movements_tab)
        self.authors_button.clicked.connect(self.show_authors_tab)
        self.settings_button.clicked.connect(self.show_settings_tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    app.exec_()
