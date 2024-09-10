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
from modules.jobs.network.vswitch.standard.uplink.VSUplinkAdd import VSUplinkAdd
from modules.jobs.network.vswitch.standard.uplink.VSUplinkRemove import VSUplinkRemove


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
    
    def _exec_commands(self, task_instance, host_object):
            for command in task_instance.exec_commands():
                print(host_object.ssh.ssh_command_execution(command))
            host_object.ssh.ssh.close()

    def run_jobs(self):
        task_handlers = {
            "VMImport": lambda job, host_object: VMImport(job["task"]["virtualMachines"], host_object.connection_dictionary(), job['binaryOpts']).import_vms(),
            "VMExport": lambda job, host_object: VMExport(job["task"]["virtualMachines"], host_object.connection_dictionary(), job['binaryOpts']).export_vms(),
            "VSAdd": lambda job, host_object: self._exec_commands(VSAdd(job["task"]["vSwitches"], quiet=job['binaryOpts']['quiet']), host_object),
            "VSRemove": lambda job, host_object: self._exec_commands(VSRemove(job["task"]["vSwitches"], quiet=job['binaryOpts']['quiet']), host_object),
            "VSSet": lambda job, host_object: self._exec_commands(VSSet(job["task"]["vSwitches"], quiet=job['binaryOpts']['quiet']), host_object),
            "VSList": lambda job, host_object: self._exec_commands(VSList(vswitches_list=job["task"].get("vSwitches", []), quiet=job['binaryOpts']['quiet']), host_object),
            "VSUplinkAdd": lambda job, host_object: self._exec_commands(VSUplinkAdd(job["task"]["VSUplinks"], quiet=job['binaryOpts']['quiet']), host_object),
            "VSUplinkRemove": lambda job, host_object: self._exec_commands(VSUplinkRemove(job["task"]["VSUplinks"], quiet=job['binaryOpts']['quiet']), host_object),
        }

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
                handler = task_handlers.get(task_type)
                if handler:
                    handler(job, host_object)
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
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Exiting...")
        sys.exit(0)
