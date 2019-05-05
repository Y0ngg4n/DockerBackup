#  Copyright (c) 2019.
#  Author: Andre Schuele / Yonggan
#
import subprocess, re, json, os, time

####################################
# Edit this to your output folder! #
####################################
outputFolder = "/backup/containerBackup"


####################################

def backupAllContainer():
    bashCommand = "docker ps"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    containerIDs = getContainerIDs(output)
    for container in containerIDs:
        backupContainer(container)


def getContainerIDs(input):
    p = re.compile("([\d\w]+)\s{8}[[a-z]")
    result = p.findall(input)
    return result


def backupContainer(containerID):
    print(
        "############################################################################################################")
    print
    print("Container: " + containerID)
    bashCommand = "docker container inspect " + containerID
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    jsonParse = json.loads(str(output))
    for i in range(len(jsonParse)):
        containerName = jsonParse[i]['Name']
        print("Container Name: " + containerName)
        backupFolder = outputFolder + "/" + containerName
        if not os.path.exists(backupFolder):
            os.makedirs(backupFolder)
        f = open(backupFolder + containerName + "_backup_inspect_" + time.strftime("%Y-%m-%d_%H-%M-%S_%Z",
                                                                                   time.gmtime()) + ".txt", "w")
        f.write(output)
        f.close()
        bashCommand = "docker export --output=" + backupFolder + containerName + "_backup" \
                      + time.strftime("%Y-%m-%d_%H-%M-%S_%Z", time.gmtime()) + ".tar " + containerName
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output);
        print("************************************************************************************************"
              "************")
        print(" Backup of " + containerName + " successfully created! ")
        print("************************************************************************************************"
              "************")
        print
        print


backupAllContainer()
