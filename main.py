import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import *


class Zephyr(QMainWindow):

    def __init__(self):
        super().__init__()

        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

        
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: 
                border-radius: 10px;
                padding: 10px;
                margin: 2px;
                min-height: 50px;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: 
            }
            QTabBar::tab:hover {
                background: 
            }
        """)

        
        container_widget = QWidget()
        container_layout = QVBoxLayout()
        container_widget.setLayout(container_layout)

        
        container_layout.addWidget(self.tabs)

        
        navbar = QToolBar()
        container_layout.addWidget(navbar)

        
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        navbar.addAction(back_btn)

        
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        navbar.addAction(forward_btn)

        
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        navbar.addAction(reload_btn)

        
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        
        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(self.add_new_tab)
        navbar.addAction(new_tab_btn)

        
        self.setCentralWidget(container_widget)

        
        self.add_new_tab(QUrl("http://www.google.com"), 'Home')

        self.showMaximized()

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None or isinstance(qurl, bool):
            qurl = QUrl("http://www.google.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        browser.urlChanged.connect(self.update_url_bar)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

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
