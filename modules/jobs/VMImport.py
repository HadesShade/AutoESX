import os

class VMImport:
    def __init__ (self,vmList, host_connection_dictionary):
        self.host_name = host_connection_dictionary['hostName']
        self.vmList = vmList
        self.importString = list()
        for vm in vmList:
            netString = list()
            for net in vm['networks']:
                for k,v in net.items():
                    netString.append(f"--net:'{k}'='{v}'")
            vmOption = f"{host_connection_dictionary['hostOptions']} --name={vm['name']} --datastore={vm['datastore']} {' '.join(netString)} {vm['source']} {host_connection_dictionary['hostURL']}"
            self.importString.append(vmOption)
    
        
    def import_vms(self):
        for i in range(len(self.importString)):
            try:
                print(f"---------- Importing {self.vmList[i]['name']} to {self.host_name} ----------")
                os.system(f"ovftool {self.importString[i]}")
            except:
                print ("Error occured while importing VM!")
      

