import psutil
import time

##
# @brief Klasa do wykrywania i zarządzania podłączonymi pendrive'ami (urządzeniami przenośnymi)
class PendriveManager:
    ##
    # @brief Statyczna metoda wyszukująca wszystkie urządzenia oznaczone jako 'removable'
    # @return list Lista ścieżek urządzeń przenośnych (pendrive)
    @staticmethod
    def search_for_removable_drives():
        rem = []
        for dev in psutil.disk_partitions():
            if 'removable' in dev.opts:
                rem.append(dev.device)
        return rem

    ##
    # @brief Wykrywa nowe podłączone urządzenia przenośne po uruchomieniu aplikacji
    #
    # Metoda monitoruje system, aż zostanie podłączony nowy pendrive.
    # Po wykryciu nowego urządzenia zwraca jego ścieżkę, która jest zachowywana w GuiManager i AppLogic
    def detect_new_drives(self):
        print("Searching for new drives... Plug in your removable device to start application")
        drives_before = set(self.search_for_removable_drives())
        while True:
            time.sleep(1)
            drives_after = set(self.search_for_removable_drives())
            if drives_after - drives_before:
                self.drives_path = (drives_after - drives_before).pop()
                print("Found: " + self.drives_path)
                return

    ##
    # @brief Resetuje wewnętrzne przechowywanie ścieżki wykrytego pendrive'a
    def reset_search(self):
        self.drives_path = None

    ##
    # @brief Zwraca ścieżkę ostatnio wykrytego pendrive'a
    def get_search(self):
        return self.drives_path

    ##
    # @brief Konstruktor klasy inicjalizujący zmienną przechowującą ścieżkę pendrive'a
    def __init__(self):
        self.drives_path = None
