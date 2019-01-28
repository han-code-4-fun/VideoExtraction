import requests
import json
import os
import time
import threading
import metadataHandler as metaHandler
import globalVariable as gb
import fileSaveAndLoad as saveload
import JSONHandler as jHandler
import downloadHandler as dHandler

allVideoJson=saveload.loadJsonFile()

def response(flow):
    
    target_type = 'video/mp4'
    json_target = 'ly/aweme/v1/feed/'

    if json_target in flow.request.url:  
        #when the app starts, few videos(current set) and their json info will be load first
        #same with that when you scroll to the end of current set of videos
        #So when we get json info we extract some info into our dict()
        saveAllDict= dict()

        req = flow.response.content
        json_data = json.loads(req)
        cha = "cha_list"

        jHandler.process(json_data,allVideoJson,saveAllDict,cha)
  
    
    else:
        #this part is to download videos
        #there are 2 ways to remove duplicate file,
        #1.check ContentLength from server header before downloading to reduce file I/O,
        #Because the server responses multiple versions of same video.
        #the contentlength of Files that have been downloaded in the current run will be 
        #saved to this ContentLength list.
        #2.used after file has been downloaded, use its metadata's comments property (vid) to 
        #  match with vid in the saveAllDict
        #We use 2nd method to avoid mismatch contentlength of video files occasionally
        #which is how TikTok app recongnized the positions of their video
        #in each "refresh"

        if flow.response.headers.get('Content-Type') == target_type: #if it's a mp4 file
            
            contentLength = flow.response.headers.get('Content-Length')
            #1st check for duplicate 
            if contentLength in gb.LengthListPreDownload:
                temp = "dumplicate file "
                print(temp * 10)
     
            else:
                response = requests.get(flow.request.url, stream=True)
                dHandler.process(response, allVideoJson, contentLength)




                
