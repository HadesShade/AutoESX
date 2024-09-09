import yaml
import argparse
import sys
from modules.host import Host
from modules.group import Group
from modules.jobs.VM.VMImport import VMImport
from modules.jobs.VM.VMExport import VMExport
from modules.initialize import Initialize
from modules.jobs.network.vswitch.standard.VSAdd import VSAdd
from modules.jobs.network.vswitch.standard.VSRemove import VSRemove
from modules.jobs.network.vswitch.standard.VSSet import VSSet
from modules.jobs.network.vswitch.standard.VSList import VSList

class AutoESX:
    def __init__(self, inventoryData, jobData):
        self.hosts = self._initialize_hosts(inventoryData.get('hosts', []))
        self.groups = self._initialize_groups(inventoryData.get('groups', []))
        self.jobs = self._initialize_jobs(jobData)
        self.init = Initialize()
        self.init.check_ovftool()

    def _initialize_hosts(self, hosts_data):
        if not hosts_data:
            print("Inventory should have 'hosts' definition!")
            sys.exit(0)
        
        return [
            {host["name"]: Host(
                name=host['name'],
                type=host['type'],
                address=host['serverData']['address'],
                username=host['serverData']['username'],
                password=host['serverData']['password'],
                httpsPort=host['serverData']['httpsPort'],
                SSLVerify=host['serverData'].get('SSLVerify', True),
                acceptAllEulas=host['serverData'].get('acceptAllEulas', False),
            )}
            for host in hosts_data
        ]

    def _initialize_groups(self, groups_data):
        return [
            {group["name"]: Group(group["name"], group["hosts"])}
            for group in groups_data
        ]

    def _initialize_jobs(self, jobs_data):
        jobs = []
        for job in jobs_data:
            job_dict = {
                "description": job["description"],
                "task": job["task"],
                "binaryOpts": {
                    "quiet": job["quiet"] if 'quiet' in job else True
                }
            }
            if "hosts" in job:
                job_dict["hosts"] = job["hosts"]
            elif "groups" in job:
                job_dict["groups"] = job["groups"]
            else:
                print("Either 'hosts' or 'groups' must be defined for a job!")
                sys.exit(0)
            jobs.append(job_dict)
        return jobs

    def run_jobs(self):
        for job in self.jobs:
            print(f"*************** Running job: {job['description']} ***************")
            task_type = job["task"]["type"]
            target_hosts = job.get("hosts", [])
            if "groups" in job:
                for group in job["groups"]:
                    target_group = next(g[group] for g in self.groups if group in g)
                    target_hosts.extend(target_group.hosts)

            for host in target_hosts:
                host_object = next(h[host] for h in self.hosts if host in h)
                if task_type == "VMImport":
                    vm_import = VMImport(job["task"]["virtualMachines"], host_object.connection_dictionary(), job['binaryOpts'])
                    vm_import.import_vms()
                elif task_type == "VMExport":
                    vm_export = VMExport(job["task"]["virtualMachines"], host_object.connection_dictionary(), job['binaryOpts'])
                    vm_export.export_vms()
                elif task_type == "VSAdd":
                    vs_add = VSAdd(job["task"]["vSwitches"], quiet=job['binaryOpts']['quiet'])
                    for command in vs_add.exec_commands():
                        print(host_object.ssh.ssh_command_execution(command))
                    host_object.ssh.ssh.close()
                elif task_type == "VSRemove":
                    vs_remove = VSRemove(job["task"]["vSwitches"], quiet=job['binaryOpts']['quiet'])
                    for command in vs_remove.exec_commands():
                        print(host_object.ssh.ssh_command_execution(command))
                    host_object.ssh.ssh.close()
                elif task_type == "VSSet":
                    vs_set = VSSet(job["task"]["vSwitches"], quiet=job['binaryOpts']['quiet'])
                    for command in vs_set.exec_commands():
                        print(host_object.ssh.ssh_command_execution(command))
                    host_object.ssh.ssh.close()
                elif task_type == "VSList":
                    vs_list = VSList(vswitches_list=job["task"]["vSwitches"] if "vSwitches" in job["task"] else [], quiet=job['binaryOpts']['quiet'])
                    for command in vs_list.exec_commands():
                        print(host_object.ssh.ssh_command_execution(command))
                    host_object.ssh.ssh.close()
                else:
                    print("Unknown task type!")
                    sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate VMWare ESXi processes")
    parser.add_argument('--inventory-file', '-i', required=True, type=str, help='Path to the inventory file')
    parser.add_argument('--job-file', '-j', required=True, type=str, help='Path to the job file')
    args = parser.parse_args()

    try:
        with open(args.inventory_file, 'r') as inventory_yaml, open(args.job_file, 'r') as job_yaml:
            inventory = yaml.safe_load(inventory_yaml)
            job = yaml.safe_load(job_yaml)
            autoesx = AutoESX(inventory, job)
            autoesx.run_jobs()
    except Exception:
        print("An error occurred! Exiting...")
        sys.exit(0)
