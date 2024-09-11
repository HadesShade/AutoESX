class VSPortgroupPolicyShapingGet:
    def __init__ (self, vsportgroups_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouppolicyshapingget_commands = list()
        for vspg in vsportgroups_list:
            vsportgrouppolicyshaping_options = [
                f"--portgroup-name={vspg['name']}"
            ]
            vsportgrouppolicyshaping_options = [opt for opt in vsportgrouppolicyshaping_options if opt is not None]
            self.vsportgrouppolicyshapingget_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup policy shaping get {' '.join(vsportgrouppolicyshaping_options)}")
    
    def exec_commands(self):
        return self.vsportgrouppolicyshapingget_commands