class VSPolicyFailoverGet:
    def __init__ (self, vs_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vspolicyfailoverget_commands = list()
        for vs in vs_list:
            vspolicyfailover_options = [
                f"--vswitch-name={vs['name']}"
            ]
            vspolicyfailover_options = [opt for opt in vspolicyfailover_options if opt is not None]
            self.vspolicyfailoverget_commands.append(f"esxcli {self.quiet_command} network vswitch standard policy failover get {' '.join(vspolicyfailover_options)}")
    
    def exec_commands(self):
        return self.vspolicyfailoverget_commands