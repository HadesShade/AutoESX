class VMNetworkList:
    def __init__ (self, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vmnetworklist_commands = [f"esxcli {self.quiet_command} network vm list"]
    
    def exec_commands(self):
        return self.vmnetworklist_commands