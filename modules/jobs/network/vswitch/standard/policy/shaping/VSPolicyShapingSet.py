class VSPolicyShapingSet:
    def __init__ (self, vspolicyshapings_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vspolicyshapingset_commands = list()
        for vsps in vspolicyshapings_list:
            vspolicyshaping_options = [
                f"--vswitch-name={vsps['vswitchName']}",
                f"--enabled={vsps['enabled']}" if 'enabled' in vsps else None,
                f"--avg-bandwidth={vsps['avgBandwidth']}" if 'avgBandwidth' in vsps else None,
                f"--peak-bandwidth={vsps['peakBandwidth']}"if 'peakBandwidth' in vsps else None,
                f"--burst-size={vsps['burstSize']}" if 'burstSize' in vsps else None,
            ]
            vspolicyshaping_options = [opt for opt in vspolicyshaping_options if opt is not None]
            self.vspolicyshapingset_commands.append(f"esxcli {self.quiet_command} network vswitch standard policy shaping set {' '.join(vspolicyshaping_options)}")
    
    def exec_commands(self):
        return self.vspolicyshapingset_commands