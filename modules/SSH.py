import paramiko
import time

class SSH:
    def __init__(self, host, username, password):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(host, username=username, password=password)
           
        except paramiko.AuthenticationException as e:
            print (f'Authentication failed: {e}')
        
        except paramiko.SSHException as e:
            print (f'SSH connection error: {e}')
        
        except Exception as e:
            print (f'An unexpected error occurred: {e}')
        

    def ssh_command_execution(self,command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            
            output = ""

            while not (stdout.channel.exit_status_ready()):
                if stdout.channel.recv_ready():
                    output += stdout.channel.recv(4096).decode()
                
                time.sleep(0.1)
            
            if stdout.channel.recv_ready():
                output += stdout.channel.recv(4096).decode()

            exit_status = stdout.channel.recv_exit_status()

            if exit_status!= 0:
                return output
            else:
                return "Execution successful"

        except Exception as e:
            return f'Command execution failed: {e}' 

    