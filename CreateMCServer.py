'''

1. Ask how many servers to create
2. Get available RAM in MB
3. Change update script accordingly.
4. For each server
    1. Create a new folder
    2. Copy update script from source folder (Keep track of source folder)
    3. move into the folder
    4. modify update script to reflect number (Screen name command)
    5. Create empty Minecraft_Server.jar file
    6. Run updater script
    7. Open Eula file and change to true
    8. Start server with appropriate RAM sizes
5. Change to Home directory
6. Create Start script
7. Add to startup
8. Create update script
9. Add to crontab

'''

import os
import sys
import subprocess
import psutil
import math
import shutil
import time


def run_update_script():
    os.chdir(os.path.join(os.getcwd(), 'MinecraftUpdater'))

    subprocess.call("python3 updater.py", shell=True)


def update_local_update_script(server_number, ram_size, source_directory):
    # Copy updater.py to local folder
    shutil.copy2(os.path.join(source_directory, 'updater.py'), os.getcwd())

    # Open the file and search for:
    # %%%%  <-- replace with the server_number
    # ^^^^  <-- replace with the ram_size
    with open('updater.py', 'r') as file:
        updater = file.readlines()

    with open('updater.py', 'w') as file:
        for line in updater:
            line.replace('%%%%', server_number)
            line.replace('^^^^', ram_size)
            file.write(line)


numberOfServers = input("Please enter the number of worlds to create:\n")
try:
    numberOfServers = int(numberOfServers)
except ValueError as e:
    print("Please enter a valid integer. Example: 4")
    sys.exit(1)

ramMemory = psutil.virtual_memory().total
ramMemory = int(ramMemory/(math.pow(1024, math.floor((math.log(ramMemory, 1024)))))) * 1024

sourceDirectory = os.getcwd()

for serverNumber in range(0, numberOfServers):
    minecraftNumber = 'minecraft{}'.format(serverNumber)
    try:
        # Try to create the folder for the server.  If it already exists, then move into the folder, and run the update
        # script instead.
        os.makedirs(os.path.join(os.path.expanduser('~'), minecraftNumber, "MinecraftUpdater"))
    except FileExistsError:
        os.chdir(os.path.join(os.path.expanduser('~'), minecraftNumber, "MinecraftUpdater"))
        run_update_script()
        continue

    #  Move into the folder
    os.chdir(os.path.join(os.getcwd(), minecraftNumber))

    subprocess.call("touch minecraft_server.jar", shell=True)

    # Modify the updater script
    update_local_update_script(serverNumber, ramMemory, sourceDirectory)

    run_update_script()

    time.sleep(60 * 2)

    # Open the eula.txt file and set it to true
    with open('eula.txt', 'r') as file:
        eula = file.readlines()

    with open('eula.txt', 'w') as file:
        for line in eula:
            line.replace('false', 'true')
            file.write(line)

    # Update the server.properties file with port numbers

    # Start the server.
    run_update_script()

os.chdir(os.path.expanduser('~'))

with open('startMinecraft.sh', 'w') as file:
    for serverNumber in range(0, numberOfServers):
        serverPath = os.path.join(os.path.expanduser('~'), 'minecraft{}'.format(serverNumber), "MinecraftUpdater")
        file.write("cd {}".format(serverPath))
        file.write("python3 updater.py")
        file.write("\n")

print("Files created and server(ss) running.  Please edit the /etc/rc.local file and add this line:")
print("{} &".format(os.path.join(os.path.expanduser('~'), " startMinecraft.sh")))
print("\nRun this command from your home directory:")
print("sudo chmod +x startMinecraft.sh")
