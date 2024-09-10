class VSPortgroupSet:
    def __init__ (self, vsportgroups_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgroupset_commands = list()
        for vspg in vsportgroups_list:
            vsportgroup_options = [
                f"--portgroup-name={vspg['name']}",
                f"--vlan-id={vspg['vlanId']}"
            ]
            vsportgroup_options = [opt for opt in vsportgroup_options if opt is not None]
            self.vsportgroupset_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup set {' '.join(vsportgroup_options)}")
    
    def exec_commands(self):
        return self.vsportgroupset_commands