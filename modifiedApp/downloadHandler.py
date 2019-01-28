import os
import globalVariable as gb
import metadataHandler as metaHandler
import appiumForProject
import errorHandler as eHandler
import fileHandler as fHandler
import fileNameHandler as fNHandler
import fileSaveAndLoad as saveload


#1.download   and name in num
#2.check if vid is in the dict allVideoJson, if not (which is usually 
#  advertisement video and in a rare case, videos never meant to be 
#  in the app and the server just send them to the app. So, in this
#  case, we will delete them anyway and then we scroll down, this won't
#  affect any videos that may left behind, because each scrolling down
#  server will response to multiple URL at a given time. After testing,
#  this never be a problem), delete this video and scroll down
#  if yes,  use vid to check if it's been downloaded already
#  if downloaded, remove file, 
#  if not downloaded before,  use it's vid to get file name from 
#  allVideoJson, rename the file, update it's download status,
#  and add it's content length into LengthListPreDownload
#3. scrolldown



def process(response, allVideoJson, contentLength):

    filename = gb.path + str(gb.num) +'.mp4'
   
    with open(filename, 'wb') as ffff:
        ffff.write(response.content)
        ffff.flush()
        gb.num = gb.num + 1
   
    thisvid = metaHandler.getMETADATA(filename)


    if thisvid in allVideoJson:
        if allVideoJson[thisvid]["download"] > 0: #means this file have been downloaded before
            os.remove(filename)
            temp = "downloaded before "
            print(temp * 10)
        else:#this file hasn't been downloaded before
            fNHandler.renameFile(allVideoJson,thisvid, filename,contentLength)

    else:
        fHandler.removeFile(filename)
        #write an error report
        eHandler.writeErrorLog(thisvid)
       