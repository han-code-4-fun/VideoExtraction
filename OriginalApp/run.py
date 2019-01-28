import mitmproxy.http
from mitmproxy import ctx
import requests
import json
import sys
import subprocess
import os
import time
import threading
import appiumForProject


#class counter is the mitmproxy API to check the flows 

class Counter:
    def __init__(self):
        self.num = 0


    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)


addons = [
    Counter()
]


#use ffmpeg to get the metadata of downloaded file
def getMETADATA(inputFile):
    command = ['ffprobe', '-show_format', inputFile]
    temp3 = subprocess.run(command, shell=True, capture_output=True).stdout.decode('utf-8')
    vidPos = temp3.find('vid:') + 4
    endPos = temp3.find('\r\n', vidPos)
    vidOutput = temp3[vidPos:endPos]
    return vidOutput



#convert the count into a partial name for future use
def covertDigg_count(inputNum):
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



path = 'video/'

num = 0


LengthListPreDownload = [] 
#this is used for avoid downloading duplicate file of current program run

number20 = 0
#check later code


def saveALLFile(inputDict):
    with open("saveThemAll.json", mode="w", encoding='utf-8') as efg:
        json.dump(inputDict, efg, ensure_ascii=False, indent=2)

with open('saveThemAll.json', mode='r', encoding='utf-8') as abc:
    allVideoJson = json.load(abc)  # file stores all the videos ever downloaded

def response(flow):
    global num,number20

   

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

        
        for currentVideo in json_data["aweme_list"]:
            
            vid = currentVideo["video"]["download_addr"]["uri"]
            likes= currentVideo["statistics"]["digg_count"]
            
            if vid in allVideoJson:
                #if we downloaded before, update digg_count(users likes)
                try:
                   
                    allVideoJson[vid].update({"hearts":likes})
                    saveALLFile(allVideoJson)
                except Exception:
                    print('something wrong with digg_count data of current Json')
            else:
               
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
               
               
                if cha in currentVideo: #which means this video joins a #topic
                    cid = currentVideo["cha_list"][0]["cid"]
                    cha_name = currentVideo["cha_list"][0]["cha_name"]
                    user_count = currentVideo["cha_list"][0]["user_count"]
                    saveAllDict[vid].update({
                        "topicID": cid,
                        "topicName": cha_name,
                        "topicUser": user_count
                    
                    })

               
                  
                allVideoJson.update(saveAllDict)
                saveALLFile(allVideoJson)
               


    
    else:
        #this part is to download videos
        #there are 2 ways to remove duplicate file,
        #1.save ContentLength from server header after downloaded
        #2.use after saved file, use its metadata's comments property (vid) to 
        #  match with vid in the saveAllDict
        #We use 2nd method to avoid mismatch contentlength of video files occasionally
        #which is how TikTok app recongnized the positions of their video
        #in each "currrent set"

        if flow.response.headers.get('Content-Type') == target_type: #if it's a mp4 file
            
            contentLength = flow.response.headers.get('Content-Length')
            #use for 1st check for duplicate 


            if contentLength in LengthListPreDownload:
                print('duplicate file     duplicate file     duplicate file     '
                        'duplicate file     duplicate file     duplicate file     ')
                print(len(LengthListPreDownload))
                
            else:

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

                
                print("pass length check     pass length check     pass length check    pass length check \
                    pass length check     pass length check     pass length check    pass length check ")

                
                

                res = requests.get(flow.request.url, stream=True)
               

                print("check 1111111111111111111111111111111111111111111111111111111111111111111111111111111111")

                filename = path + str(num) +'.mp4'
                print("check 2222222222222222222222222222222222222222222222222222222222222222222222222222222222 ")
                with open(filename, 'wb') as ffff:
                    ffff.write(res.content)
                    ffff.flush()
                    num = num + 1
                print("check 3333333333333333333333333333333333333333333333333333333333333333333333333file downloaded")
                
                thisvid = getMETADATA(filename)

            
                print("check metadata  check metadata  check metadata  check metadata  check metadata  ")
                if thisvid in allVideoJson:
                    
                    if allVideoJson[thisvid]["download"] > 0: #this file have been downloaded before
                        os.remove(filename)
                        print('downloaded before  before  before  before  before  before  before  before \
                        before  before  before  before  before  before  before  before  before  before ')
                    else:#this file hasn't been downloaded before
                        name = removeIllegalCharForWinOS(allVideoJson[thisvid]["videoName"])
                        likes = allVideoJson[thisvid]["hearts"]
                        newfilename = path + covertDigg_count(likes) + name + '.mp4'
                        try:
                            os.rename(filename,newfilename)
                        except FileExistsError:
                            #use a nameCounter to avoid duplicate videos if two videos have similar likes
                            #and no description or have same #topic
                            nameCounter = allVideoJson["anchor"]["countForDupName"]
                            newfilename = path + covertDigg_count(likes) + name + str(nameCounter) + '.mp4'
                            #rename file that starts with number of hearts allows user easily
                            #filter high hearts videos and watch
                            os.rename(filename,newfilename)
                            allVideoJson["anchor"]["countForDupName"] = nameCounter + 1
                        allVideoJson[thisvid]["download"] = 1 #this to prevent duplicate downloading
                        saveALLFile(allVideoJson)
                        LengthListPreDownload.insert(0, contentLength)
                        #add to the first position for a faster search
                        if likes > 1000000-1:
                            number20 = number20 + 1
                            if number20 >= 20:
                                sys.exit()
                                #when software download 20 qualified videos it will quit
                        appiumForProject.action.scroll()
                        #scroll down

                else:
                    os.remove(filename)
                    print("find advertisement video and removed removed removed removed removed removed\
                        removed removed removed removed removed removed removed removed removed removed\
                        removed removed removed removed removed removed removed removed removed removed")
                    appiumForProject.action.scroll()
                    #write an error report
                    with open('errorStrangeFile.txt',mode='a+',encoding='utf-8') as errStra:
                        errStra.write('vid: \r\n')
                        errStra.write('   ')
                        errStra.write(thisvid + "advertisement")
                        errStra.write('\r\n')



                
