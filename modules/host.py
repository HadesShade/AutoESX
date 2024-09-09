from modules.SSH import SSH

class Host:
    def __init__(self, name, type, address, username, password, httpsPort, SSLVerify=True, acceptAllEulas=False):
        self.name = name
        self.type = type
        self.address = address
        self.username = username
        self.password = password
        self.sanitized_password = password.replace('$', '\\$')
        self.httpsPort = httpsPort
        self.ssh = SSH(self.address, self.username, self.password)

        self.options = list()
        if not SSLVerify:
            self.options.append('--noSSLVerify')
        if acceptAllEulas:
            self.options.append('--acceptAllEulas')
    
    def connection_dictionary(self):
        host_connection_dictionary = {
            "hostOptions": f"{' '.join(self.options)}",
            "hostURL": f"vi://{self.username}:{self.sanitized_password}@{self.address}:{self.httpsPort}",
            "hostName": self.name
        }
        return host_connection_dictionary
