
#!/usr/bin/env python
'''
Name: Thomas Cole Amick
Run: python backup.py
'''

#
#Imports 
#

import urllib
import subprocess
import os
from subprocess import call
from datetime import  date

#
#Variables
#143.88.65.57
HOSTNAME= raw_input('Hostname: ')
#datastore1
DATASTORE= raw_input('Datastore: ')
#VI
SOURCE_TYPE= raw_input('Source Type(ex.VI): ')
USERNAME=raw_input('Username: ')
PASSWORD=raw_input('Password: ')

today = date.today()
TARGET_PATH='/home/cole/workspace/CSBL_Scripts/'+ str(today) +'_VMs' 


#Format password for url
ENCODED_PASSWORD = urllib.quote(PASSWORD)

#Grab machine names
#The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
server_creds = "vi://" + USERNAME + ':' + ENCODED_PASSWORD + '@' + HOSTNAME #vi://${USERNAME}:${ENCODED_PASSWORD}@${HOSTNAME}/
MACHINES = subprocess.Popen(['ovftool', '--sourceType=' + SOURCE_TYPE , '--datastore=' + DATASTORE, server_creds + '/' ], stdout = subprocess.PIPE  )

#Put machine names in a list of strings
machineList = []
for machine in iter(MACHINES.stdout.readline,''):
  machineList.append(machine.strip())


if not os.path.exists(TARGET_PATH):
  os.makedirs(TARGET_PATH)

#remove ovftool eroor message  
machineList.pop(0)

for machine in machineList:
  print "Backing up: " + machine
  TARGET = TARGET_PATH + '/' + machine
  ENCODED_MACHINE_NAME = urllib.quote(machine)
  subprocess.call(['ovftool', '--sourceType=' + SOURCE_TYPE , '--datastore=' + DATASTORE, server_creds + '/' + machine, TARGET_PATH])


