from PyQt5.QtWidgets import *
import sys


def create_window(w: int) -> QWidget:
    window = QWidget()
    window.setWindowTitle("Project BSK")
    window.resize(w, w)
    return window


def create_layout() -> QVBoxLayout:
    layout = QVBoxLayout()
    return layout


class MyWindow:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = create_window(500)
        self.layout = create_layout()
        self.window.setLayout(self.layout)

    def add_widget_to_layout(self, widget: QWidget):
        self.layout.addWidget(widget)

    def start(self):
        self.window.show()

    def quit(self):
        sys.exit(self.app.exec_())

