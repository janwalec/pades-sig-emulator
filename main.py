from gui_manager import *
from pendrive_manager import *


pm = PendriveManager()
pm.detect_new_drives()
plugged = pm.get_search()
al = AppLogic()

gm = GuiManager(al)
gm.w.start()
gm.attach_pendrive(plugged)
gm.detect_key()


gm.w.quit()
