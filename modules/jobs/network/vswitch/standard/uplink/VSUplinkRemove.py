class VSUplinkRemove:
    def __init__ (self, vsuplinks_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsuplinkremove_commands = list()
        for vsup in vsuplinks_list:
            vsuplink_options = [
                f"--uplink-name={vsup['name']}",
                f"--vswitch-name={vsup['vswitchName']}"
            ]
            vsuplink_options = [opt for opt in vsuplink_options if opt is not None]
            self.vsuplinkremove_commands.append(f"esxcli {self.quiet_command} network vswitch standard uplink remove {' '.join(vsuplink_options)}")
    
    def exec_commands(self):
        return self.vsuplinkremove_commands