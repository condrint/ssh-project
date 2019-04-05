import sys
import time
import select
import paramiko

class SSH():
    def __init__(self, host, username=None, password=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

        if username and password: 
            self.ssh.connect(host, username=username, password=password)
        else:
            self.ssh.connect(host)

    def sendCommand(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command, timeout=10)

        error = stderr.read()
        if error:
            return 'Error: ' + error.decode("utf-8") 
        else:
            return stdout.read().decode("utf-8") 
"""       
# prompt user for these 
host = 'login.unx.csupomona.edu'
username = 'tjcondrin'
password = ''

ssh = SSH(host, username, password)
cmd = input('enter command')
ssh.sendCommand(cmd)
"""

