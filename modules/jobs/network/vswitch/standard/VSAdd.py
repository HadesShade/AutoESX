class VSAdd:
    def __init__ (self, vswitches_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsadd_commands = list()
        for vs in vswitches_list:
            vsadd_options = [
                f"--vswitch-name={vs['name']}",
                f"--ports={vs['portNumber']}" if 'portNumber' in vs and vs['portNumber'] is not None else None,
            ]
            vsadd_options = [opt for opt in vsadd_options if opt is not None]
            self.vsadd_commands.append(f"esxcli {self.quiet_command} network vswitch standard add {' '.join(vsadd_options)}")

    def exec_commands(self):
        return self.vsadd_commands