class VSPolicySecurityGet:
    def __init__ (self, vs_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vspolicysecurityget_commands = list()
        for vs in vs_list:
            vspolicysecurity_options = [
                f"--vswitch-name={vs['name']}"
            ]
            vspolicysecurity_options = [opt for opt in vspolicysecurity_options if opt is not None]
            self.vspolicysecurityget_commands.append(f"esxcli {self.quiet_command} network vswitch standard policy security get {' '.join(vspolicysecurity_options)}")
    
    def exec_commands(self):
        return self.vspolicysecurityget_commands