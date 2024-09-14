class VSPolicyFailoverSet:
    def __init__ (self, vspolicyfailovers_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vspolicyfailoverset_commands = list()
        for vs in vspolicyfailovers_list:
            vspolicyfailover_options = [
                f"--vswitch-name={vs['vswitchName']}",
                f"--active-uplinks={','.join(vs['activeUplinks'])}" if 'activeUplinks' in vs else None,
                f"--failback={vs['failback']}" if 'failback' in vs else None,
                 f"--failure-detection={vs['failureDetection']}" if 'failureDetection' in vs else None,
                f"--load-balancing={vs['loadBalancing']}" if 'loadBalancing' in vs else None,
                f"--notify-switches={vs['notifySwitches']}" if 'notifySwitches' in vs else None,
                f"--standby-uplinks={','.join(vs['standbyUplinks'])}" if'standbyUplinks' in vs else None
            ]
                
            vspolicyfailover_options = [opt for opt in vspolicyfailover_options if opt is not None]
            self.vspolicyfailoverset_commands.append(f"esxcli {self.quiet_command} network vswitch standard policy failover set {' '.join(vspolicyfailover_options)}")
    
    def exec_commands(self):
        return self.vspolicyfailoverset_commands