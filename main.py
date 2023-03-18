import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

WORKINGDIR = os.getcwd()

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create address bar and go button
        self.address_label = QLabel("Address:")
        self.address_entry = QLineEdit()
        self.address_entry.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.address_entry.returnPressed.connect(self.fetch_page)

        toolbar = QToolBar()
        toolbar.addWidget(self.address_label)
        toolbar.addWidget(self.address_entry)
        self.addToolBar(toolbar)

        # Create web view to display web pages
        storage_path = "%LOCALAPPDATA%\\PyBrowse\\storage"
        profile = QWebEngineProfile(storage_path, self)
        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.url_changed)

        self.web_view.setPage(QWebEnginePage(profile, self.web_view))
        self.setCentralWidget(self.web_view)

    def url_changed(self):
        self.address_entry.setText(self.web_view.url().toString())

    def fetch_page(self):
        input_text = self.address_entry.text()

        if "." not in input_text:
            input_text = "https://google.com/?q=" + input_text
        if not input_text[:4] == "http":
            input_text = "http://" + input_text
            self.address_entry.setText(input_text)
            
        self.web_view.load(QUrl(input_text))


# Create the application and start the main event loop
app = QApplication(sys.argv)
browser = Browser()
browser.showMaximized()
sys.exit(app.exec_())
