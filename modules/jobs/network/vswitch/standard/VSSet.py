class VSSet:
    def __init__ (self, vswitches_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsset_commands = list()
        for vs in vswitches_list:
            vsset_options = [
                f"--vswitch-name={vs['name']}",
                f"--mtu={vs['mtu']}" if 'mtu' in vs and vs['mtu'] is not None else None,
                f"--cdp-status={vs['cdpStatus']}" if 'cdpStatus' in vs and vs['cdpStatus'] is not None else None
            ]
            vsset_options = [opt for opt in vsset_options if opt is not None]
            self.vsset_commands.append(f"esxcli {self.quiet_command} network vswitch standard set {' '.join(vsset_options)}")

    def exec_commands(self):
        return self.vsset_commands