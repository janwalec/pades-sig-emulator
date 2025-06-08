import psutil
# https://psutil.readthedocs.io/en/latest/index.html#psutil.disk_partitions
import time

class PendriveManager:
    @staticmethod
    def search_for_removable_drives():
        # return list of devices that got 'removable' tag
        rem = []
        for dev in psutil.disk_partitions():
            if 'removable' in dev.opts:
                rem.append(dev.device)
        return rem

    def detect_new_drives(self):
        # searches for pendrive, stops if one is connected (after app was run)
        print("Searching for new drives... Plug in your removable device to start aplication")
        drives_before = set(self.search_for_removable_drives())
        while 1:
            time.sleep(1)
            drives_after = set(self.search_for_removable_drives())
            if drives_after - drives_before:
                self.drives_path = (drives_after - drives_before).pop()
                print("Found: " + self.drives_path)
                return

    def reset_search(self):
        self.drives_path = None

    def get_search(self):
        return self.drives_path

    def __init__(self):
        self.drives_path = None



