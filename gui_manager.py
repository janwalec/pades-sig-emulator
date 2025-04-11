from PyQt5.QtWidgets import *
import sys
from gui import *

def check_if_pdf(file_name):
    # check if name of the file ends with .pdf
    return file_name.lower().endswith(".pdf")

def create_push_button(title, method_to_run) -> QPushButton:
    # universal method for creating buttons
    button = QPushButton(title)
    button.clicked.connect(method_to_run)
    return button


class GuiManager:
    def __init__(self):
        self.w = MyWindow()
        self.file_chosen = None
        self.buttons = []   # list of tuples (button, name) -- buttons added to layout
        self.widgets = []   # list of tuples (widget, name) -- tuples added to layout

        self.create_all_buttons()
        self.create_all_widgets()


    def create_all_buttons(self):
        # create all buttons here, that should be displayed in the window
        b1 = create_push_button("Choose file", self.choose_file)
        self.buttons.append((b1, "choose_file"))    # append it for later use
        self.w.add_widget_to_layout(b1)             # display it in main window


    def create_all_widgets(self):
        error_label = QLabel("")
        self.widgets.append((error_label, "error_label"))   # append it for later use
        self.w.add_widget_to_layout(error_label)            # display it in main window

        file_label = QLabel("")
        self.widgets.append((file_label, "file_label"))
        self.w.add_widget_to_layout(file_label)

    def choose_file(self):
        # opens dialog window for user
        file_name, _ = QFileDialog.getOpenFileName(self.w.window, "Choose file", "", "Wszystkie pliki (*)")
        self.parse_file(file_name)

    def parse_file(self, filename):
        # parses if file exists and if it is .pdf

        error_label = next((widget for widget, name in self.widgets if name == "error_label"), None) # find error label in case of modification
        file_label  = next((widget for widget, name in self.widgets if name == "file_label"), None)

        if filename and check_if_pdf(filename): # correct, file is ok
            self.file_chosen = filename
            if error_label and file_label:
                error_label.setText("")
                file_label.setText("You have chosen: " + filename)

        else:
            self.file_chosen = None
            if error_label and file_label:
                error_label.setText("You have chosen the wrong file")
                file_label.setText("")

gm = GuiManager()

gm.w.start()
gm.w.quit()