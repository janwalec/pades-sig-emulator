from App_Logic import *
from PyQt5.QtWidgets import *
from gui import MyWindow
##
# @brief Klasa do zarządzania GUI aplikacji
#
# @param app_logic Instancja klasy odpowiedzialnej za logikę aplikacji (AppLogic)
class GuiManager:
    ##
    # @brief Konstruktor klasy GuiManager
    #
    # @param app_logic Obiekt logiki aplikacji, wykorzystywany do operacji biznesowych
    def __init__(self, app_logic: AppLogic):
        self.app_logic = app_logic
        self.w = MyWindow()

        self.create_all_buttons()
        self.create_all_widgets()
        self.create_all_input_fields()

    ##
    # @brief Ustawia ekran gdy klucz prywatny został znaleziony i został podany pin
    def set_screen_accepted(self):
        self.choose_file_button.show()
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

    ##
    # @brief Ustawia ekran, gdy klucz prywatny nie został znaleziony i wymagana jest generacja
    def set_screen_key_not_found(self):
        self.choose_file_button.hide()
        self.accept_button.show()
        self.generate_key_input_field.show()
        self.pin_required_to_sign_label.show()

    ##
    # @brief Ustawia ekran wymagający podania pin-u do kontynuacji, gdy klucz jest wykryty
    def set_screen_pin_required(self):
        self.choose_file_button.show()
        self.verify_button.show()
        self.decrypt_key_input_field.show()
        self.to_short_key_label.hide()
        self.pin_required_to_sign_label.show()
        self.check_signed_document_button.show()

    ##
    # @brief Tworzy wszystkie przyciski i łączy je z odpowiednimi metodami
    def create_all_buttons(self):
        ##
        # @brief Tworzy przycisk wyboru pliku i ustawia jego zachowanie
        self.choose_file_button = QPushButton("Choose file")
        self.choose_file_button.clicked.connect(self.choose_file)
        self.choose_file_button.hide()
        self.w.add_widget_to_layout(self.choose_file_button)

        ##
        # @brief Tworzy przycisk akceptacji PIN-u i ustawia jego zachowanie
        self.accept_button = QPushButton("Accept pin")
        self.accept_button.hide()
        self.accept_button.clicked.connect(self.generate_key)
        self.w.add_widget_to_layout(self.accept_button)

        ##
        # @brief Tworzy przycisk weryfikacji PIN-u i ustawia jego zachowanie
        self.verify_button = QPushButton("Verify pin")
        self.verify_button.hide()
        self.verify_button.clicked.connect(self.check_key)
        self.w.add_widget_to_layout(self.verify_button)

        ##
        # @brief Tworzy przycisk do podpisywania dokumentu i ustawia jego zachowanie
        self.sign_document_button = QPushButton("Sign document")
        self.sign_document_button.hide()
        self.sign_document_button.clicked.connect(self.sign_document)
        self.w.add_widget_to_layout(self.sign_document_button)

        ##
        # @brief Tworzy przycisk do sprawdzania podpisanego dokumentu i ustawia jego zachowanie
        self.check_signed_document_button = QPushButton("Check signed document")
        self.check_signed_document_button.hide()
        self.check_signed_document_button.clicked.connect(self.check_document)
        self.w.add_widget_to_layout(self.check_signed_document_button)

    ##
    # @brief Tworzy wszystkie pola do wprowadzania danych (input fields)
    def create_all_input_fields(self):
        ##
        # @brief Pole do wpisania PIN-u podczas generowania klucza
        self.generate_key_input_field = QLineEdit()
        self.generate_key_input_field.setPlaceholderText("Enter pin to generate key. Then click \"Accept key\"")
        self.generate_key_input_field.hide()
        self.w.add_widget_to_layout(self.generate_key_input_field)

        ##
        # @brief Pole do wpisania PIN-u podczas weryfikacji klucza
        self.decrypt_key_input_field = QLineEdit()
        self.decrypt_key_input_field.setPlaceholderText("Enter pin to verify key. Then click \"Verify key\"")
        self.decrypt_key_input_field.hide()
        self.w.add_widget_to_layout(self.decrypt_key_input_field)

    ##
    # @brief Tworzy wszystkie etykiety (labels) widoczne na GUI
    def create_all_widgets(self):
        ##
        # @brief Etykieta do wyświetlania błędów
        self.error_label = QLabel("")
        self.w.add_widget_to_layout(self.error_label)

        ##
        # @brief Etykieta pokazująca wybrany plik
        self.file_label = QLabel("")
        self.w.add_widget_to_layout(self.file_label)

        ##
        # @brief Etykieta pokazująca informację o podłączonym pendrive
        self.pendrive_label = QLabel("Waiting for plugging in pendrive")
        self.w.add_widget_to_layout(self.pendrive_label)

        ##
        # @brief Etykieta pokazująca, że klucz został znaleziony
        self.key_found_label = QLabel("")
        self.w.add_widget_to_layout(self.key_found_label)

        ##
        # @brief Etykieta informująca o zbyt krótkim pinie
        self.to_short_key_label = QLabel("Your pin is too short!")
        self.to_short_key_label.hide()
        self.w.add_widget_to_layout(self.to_short_key_label)

        ##
        # @brief Etykieta informująca o niepoprawnym PIN-ie
        self.wrong_pin_label = QLabel("Wrong pin!")
        self.wrong_pin_label.hide()
        self.w.add_widget_to_layout(self.wrong_pin_label)

        ##
        # @brief Etykieta informująca o poprawnym PIN-ie
        self.pin_ok_label = QLabel("Pin OK!")
        self.pin_ok_label.hide()
        self.w.add_widget_to_layout(self.pin_ok_label)

        ##
        # @brief Etykieta informująca o generowaniu klucza
        self.generating_key_label = QLabel("Generating key...")
        self.generating_key_label.hide()
        self.w.add_widget_to_layout(self.generating_key_label)

        ##
        # @brief Etykieta informująca, że nie można podpisać dokumentu bez klucza
        self.pin_required_to_sign_label = QLabel("You cannot sign document unless you have a key")
        self.pin_required_to_sign_label.hide()
        self.w.add_widget_to_layout(self.pin_required_to_sign_label)

    '''
    Poniżej metody powiązane z logiką aplikacji (AppLogic)
    '''

    ##
    # @brief Obsługuje zdarzenie wyboru pliku przez użytkownika
    def choose_file(self):
        ##
        # @brief Zmienna przechowująca nazwę pliku wybranego przez użytkownika
        file_name, _ = QFileDialog.getOpenFileName(self.w.window, "Choose file", "", "Wszystkie pliki (*)")
        if self.app_logic.set_file(file_name):
            self.error_label.setText("")
            self.file_label.setText(f"You have chosen: {file_name}")
            self.app_logic.pdf_to_sign = file_name
        else:
            self.file_label.setText("")
            self.error_label.setText("You have chosen the wrong file")
            self.app_logic.pdf_to_sign = None

    ##
    # @brief Wykrywa klucz i ustawia odpowiedni stan GUI
    def detect_key(self):
        if self.app_logic.detect_key():
            self.key_found_label.setText("Key found!")
            self.set_screen_pin_required()
        else:
            self.key_found_label.setText("Key not found")
            self.set_screen_key_not_found()

    ##
    # @brief Obsługuje zdarzenie wykrycia podłączonego pendrive'a
    #
    # @param pendrive Ścieżka (nazwa dysku)
    def attach_pendrive(self, pendrive):
        self.app_logic.set_pendrive(pendrive)
        self.pendrive_label.setText("Found removable device " + pendrive)

    ##
    # @brief Generuje klucz na podstawie wpisanego PIN-u i aktualizuje GUI
    def generate_key(self):
        pin = self.generate_key_input_field.text()
        if len(pin) < 5:
            self.to_short_key_label.show()
            return

        self.generating_key_label.show()
        self.app_logic.generate_key(pin)
        self.generating_key_label.hide()
        self.app_logic.detect_key()
        self.app_logic.compare_pin(pin)
        self.set_screen_accepted()

    ##
    # @brief Sprawdza poprawność PIN-u wpisanego przez użytkownika
    def check_key(self):
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

    ##
    # @brief Podpisuje wybrany dokument
    def sign_document(self):
        try:
            self.app_logic.sign_document()
            self.error_label.setText("Successfully signed")
        except ValueError as e:
            self.error_label.setText("Something went wrong")

    ##
    # @brief Sprawdza, czy dokument PDF jest poprawnie podpisany (przy użyciu klucza publicznego)
    def check_document(self):
        try:
            result = self.app_logic.check_signed_document()
            if result:
                self.error_label.setText("THIS PDF IS OK SIGNED")
            else:
                self.error_label.setText("Signature verification failed. Wrong pdf or signature")
        except ValueError as e:
            self.error_label.setText("Something went wrong")
