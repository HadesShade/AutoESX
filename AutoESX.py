import yaml
import argparse
import sys
from modules.host import Host
from modules.group import Group
from modules.jobs.VMImport import VMImport
from modules.jobs.VMExport import VMExport
from modules.initialize import Initialize

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
                acceptAllEulas=host['serverData'].get('acceptAllEulas', False)
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
                "task": job["task"]
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
            task_type = job["task"]["type"]
            target_hosts = job.get("hosts", [])
            if "groups" in job:
                for group in job["groups"]:
                    target_group = next(g[group] for g in self.groups if group in g)
                    target_hosts.extend(target_group.hosts)

            for host in target_hosts:
                host_object = next(h[host] for h in self.hosts if host in h)
                if task_type == "VMImport":
                    vm_import = VMImport(job["task"]["virtualMachines"], host_object.connection_dictionary())
                    vm_import.import_vms()
                elif task_type == "VMExport":
                    vm_export = VMExport(job["task"]["virtualMachines"], host_object.connection_dictionary())
                    vm_export.export_vms()
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
    except:
        print("An error occurred! Exiting...")
        sys.exit(0)