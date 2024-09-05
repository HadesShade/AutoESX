import os

class VMImport:
    def __init__ (self,vmList, host_connection_dictionary):
        self.host_name = host_connection_dictionary['hostName']
        self.vmList = vmList
        self.importString = list()
        for vm in vmList:
            netString = [f"--net:'{k}'='{v}'" for net in vm.get('networks', []) for k, v in net.items()]

            peripheralString = [
                f"--memorySize:*={vm['memorySize']}" if 'memorySize' in vm else '',
                f"--numberOfCpus:*={vm['cpuNumber']}" if 'cpuNumber' in vm else ''
            ] + [f"--diskSize:*,{disk['diskInstanceId']}={disk['size']}" for disk in vm.get('diskSizes', [])]

            vmOption = (
                f"{host_connection_dictionary['hostOptions']} --name={vm['name']} "
                f"--datastore={vm['datastore']} {' '.join(filter(None, netString))} "
                f"{' '.join(filter(None, peripheralString))} {vm['source']} {host_connection_dictionary['hostURL']}"
            )

            self.importString.append(vmOption)
    
        
    def import_vms(self):
        for i in range(len(self.importString)):
            try:
                print(f"> Importing {self.vmList[i]['name']} to {self.host_name}")
                os.system(f"ovftool {self.importString[i]}")
            except:
                print ("Error occured while importing VM!")
      

