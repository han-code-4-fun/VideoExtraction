import json

def saveALLFile(inputDict):
    with open("saveThemAll.json", mode="w", encoding='utf-8') as efg:
        json.dump(inputDict, efg, ensure_ascii=False, indent=2)
def loadJsonFile():
    with open('saveThemAll.json', mode='r', encoding='utf-8') as abc:
        allVideoJson = json.load(abc)  # file stores all the videos ever downloaded
        return allVideoJson