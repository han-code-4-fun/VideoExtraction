import fileSaveAndLoad

def updateExistingVideo(allVideoJson, vid,likes):
    try:    
        allVideoJson[vid].update({"hearts":likes})
        fileSaveAndLoad.saveALLFile(allVideoJson)
    except Exception:
        print('something wrong with digg_count data of current Json')

def recordTopic(cha, currentVideo, saveAllDict, vid):
    if cha in currentVideo: #which means this video joins a #topic
        cid = currentVideo["cha_list"][0]["cid"]
        cha_name = currentVideo["cha_list"][0]["cha_name"]
        user_count = currentVideo["cha_list"][0]["user_count"]
        saveAllDict[vid].update({
            "topicID": cid,
            "topicName": cha_name,
            "topicUser": user_count
        
        })

def saveNewJSONToLocalJSONFile(currentVideo, saveAllDict,vid, cha,likes,allVideoJson):
    
    videoid = currentVideo["aweme_id"]
    name = currentVideo["desc"]
    author_id = currentVideo["author_user_id"] 
    author_nickname = currentVideo["author"]["nickname"]
    music_id = currentVideo["music"]["id_str"]
    #collect author_id and music_id for further development
    #Eg. if we really like some channel, and we can write function
    #to save videos into an seperate folder under the channel's name
    
    saveAllDict[vid]= {
        "videoName": name,
        "hearts": likes,
        "videoID": videoid,
        "channelID": author_id,
        "channelName": author_nickname,
        "musicID": music_id,
        "download": 0 

    }
    
    
    recordTopic(cha, currentVideo, saveAllDict, vid)

    allVideoJson.update(saveAllDict)
    fileSaveAndLoad.saveALLFile(allVideoJson)


def process(json_data,allVideoJson,saveAllDict,cha):

    for currentVideo in json_data["aweme_list"]:
        
        vid = currentVideo["video"]["download_addr"]["uri"]
        likes= currentVideo["statistics"]["digg_count"]
        
        if vid in allVideoJson:
            #if we downloaded before, update digg_count(users likes)
            updateExistingVideo(allVideoJson, vid,likes)
            
        else:
            saveNewJSONToLocalJSONFile(currentVideo, saveAllDict,vid, cha,likes, allVideoJson)
            
           