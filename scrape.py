import os
import json
from dateutil.parser import parse
import time

def playSound(times):
    for i in range(times):
        cmd = "omxplayer --no-keys magic_bell.wav"
        os.system(cmd)
        if i + 1 < times:
            time.sleep(5)


alltweets = {}
lastdate = None
startup = True
playSound(1)
print("Running script")
while(True):
    try:
        cmd = "snscrape"
        if (lastdate != None):
            cmd += " --since "+str(lastdate.strftime("%Y-%m-%d"))
        cmd += " --jsonl --max-results 20 twitter-user vaccinetime" 
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
                if ("fizer" in content or "CVS" in content):
                    if (startup):
                        print("Skipped old availability")
                        print(content)
                    else:
                        print("NEW TWEET!!!")
                        print(content+" "+tweetd['outlinks'][0])
                        playSound(5)
                elif not startup:
                    print("Skipping uninteresting tweet")
                    print(content)
            alltweets[date] = content
        startup = False
    except:
        print("Exception running loop")
        pass
    time.sleep(60)
    
