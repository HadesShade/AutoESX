class VSPortgroupPolicySecurityGet:
    def __init__ (self, vsportgroups_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouppolicysecurityget_commands = list()
        for vspg in vsportgroups_list:
            vsportgrouppolicysecurity_options = [
                f"--portgroup-name={vspg['name']}"
            ]
            vsportgrouppolicysecurity_options = [opt for opt in vsportgrouppolicysecurity_options if opt is not None]
            self.vsportgrouppolicysecurityget_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup policy security get {' '.join(vsportgrouppolicysecurity_options)}")
    
    def exec_commands(self):
        return self.vsportgrouppolicysecurityget_commands