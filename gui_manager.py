from App_Logic import *

from PyQt5.QtWidgets import *
from gui import MyWindow

class GuiManager:
    def __init__(self, app_logic: AppLogic):
        self.app_logic = app_logic
        self.w = MyWindow()

        self.create_all_buttons()
        self.create_all_widgets()
        self.create_all_input_fields()


    def create_all_buttons(self):
        self.choose_file_button = QPushButton("Choose file")
        self.choose_file_button.clicked.connect(self.choose_file)
        self.choose_file_button.hide()
        self.w.add_widget_to_layout(self.choose_file_button)

        self.detect_keys_button = QPushButton("Detect keys")
        self.detect_keys_button.clicked.connect(self.detect_key)
        self.w.add_widget_to_layout(self.detect_keys_button)

        self.accept_button = QPushButton("Accept key")
        self.accept_button.hide()
        self.accept_button.clicked.connect(self.generate_key)
        self.w.add_widget_to_layout(self.accept_button)

    def create_all_input_fields(self):
        self.text_input_field = QLineEdit()
        self.text_input_field.setPlaceholderText("Enter pin to generate key. Then click \"Accept key\"")
        self.text_input_field.hide()
        self.w.add_widget_to_layout(self.text_input_field)

    def create_all_widgets(self):
        self.error_label = QLabel("")
        self.w.add_widget_to_layout(self.error_label)

        self.file_label = QLabel("")
        self.w.add_widget_to_layout(self.file_label)

        self.pendrive_label = QLabel("Waiting for plugging in pendrive")
        self.w.add_widget_to_layout(self.pendrive_label)

        self.key_found_label = QLabel("")
        self.w.add_widget_to_layout(self.key_found_label)

        self.to_short_key_label = QLabel("Your key is to short!")
        self.to_short_key_label.hide()
        self.w.add_widget_to_layout(self.to_short_key_label)

    '''
    logic references
    '''

    def choose_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self.w.window, "Choose file", "", "Wszystkie pliki (*)")
        if self.app_logic.set_file(file_name):
            self.error_label.setText("")
            self.file_label.setText(f"You have chosen: {file_name}")
        else:
            self.file_label.setText("")
            self.error_label.setText("You have chosen the wrong file")

    def detect_key(self):
        if self.app_logic.detect_key():
            self.key_found_label.setText("Key found!")
            self.detect_keys_button.hide()
            self.key_found_label.hide()
            self.accept_button.hide()
            self.choose_file_button.show()
            self.text_input_field.hide()

        else:
            self.key_found_label.setText("Key not found")
            self.text_input_field.show()
            self.accept_button.show()


    def attach_pendrive(self, pendrive):
        self.app_logic.set_pendrive(pendrive)
        self.pendrive_label.setText("Found removable device " + pendrive)

    def generate_key(self):
        key_to_generate = self.text_input_field.text()
        if len(key_to_generate) < 5:
            self.to_short_key_label.show()
            return
        self.detect_keys_button.hide()
        self.to_short_key_label.hide()
        self.text_input_field.hide()
        self.accept_button.hide()
        self.choose_file_button.show()
        self.app_logic.generate_key(key_to_generate)




