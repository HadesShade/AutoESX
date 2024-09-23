import os

class VMImport:
    def __init__ (self,vmList, host_connection_dictionary, jobBinaryOpts):
        self.host_name = host_connection_dictionary['hostName']
        self.jobBinaryOpts = jobBinaryOpts
        self.vmList = vmList
        self.importString = list()
        for vm in vmList:
            netString = [f"--net:'{k}'='{v}'" for net in vm.get('networks', []) for k, v in net.items()]

            peripheralString = [
                f"--memorySize:*={vm['memorySize']}" if 'memorySize' in vm else '',
                f"--numberOfCpus:*={vm['cpuNumber']}" if 'cpuNumber' in vm else ''
            ] + [f"--diskSize:*,{disk['diskInstanceId']}={disk['size']}" for disk in vm.get('diskSizes', [])]

            binaryOptsString = [
                "--quiet" if self.jobBinaryOpts['quiet'] == True else '',
                "--overwrite" if ('overwrite' in vm and vm['overwrite'] == True) else '',
                "--powerOn" if ('powerOn' in vm and vm['powerOn'] == True) else '',
                "--powerOffSource" if('powerOffSource' in vm and vm['powerOffSource'] == True) else '',
                "--powerOffTarget" if('powerOffTarget' in vm and vm['powerOffTarget'] == True) else ''
            ]

            vmOption = (
                f"{host_connection_dictionary['hostOptions']} --name={vm['name']} "
                f"--datastore={vm['datastore']} {' '.join(filter(None, netString))} {' '.join(filter(None, binaryOptsString))} "
                f"{' '.join(filter(None, peripheralString))} {vm['source']} {host_connection_dictionary['hostURL']}"
            )

            self.importString.append(vmOption)
    
        
    def import_vms(self):
        for i in range(len(self.importString)):
            try:
                os.system(f"ovftool {self.importString[i]}")
            except:
                print ("Error occured while importing VM!")
      

