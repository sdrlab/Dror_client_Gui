from paramiko import SSHClient
client = SSHClient()
client.load_system_host_keys()

