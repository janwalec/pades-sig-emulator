from PyQt5.QtWidgets import *
import sys

##
# @brief Tworzy główne okno aplikacji o zadanej szerokości i wysokości (kwadrat)
# @param w Rozmiar okna (szerokość i wysokość)
# @return QWidget Obiekt okna QWidget
def create_window(w: int) -> QWidget:
    window = QWidget()
    window.setWindowTitle("Project BSK")
    window.resize(w, w)
    return window

##
# @brief Tworzy pionowy layout (QVBoxLayout)
# @return QVBoxLayout Obiekt layoutu
def create_layout() -> QVBoxLayout:
    layout = QVBoxLayout()
    return layout

##
# @brief Klasa zarządzająca głównym oknem aplikacji i jej layoutem
class MyWindow:

    ##
    # @brief Konstruktor klasy MyWindow - tworzy aplikację, okno i layout
    def __init__(self):
        self.app = QApplication(sys.argv)  ## Obiekt aplikacji Qt
        self.window = create_window(500)  ## Główne okno aplikacji
        self.layout = create_layout()     ## Layout okna
        self.window.setLayout(self.layout)

    ##
    # @brief Dodaje widget do głównego layoutu okna
    # @param widget Obiekt QWidget, który ma zostać dodany do layoutu
    def add_widget_to_layout(self, widget: QWidget):
        self.layout.addWidget(widget)

    ##
    # @brief Wyświetla okno aplikacji
    def start(self):
        self.window.show()

    ##
    # @brief Uruchamia główną pętlę aplikacji i zamyka ją po zakończeniu
    def quit(self):
        sys.exit(self.app.exec_())
