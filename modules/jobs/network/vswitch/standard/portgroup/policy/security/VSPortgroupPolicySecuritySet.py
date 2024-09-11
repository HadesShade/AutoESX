class VSPortgroupPolicySecuritySet:
    def __init__ (self, vsportgrouppolicysecurities_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgrouppolicysecurityset_commands = list()
        for vspgps in vsportgrouppolicysecurities_list:
            vsportgrouppolicysecurity_options = [
                f"--portgroup-name={vspgps['portgroupName']}",
                f"--use-vswitch" if 'useVswitch' in vspgps and vspgps['useVswitch'] == True else None,
                f"--allow-forged-transmits={vspgps['allowForgedTransmits']}"  if 'allowForgedTransmits' in vspgps else None,
                f"--allow-mac-change={vspgps['allowMacChange']}" if 'allowMacChange' in vspgps else None,
                f"--allow-promiscuous={vspgps['allowPromiscuous']}" if 'allowPromiscuous' in vspgps else None
            ]
            vsportgrouppolicysecurity_options = [opt for opt in vsportgrouppolicysecurity_options if opt is not None]
            self.vsportgrouppolicysecurityset_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup policy security set {' '.join(vsportgrouppolicysecurity_options)}")
    
    def exec_commands(self):
        return self.vsportgrouppolicysecurityset_commands