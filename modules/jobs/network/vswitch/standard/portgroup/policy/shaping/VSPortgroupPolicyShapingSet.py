class VSPortgroupPolicyShapingSet:
    def __init__ (self, vsportgrouppolicyshapings_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouppolicyshapingset_commands = list()
        for vspgps in vsportgrouppolicyshapings_list:
            vsportgrouppolicyshaping_options = [
                f"--portgroup-name={vspgps['portgroupName']}",
                f"--enabled={vspgps['enabled']}" if 'enabled' in vspgps else None,
                f"--use-vswitch" if 'useVswitch' in vspgps and vspgps['useVswitch'] == True else None,
                f"--avg-bandwidth={vspgps['avgBandwidth']}" if 'avgBandwidth' in vspgps else None,
                f"--peak-bandwidth={vspgps['peakBandwidth']}"if 'peakBandwidth' in vspgps else None,
                f"--burst-size={vspgps['burstSize']}" if 'burstSize' in vspgps else None,
            ]
            vsportgrouppolicyshaping_options = [opt for opt in vsportgrouppolicyshaping_options if opt is not None]
            self.vsportgrouppolicyshapingset_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup policy shaping set {' '.join(vsportgrouppolicyshaping_options)}")
    
    def exec_commands(self):
        return self.vsportgrouppolicyshapingset_commands