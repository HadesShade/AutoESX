class VSPolicySecuritySet:
    def __init__ (self, vspolicysecurities_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vspolicysecurityset_commands = list()
        for vsps in vspolicysecurities_list:
            vspolicysecurity_options = [
                f"--vswitch-name={vsps['vswitchName']}",
                f"--allow-forged-transmits={vsps['allowForgedTransmits']}"  if 'allowForgedTransmits' in vsps else None,
                f"--allow-mac-change={vsps['allowMacChange']}" if 'allowMacChange' in vsps else None,
                f"--allow-promiscuous={vsps['allowPromiscuous']}" if 'allowPromiscuous' in vsps else None
            ]
            vspolicysecurity_options = [opt for opt in vspolicysecurity_options if opt is not None]
            self.vspolicysecurityset_commands.append(f"esxcli {self.quiet_command} network vswitch standard policy security set {' '.join(vspolicysecurity_options)}")
    
    def exec_commands(self):
        return self.vspolicysecurityset_commands