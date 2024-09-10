class VSPortgroupList:
    def __init__ (self, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouplist_commands = list()
        self.vsportgrouplist_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup list")
    
    def exec_commands(self):
        return self.vsportgrouplist_commands