class VMPortList:
    def __init__ (self, worldids_list=[], quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vmportlist_commands = list()
        for w in worldids_list:
            vmportlist_options = [
                f"--world-id={w}"
            ]
            vmportlist_options = [opt for opt in vmportlist_options if opt is not None]
            self.vmportlist_commands.append(f"esxcli {self.quiet_command} network vm port list {' '.join(vmportlist_options)}")
    
    def exec_commands(self):
        return self.vmportlist_commands