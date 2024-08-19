import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *


class Zephyr(QMainWindow):

    def __init__(self):
        super().__init__()

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

        back_btn = QAction('⬅️', self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)

        forward_btn = QAction('➡️', self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction('⟳', self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction('🏠', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

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

        new_tab_btn = QAction('+', self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_btn)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setElideMode(Qt.ElideRight)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

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
                transition: background 0.3s, transform 0.3s;
            }
            QTabBar::tab:selected {
                background: white;
                border-color: #DADCE0;
                transform: translateY(-5px);
            }
            QTabBar::tab:hover {
                background: #F8F9FA;
                transform: translateY(-2px);
            }
        """)

        main_layout.addWidget(self.tabs)

        self.browser_area = QWebEngineView()
        main_layout.addWidget(self.browser_area)

        self.add_new_tab(QUrl("http://www.google.com"), 'Home')

        self.showMaximized()

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
