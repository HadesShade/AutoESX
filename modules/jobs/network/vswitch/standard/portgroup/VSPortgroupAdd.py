class VSPortgroupAdd:
    def __init__ (self, vsportgroups_list, quiet=True):
        self.quiet_command = "--debug" if quiet == False else ''
        self.vsportgroupadd_commands = list()
        for vspg in vsportgroups_list:
            vsportgroup_options = [
                f"--portgroup-name={vspg['name']}",
                f"--vswitch-name={vspg['vsName']}"
            ]
            vsportgroup_options = [opt for opt in vsportgroup_options if opt is not None]
            self.vsportgroupadd_commands.append(f"esxcli {self.quiet_command} network vswitch standard portgroup add {' '.join(vsportgroup_options)}")
    
    def exec_commands(self):
        return self.vsportgroupadd_commands