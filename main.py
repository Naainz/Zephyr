import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFontDatabase, QFont, QKeySequence

class Zephyr(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load Font Awesome using an absolute path
        ttf_path = os.path.join(os.path.dirname(__file__), 'fa-solid-900.ttf')
        font_id = QFontDatabase.addApplicationFont(ttf_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.fa_font = QFont(font_family)
            self.fa_font.setPointSize(12)
        else:
            print("Failed to load Font Awesome")
            sys.exit(-1)

        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        navbar = QToolBar()
        navbar.setStyleSheet("""
            QToolBar {
                background-color: #F1F3F4;
                border: none;
                padding: 5px;
            }
        """)
        navbar.setIconSize(QSize(16, 16))
        main_layout.addWidget(navbar)

        # Back button using QPushButton
        back_btn = QPushButton("\uf053", self)  # FontAwesome arrow-left icon
        back_btn.setFont(self.fa_font)
        back_btn.clicked.connect(lambda: self.current_browser().back())
        navbar.addWidget(back_btn)

        # Forward button using QPushButton
        forward_btn = QPushButton("\uf054", self)  # FontAwesome arrow-right icon
        forward_btn.setFont(self.fa_font)
        forward_btn.clicked.connect(lambda: self.current_browser().forward())
        navbar.addWidget(forward_btn)

        # Reload button using QPushButton
        reload_btn = QPushButton("\uf021", self)  # FontAwesome sync icon
        reload_btn.setFont(self.fa_font)
        reload_btn.clicked.connect(lambda: self.current_browser().reload())
        navbar.addWidget(reload_btn)

        # Home button using QPushButton
        home_btn = QPushButton("\uf015", self)  # FontAwesome home icon
        home_btn.setFont(self.fa_font)
        home_btn.clicked.connect(self.navigate_home)
        navbar.addWidget(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border-radius: 10px;
                border: 1px solid #DADCE0;
                background-color: white;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # New tab button using QPushButton
        new_tab_btn = QPushButton("\uf067", self)  # FontAwesome plus icon
        new_tab_btn.setFont(self.fa_font)
        new_tab_btn.clicked.connect(self.add_new_tab)
        navbar.addWidget(new_tab_btn)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

        # Remove unsupported properties: transition and transform
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                position: relative;
                top: -12px;
                background: none;
            }
            QTabBar::tab {
                background: #E8EAED;
                border: 1px solid #DADCE0;
                border-bottom: none;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                padding: 8px;
                margin-right: 2px;
                margin-bottom: 0px;
                min-width: 150px;
                text-align: center;
                vertical-align: middle;
                height: 30px;
            }
            QTabBar::tab:selected {
                background: white;
                border-color: #DADCE0;
            }
            QTabBar::tab:hover {
                background: #F8F9FA;
            }
        """)

        main_layout.addWidget(self.tabs)

        self.browser_area = QWebEngineView()
        main_layout.addWidget(self.browser_area)

        self.add_new_tab(QUrl("http://www.google.com"), 'Home')

        self.showMaximized()

        # Ensure QKeySequence is imported and used correctly
        new_tab_shortcut = QShortcut(QKeySequence('Ctrl+T'), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)

        close_tab_shortcut = QShortcut(QKeySequence('Ctrl+W'), self)
        close_tab_shortcut.activated.connect(lambda: self.close_current_tab(self.tabs.currentIndex()))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab and event.modifiers() == Qt.ControlModifier:
            self.next_tab()
        elif event.key() == Qt.Key_Tab and event.modifiers() == (Qt.ControlModifier | Qt.ShiftModifier):
            self.previous_tab()
        else:
            super().keyPressEvent(event)

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or isinstance(qurl, bool):
            qurl = QUrl("http://www.google.com")

        new_browser = QWebEngineView()
        new_browser.setUrl(qurl)
        new_browser.urlChanged.connect(self.update_url_bar)

        i = self.tabs.addTab(new_browser, label)
        self.tabs.setCurrentIndex(i)

        new_browser.loadFinished.connect(lambda _, i=i, browser=new_browser:
                                         self.tabs.setTabText(i, browser.page().title()))

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def next_tab(self):
        current_index = self.tabs.currentIndex()
        next_index = (current_index + 1) % self.tabs.count()
        self.tabs.setCurrentIndex(next_index)

    def previous_tab(self):
        current_index = self.tabs.currentIndex()
        prev_index = (current_index - 1) % self.tabs.count()
        self.tabs.setCurrentIndex(prev_index)

    def current_browser(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url_bar(self):
        q = self.current_browser().url()
        self.url_bar.setText(q.toString())

        self.tabs.setTabText(self.tabs.currentIndex(), self.current_browser().page().title())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('Zephyr')
    window = Zephyr()
    window.show()
    sys.exit(app.exec_())
