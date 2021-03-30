import os
import json
from dateutil.parser import parse
import time

alltweets = {}
lastdate = None
startup = True
while(True):
    try:
        cmd = "snscrape"
        if (lastdate != None):
            cmd += " --since "+str(lastdate.strftime("%Y-%m-%d"))
        cmd += " --jsonl --max-results 200 twitter-user vaccinetime" 
        tweets = os.popen(cmd).read()
        for tweet in tweets.split("\n"):
            if (tweet.strip() == ""):
                continue
            tweetd = json.loads(tweet)
            date = parse(tweetd['date'])
            if (lastdate == None or date > lastdate):
                lastdate = date
            content = tweetd['content']
            if (not(date in alltweets)):
                if ("CVS" in content):
                    if (startup):
                        print("Skipped old availability")
                    else:
                        print(content+" "+tweetd['outlinks'][0])
                        while(True):
                            cmd = "powershell.exe '(New-Object Media.SoundPlayer \"C:\\Windows\\Media\\notify.wav\").PlaySync()'" 
                            os.system(cmd)
                            time.sleep(1)
            alltweets[date] = content
        startup = False
    except:
        pass
    time.sleep(60)
    
