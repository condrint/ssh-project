import sys
import time
import select
import paramiko


# prompt user for these 
host = 'login.unx.csupomona.edu'
username = 'tjcondrin'
password = ''

# run these when connect is hit
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
ssh.connect(host, username=username, password=password)
print ("Connected to %s" % host)


"""
# Send the command (non-blocking)
stdin, stdout, stderr = ssh.exec_command("my_long_command --arg 1 --arg 2")

# Wait for the command to terminate
while not stdout.channel.exit_status_ready():
    # Only print data if there is data to read in the channel
    if stdout.channel.recv_ready():
        rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
        if len(rl) > 0:
            # Print data from stdout
            print (stdout.channel.recv(1024))

#
# Disconnect from the host
#
print ("Command done, closing SSH connection")

"""
ssh.close()