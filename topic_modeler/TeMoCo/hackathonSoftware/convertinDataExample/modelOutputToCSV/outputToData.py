import os
import json
import re

filetxt ="topic,time,words,topic_size,filenames"

path = ""

raw = "denews_dtm2.json"
i=0

with  open(raw) as time:
    js = json.loads(time.read())   
    for timeslice in js:
        for topic in js.get('0', "none"):

            tpc = js.get(str(timeslice), "none").get(str(topic))
            tpcwords = tpc.get("topic_words", "none")
            word_list = tpcwords.split()
            tpcwords= ' '.join(word for word in word_list)
            tpcfile_list = tpc.get("top_articles", "none")
            tpcfiles = ' '.join(tpcfile_list)
            filetxt+= "\n"+"Topic"+str(topic)
            filetxt+=","+str(timeslice)
            filetxt+=","+  str(tpcwords)
            filetxt+= ","+str(tpc.get("topic_weight", "none"))+","
            filetxt+=str(tpcfiles)

f = open(""+"articles1"+".csv","w+")
f.write(filetxt)
f.close()
   