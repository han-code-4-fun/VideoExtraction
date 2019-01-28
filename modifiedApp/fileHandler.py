import os
import appiumForProject

def removeFile(filename):
    os.remove(filename)
    tempMSG = "find advertisement video and removed "
    print(tempMSG *3)
    appiumForProject.action.scroll()