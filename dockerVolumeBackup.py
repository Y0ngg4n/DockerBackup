#  Copyright (c) 2019.
#  Author: Andre Schuele / Yonggan
#  Based on this: http://scorban.de/2018/02/06/auto-backup-fuer-docker-volumes/

import subprocess, re, json, os, time

####################################
# Edit this to your output folder! #
####################################
outputFolder = "/backup/volumeBackup"
####################################

def backupAllContainer():
    bashCommand = "docker ps"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    containerIDs = getContainerIDs(output)
    for container in containerIDs:
        backupVolumes(container)


def getContainerIDs(input):
    p = re.compile("([\d\w]+)\s{8}[[a-z]")
    result = p.findall(input)
    return result


def backupVolumes(containerID):
    print("############################################################################################################")
    print
    print("Container: " + containerID)
    bashCommand = "docker container inspect " + containerID
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    jsonParse = json.loads(str(output))
    for i in range(len(jsonParse)):
        containerName = jsonParse[i]['Name']
        print("Container Name: " + containerName)
        mounts = jsonParse[i]['Mounts']
        for mount in mounts:
            try:
                mountName = mount['Name']
                print("Mountname: " + mountName)
                backupFolder = outputFolder + containerName + mount['Destination']
                if not os.path.exists(backupFolder):
                    os.makedirs(backupFolder)
                bashCommand = "docker run -v " + mountName + ":/volume -v " + backupFolder \
                              + ":/backup --rm scorb/docker-volume-backup backup " + containerName + "_backup_" \
                              + time.strftime("%Y-%m-%d_%H-%M-%S_%Z", time.gmtime())
                process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                print(output);
                print("************************************************************************************************"
                      "************")
                print(" Backup of " + containerName + " | " + mountName + " successfully created! ")
                print("************************************************************************************************"
                      "************")
                print
                print
            except Exception as e:
                print(e)
                print('No volume ID found')
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(" Backup of " + containerName + " failed!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print
                print


backupAllContainer()
