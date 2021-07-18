import json
import requests
import uuid
import os
from tqdm import tqdm
import time
from retrying import retry


class BirdSoundDownloader(object):
    def __init__(self,jsonObj,currentPage=1):
        self.jsonObj = jsonObj
        self.currentPage = currentPage
        self.totalPages = self.jsonObj.get('numPages')
    
    def setNextPage(self,pageNumber):
        self.currentPage = pageNumber
    
    def getRecords(self):
        return self.jsonObj.get('recordings')
        
    def getUrl(self,record):
        return record.get('file','')
    
    def getName(self,record):
        return record.get('en','unknown')
    
    @retry(stop_max_attempt_number=10, wait_random_min=2000, wait_random_max=5000)
    def downloadUrl(self,url,bird_name):
        
        audioData = requests.get(url)
        
        _id = uuid.uuid4().hex[:8]
        localFile = ''.join(['new_recordings/',bird_name,'/',bird_name,_id,'.wav'])
        os.makedirs(os.path.dirname(localFile), exist_ok=True)
        with open(localFile,'wb') as f:
            f.write(audioData.content)

def main():
    json_directory = os.getcwd() + "/json_downloads"
    print ()
    
    for r in os.listdir(json_directory):
        fileName = r
        print (fileName)
        data = json.load(
            open('new-approach/'+fileName)
            )
        bsd = BirdSoundDownloader(data)
        records = bsd.getRecords()
        for record in tqdm(records):
            if birdUrl := bsd.getUrl(record):
                birdName = bsd.getName(record)
                birdUrl = 'https:' + birdUrl
                bsd.downloadUrl(birdUrl,birdName)
    

if __name__ == "__main__":
    main()
