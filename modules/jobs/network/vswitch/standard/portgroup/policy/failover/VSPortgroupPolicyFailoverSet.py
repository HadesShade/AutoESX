class VSPortgroupPolicyFailoverSet:
    def __init__ (self, vsportgrouppolicyfailovers_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouppolicyfailoverset_commands = list()
        for vspgpf in vsportgrouppolicyfailovers_list:
            vsportgrouppolicyfailover_options = [
                f"--portgroup-name={vspgpf['portgroupName']}",
                f"--active-uplinks={','.join(vspgpf['activeUplinks'])}" if 'activeUplinks' in vspgpf else None,
                f"--failback={vspgpf['failback']}" if 'failback' in vspgpf else None,
                f"--failure-detection={vspgpf['failureDetection']}" if 'failureDetection' in vspgpf else None,
                f"--load-balancing={vspgpf['loadBalancing']}" if 'loadBalancing' in vspgpf else None,
                f"--notify-switches={vspgpf['notifySwitches']}" if 'notifySwitches' in vspgpf else None,
                f"--standby-uplinks={','.join(vspgpf['standbyUplinks'])}" if'standbyUplinks' in vspgpf else None,
                f"--use-vswitch" if 'useVswitch' in vspgpf and vspgpf['useVswitch'] == True else None
            ]
                
            vsportgrouppolicyfailover_options = [opt for opt in vsportgrouppolicyfailover_options if opt is not None]
            self.vsportgrouppolicyfailoverset_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup policy failover set {' '.join(vsportgrouppolicyfailover_options)}")
    
    def exec_commands(self):
        return self.vsportgrouppolicyfailoverset_commands