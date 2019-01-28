import fileHandler as fHandler
import os
import sys
import globalVariable as gb
import fileSaveAndLoad as saveload
import appiumForProject


#convert the count into a partial name for future use
def prepareNameFromLikes(inputNum):
    if inputNum<=49999:
        return "_"
    if inputNum>49999 and inputNum<100000:
        return "50kHearts_"
    if inputNum>=100000 and inputNum<200000:
        return "100kHearts_"
    if inputNum >= 200000 and inputNum < 300000:
        return "200kHearts_"
    if inputNum >= 300000 and inputNum < 400000:
        return "300kHearts_"
    if inputNum >= 400000 and inputNum < 500000:
        return "400kHearts_"
    if inputNum >= 500000 and inputNum < 600000:
        return "500kHearts_"
    if inputNum >= 600000 and inputNum < 700000:
        return "600kHearts_"
    if inputNum >= 700000 and inputNum < 800000:
        return "700kHearts_"
    if inputNum >= 800000 and inputNum < 900000:
        return "800kHearts_"
    if inputNum >= 900000 and inputNum < 1000000:
        return "900kHearts_"
    if inputNum >= 1000000 and inputNum < 1500000:
        return "1mHearts_"
    if inputNum >= 1500000 and inputNum < 2000000:
        return "1.5mHearts_"
    if inputNum >= 2000000 and inputNum < 3000000:
        return "2mHearts_"
    if inputNum >= 3000000 and inputNum < 4000000:
        return "3mHearts_"
    if inputNum >= 4000000 and inputNum < 5000000:
        return "4mHearts_"
    if inputNum >= 5000000:
        return "5mHearts_"


def removeIllegalCharForWinOS(inputString):
    illegal='\/:*?"<>|'
    temp = []
    for ele in inputString:
        if ele not in illegal:
            temp.append(ele)
    return ''.join(temp)




def renameFile(allVideoJson,thisvid, filename,contentLength):
    name = removeIllegalCharForWinOS(allVideoJson[thisvid]["videoName"])
    likes = allVideoJson[thisvid]["hearts"]
    newfilename = gb.path + prepareNameFromLikes(likes) + name + '.mp4'
    try:
        os.rename(filename,newfilename)
    except FileExistsError:
        #use a nameCounter to avoid duplicate videos if two videos have similar likes
        #and no description or have same #topic
        nameCounter = allVideoJson["anchor"]["countForDupName"]
        newfilename = gb.path + prepareNameFromLikes(likes) + name + str(nameCounter) + '.mp4'
        #rename file that starts with number of hearts allows user easily
        #filter high hearts videos and watch
        os.rename(filename,newfilename)
        allVideoJson["anchor"]["countForDupName"] = nameCounter + 1 
        
    allVideoJson[thisvid]["download"] = 1 #this to prevent duplicate downloading
    saveload.saveALLFile(allVideoJson)
    gb.LengthListPreDownload.insert(0, contentLength)
    #add to the first position for a faster search
    if likes > 1000000-1:
        gb.number = gb.number + 1
        if gb.number >= 50:
            sys.exit()
            #when software download 50 qualified videos it will quit
    appiumForProject.action.scroll()
    #scroll down to next video