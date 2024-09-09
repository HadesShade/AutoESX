class VSList:
    def __init__ (self, vswitches_list=[], quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vslist_commands = list()
        if len(vswitches_list) == 0:
            self.vslist_commands.append("esxcli network vswitch standard list")

        else:
            for vs in vswitches_list:
                vslist_options = [
                    f"--vswitch-name = {vs['name']}" if 'name' in vs and vs['name'] is not None else None
                ]
                vslist_options = [opt for opt in vslist_options if opt is not None]
                self.vslist_commands.append(f"esxcli {self.quiet_command} network vswitch standard list {' '.join(vslist_options)}")
    
    def exec_commands(self):
        return self.vslist_commands