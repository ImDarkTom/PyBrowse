import sys
import os
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

WORKINGDIR = os.getcwd()

# Read search engines file and extract default search engine URL
with open("settings/searchEngines.json", "r") as f:
    search_engines = json.load(f)

default_index = 0
with open("settings/clientSettings.json", "r") as f:
    client_settings = json.load(f)
    default_index = client_settings["preferred_search_engine_index"]

default_search_url = search_engines["search_engines"][default_index]["url"]
default_search_name = search_engines["search_engines"][default_index]["name"]

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.coreLayout = QVBoxLayout()
        self.navbar = QHBoxLayout()

        # Create web view to display web pages
        storage_path = "%LOCALAPPDATA%\\PyBrowse\\storage"
        profile = QWebEngineProfile(storage_path, self)
        self.web_view = QWebEngineView()
        self.web_view.urlChanged.connect(self.url_changed)

        # Create the navigation buttons
        self.back_button = QPushButton("←")
        self.back_button.clicked.connect(self.web_view.back)

        self.forward_button = QPushButton("→")
        self.forward_button.clicked.connect(self.web_view.forward)

        self.refresh_button = QPushButton("↻")
        self.refresh_button.clicked.connect(self.web_view.reload)

        # Create address bar
        self.address_entry = QLineEdit()
        self.address_entry.setPlaceholderText(f"Search with {default_search_name} or enter address")
        self.address_entry.returnPressed.connect(self.fetch_page)

        self.navbar.addWidget(self.back_button)
        self.navbar.addWidget(self.forward_button)
        self.navbar.addWidget(self.refresh_button)
        self.navbar.addWidget(self.address_entry)

        self.coreLayout.addLayout(self.navbar)

        navigation_layout = QHBoxLayout()
        navigation_layout.addWidget(self.back_button)
        navigation_layout.addWidget(self.forward_button)
        navigation_layout.addWidget(self.refresh_button)

        self.coreLayout.addWidget(self.web_view)

        # Set the layout to the main window
        central_widget = QWidget()
        central_widget.setLayout(self.coreLayout)
        self.setCentralWidget(central_widget)


        #Styling
        self.coreLayout.setContentsMargins(0,0,0,0)


    def url_changed(self):
        self.address_entry.setText(self.web_view.url().toString())

    def fetch_page(self):
        input_text = self.address_entry.text()

        if "." not in input_text:
            input_text = default_search_url + input_text
        if not input_text[:4] == "http":
            input_text = "http://" + input_text
            self.address_entry.setText(input_text)
            
        self.web_view.load(QUrl(input_text))
        self.address_entry.clearFocus()


# Create the application and start the main event loop
app = QApplication(sys.argv)
browser = Browser()

browser.showMaximized()
browser.setMinimumHeight(50)

browser.setWindowTitle("PyBrowse")

sys.exit(app.exec_())
