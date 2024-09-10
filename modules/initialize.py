import platform
import shutil

class Initialize:
    def __init__(self):
        self.os_type = platform.system()
        self.architecture = platform.machine()
    
    def check_ovftool(self):
        if shutil.which("ovftool") is None:
            print ("WARNING: OVFTool is not installed. VM Import and Export will not work.")
            print ("You can download OVFTool from https://developer.broadcom.com/tools/open-virtualization-format-ovf-tool/latest")
    
    def check_ssh(self):
        if shutil.which("ssh") is None:
            print ("WARNING: SSH is not installed. Only VM Import and Export will work.")
        