class VSRemove:
    def __init__ (self, vswitches_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsremove_commands = list()
        for vs in vswitches_list:
            vsremove_options = [
                f"--vswitch-name={vs['name']}"
            ]
            vsremove_options = [opt for opt in vsremove_options if opt is not None]
            self.vsremove_commands.append(f"esxcli {self.quiet_command} network vswitch standard remove {' '.join(vsremove_options)}")
    
    def exec_commands(self):
        return self.vsremove_commands