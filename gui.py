from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QProgressBar, QCheckBox
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtGui import QDesktopServices
import sys
import os
from threading import Thread
from pdf_processor import main

class PDFSummarizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Summarizer')
        self.setGeometry(100, 100, 400, 350)

        self.label = QLabel('Select PDF file to summarize:', self)
        self.label.move(20, 20)

        self.button = QPushButton('Select File', self)
        self.button.move(20, 50)
        self.button.clicked.connect(self.select_file)

        self.handwritten_checkbox = QCheckBox('Handwritten', self)
        self.handwritten_checkbox.move(20, 90)

        self.two_column_checkbox = QCheckBox('Two-Column Format', self)
        self.two_column_checkbox.move(20, 120)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 150, 360, 30)
        self.progress.setValue(0)

        self.output_label = QLabel('', self)
        self.output_label.move(20, 190)

        self.open_folder_button = QPushButton('Open Folder', self)
        self.open_folder_button.setGeometry(20, 230, 360, 30)
        self.open_folder_button.setEnabled(False)
        self.open_folder_button.clicked.connect(self.open_folder)

        self.output_pdf_path = ""

    def select_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter('PDF Files (*.pdf)')
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                input_pdf_path = file_paths[0]

                # Construct the path to the user's Downloads folder
                downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
                self.output_pdf_path = os.path.join(downloads_folder, 'summarized_output.pdf')

                is_handwritten = self.handwritten_checkbox.isChecked()
                is_two_column = self.two_column_checkbox.isChecked()

                self.progress.setValue(0)
                thread = Thread(target=self.run_main, args=(input_pdf_path, self.output_pdf_path, is_handwritten, is_two_column))
                thread.start()

    def run_main(self, input_pdf_path, output_pdf_path, is_handwritten, is_two_column):
        try:
            main(input_pdf_path, output_pdf_path, is_handwritten, is_two_column, self.update_progress)
            self.output_label.setText('PDF summarized successfully!')
            self.open_folder_button.setEnabled(True)  # Enable the button after processing
        except Exception as e:
            self.output_label.setText(f'Error: {e}')

    def update_progress(self, value):
        self.progress.setValue(int(value))

    def open_folder(self):
        if self.output_pdf_path:
            folder = os.path.dirname(self.output_pdf_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFSummarizerApp()
    window.show()
    sys.exit(app.exec_())
