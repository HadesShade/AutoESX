class VSPolicyShapingGet:
    def __init__ (self, vs_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vspolicyshapingget_commands = list()
        for vs in vs_list:
            vspolicyshaping_options = [
                f"--vswitch-name={vs['name']}"
            ]
            vspolicyshaping_options = [opt for opt in vspolicyshaping_options if opt is not None]
            self.vspolicyshapingget_commands.append(f"esxcli {self.quiet_command} network vswitch standard policy shaping get {' '.join(vspolicyshaping_options)}")
    
    def exec_commands(self):
        return self.vspolicyshapingget_commands