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

    def set_screen_accepted(self):
        # Set gui to the state in which private key is detected and user entered theirs pin
        self.choose_file_button.show()
        #self.detect_keys_button.hide()
        self.accept_button.hide()
        self.generate_key_input_field.hide()
        self.to_short_key_label.hide()
        self.verify_button.hide()
        self.decrypt_key_input_field.hide()
        self.wrong_pin_label.hide()
        self.pin_ok_label.show()
        self.key_found_label.setText("Key found!")
        self.pin_required_to_sign_label.hide()
        self.sign_document_button.show()
        self.check_signed_document_button.show()

    def set_screen_key_not_found(self):
        # Set screen to the state in which private key is not found and user needs to generate it
        self.choose_file_button.hide()
        #self.detect_keys_button.show()
        self.accept_button.show()
        self.generate_key_input_field.show()
        self.pin_required_to_sign_label.show()

    def set_screen_pin_required(self):
        # Set screen to the state in which private key is detected and user needs to pass a pin to continue
        self.choose_file_button.show()
        self.verify_button.show()
        #self.detect_keys_button.hide()
        self.decrypt_key_input_field.show()
        self.to_short_key_label.hide()
        self.pin_required_to_sign_label.show()
        self.check_signed_document_button.show()


    def create_all_buttons(self):
        # method that creates all buttons for GUI
        self.choose_file_button = QPushButton("Choose file")
        self.choose_file_button.clicked.connect(self.choose_file)
        self.choose_file_button.hide()
        self.w.add_widget_to_layout(self.choose_file_button)
        '''
        self.detect_keys_button = QPushButton("Detect keys")
        self.detect_keys_button.clicked.connect(self.detect_key)
        self.w.add_widget_to_layout(self.detect_keys_button)
        '''
        self.accept_button = QPushButton("Accept pin")
        self.accept_button.hide()
        self.accept_button.clicked.connect(self.generate_key)
        self.w.add_widget_to_layout(self.accept_button)

        self.verify_button = QPushButton("Verify pin")
        self.verify_button.hide()
        self.verify_button.clicked.connect(self.check_key)
        self.w.add_widget_to_layout(self.verify_button)

        self.sign_document_button = QPushButton("Sign document")
        self.sign_document_button.hide()
        self.sign_document_button.clicked.connect(self.sign_document)
        self.w.add_widget_to_layout(self.sign_document_button)

        self.check_signed_document_button = QPushButton("Check signed document")
        self.check_signed_document_button.hide()
        self.check_signed_document_button.clicked.connect(self.check_document)
        self.w.add_widget_to_layout(self.check_signed_document_button)

    def create_all_input_fields(self):
        # method that creates all input fields for GUI
        self.generate_key_input_field = QLineEdit()
        self.generate_key_input_field.setPlaceholderText("Enter pin to generate key. Then click \"Accept key\"")
        self.generate_key_input_field.hide()
        self.w.add_widget_to_layout(self.generate_key_input_field)

        self.decrypt_key_input_field = QLineEdit()
        self.decrypt_key_input_field.setPlaceholderText("Enter pin to verify key. Then click \"Verify key\"")
        self.decrypt_key_input_field.hide()
        self.w.add_widget_to_layout(self.decrypt_key_input_field)

    def create_all_widgets(self):
        # method that creates all labels displayed for GUI
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

        self.wrong_pin_label = QLabel("Wrong pin!")
        self.wrong_pin_label.hide()
        self.w.add_widget_to_layout(self.wrong_pin_label)

        self.pin_ok_label = QLabel("Pin OK!")
        self.pin_ok_label.hide()
        self.w.add_widget_to_layout(self.pin_ok_label)

        self.generating_key_label = QLabel("Generating key...")
        self.generating_key_label.hide()
        self.w.add_widget_to_layout(self.generating_key_label)

        self.pin_required_to_sign_label = QLabel("You cannot sign document unless you have a key")
        self.pin_required_to_sign_label.hide()
        self.w.add_widget_to_layout(self.pin_required_to_sign_label)

    '''
    App logic references below
    '''

    def choose_file(self):
        # method attached to "Choose file" button
        file_name, _ = QFileDialog.getOpenFileName(self.w.window, "Choose file", "", "Wszystkie pliki (*)")
        if self.app_logic.set_file(file_name):
            self.error_label.setText("")
            self.file_label.setText(f"You have chosen: {file_name}")
            self.app_logic.pdf_to_sign = file_name
        else:
            self.file_label.setText("")
            self.error_label.setText("You have chosen the wrong file")
            self.app_logic.pdf_to_sign = None

    def detect_key(self):
        # detects key and sets proper information
        if self.app_logic.detect_key():
            self.key_found_label.setText("Key found!")
            self.set_screen_pin_required()
        else:
            self.key_found_label.setText("Key not found")
            self.set_screen_key_not_found()

    def attach_pendrive(self, pendrive):
        # found removable device
        self.app_logic.set_pendrive(pendrive)
        self.pendrive_label.setText("Found removable device " + pendrive)

    def generate_key(self):
        # if user doesn't have a key on theirs removable device, it generates a new one based on theirs pin
        pin = self.generate_key_input_field.text()
        if len(pin) < 5:
            self.to_short_key_label.show()
            return

        self.generating_key_label.show() # inform that key is generating
        self.app_logic.generate_key(pin)
        self.generating_key_label.hide()
        self.app_logic.detect_key()
        self.app_logic.compare_pin(pin) # just to calm the app logic down
        self.set_screen_accepted()

    def check_key(self):
        # checks if user knows pin for theirs private key
        pin = self.decrypt_key_input_field.text()
        if len(pin) < 5:
            self.to_short_key_label.show()
            return
        self.to_short_key_label.hide()
        try:
            self.app_logic.compare_pin(pin)
            self.set_screen_accepted()
        except ValueError as e:
            self.wrong_pin_label.show()

    def sign_document(self):
        # signs chosen file
        try:
            self.app_logic.sign_document()
            self.error_label.setText("Successfully signed")
        except ValueError as e:
            self.error_label.setText("Something went wrong")

    def check_document(self):
        # checks if pdf is signed by known user
        try:
            result = self.app_logic.check_signed_document()
            if(result):
                self.error_label.setText("THIS PDF IS OK SIGNED")
            else:
                self.error_label.setText("Signature veryfication failed. Wrong pdf or signature")
        except ValueError as e:
            self.error_label.setText("Something went wrong")

