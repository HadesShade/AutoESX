import platform
import shutil

class Initialize:
    def __init__(self):
        self.os_type = platform.system()
        self.architecture = platform.machine()
    
    def check_ovftool(self):
        if shutil.which("ovftool") is None:
            print ("WARNING: OVFTool is not installed. Functionality may be limited.")
        