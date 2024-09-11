class VSPortgroupPolicyFailoverGet:
    def __init__ (self, vsportgroups_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouppolicyfailoverget_commands = list()
        for vspg in vsportgroups_list:
            vsportgrouppolicyfailover_options = [
                f"--portgroup-name={vspg['name']}"
            ]
            vsportgrouppolicyfailover_options = [opt for opt in vsportgrouppolicyfailover_options if opt is not None]
            self.vsportgrouppolicyfailoverget_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup policy failover get {' '.join(vsportgrouppolicyfailover_options)}")
    
    def exec_commands(self):
        return self.vsportgrouppolicyfailoverget_commands