import os

class VMExport:
    def __init__(self, vmList, host_connection_dictionary):
        self.host_name = host_connection_dictionary['hostName']
        self.vmList = vmList
        self.exportString = list()
        for vm in vmList:
            vmOption = f"{host_connection_dictionary['hostOptions']} {host_connection_dictionary['hostURL']}/{vm['name']} {vm['destination']}"
            self.exportString.append(vmOption)
    
    def export_vms(self):
        for i in range (len(self.exportString)):
            try:
                print(f"> Exporting {self.vmList[i]['name']} from {self.host_name} to {self.vmList[i]['destination']}")
                os.system(f"ovftool {self.exportString[i]}")
            except:
                print ("Error occured while exporting VM!")